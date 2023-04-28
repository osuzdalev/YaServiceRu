import logging
import re
from typing import List, Tuple, Dict

import openai
from openai import InvalidRequestError

from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler
from telegram.constants import ParseMode

from resources.constants_loader import load_constants
from background.global_fallback import ignored_texts_re
from clientcommands.chatgpt_module.chatgpt_data.config import *
from clientcommands.chatgpt_module.token_count import num_tokens_from_string
from clientcommands.chatgpt_module.prompt_validation import validate_prompt, check_conversation_tokens

logger_chatgpt = logging.getLogger(__name__)
constants = load_constants()

openai.api_key = constants.get("API", "OPENAI")

# Load the model to GPU if available
EMBEDDING_MODEL.to(DEVICE)


async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Activates the ChatGPT feature for the user by setting a flag in their context that sends every incoming message
    to ChatGPT through the API. If the user has not used the ChatGPT feature before, initializes the necessary
    context variables.
    If the user has used the ChatGPT feature before, checks if they have reached the free prompts limit"""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_start".format(user.id, user.name, user.first_name))

    # First time calling the chat feature
    if "GPT_level" not in context.user_data:
        context.user_data["GPT_active"] = True
        context.user_data["GPT_level"] = 0
        context.user_data["GPT_messages_sent"] = 0
        context.user_data["GPT_premium"] = False
        context.user_data["GPT_conversation"] = GPT_CONVERSATION_START
        context.user_data["GPT_premium_conversation"] = GPT_CONVERSATION_START

        await update.message.reply_text("Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
                                        "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop"
                                        .format(FREE_PROMPT_LIMIT - context.user_data["GPT_messages_sent"]))

    # Already previously called the chat feature
    elif context.user_data["GPT_level"] in (0, 1) and context.user_data["GPT_messages_sent"] < FREE_PROMPT_LIMIT:
        context.user_data["GPT_active"] = True
        await update.message.reply_text("Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
                                        "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop"
                                        .format(FREE_PROMPT_LIMIT - context.user_data["GPT_messages_sent"]))
    # Test if user already used 5 messages
    elif context.user_data["GPT_level"] == 1 and context.user_data["GPT_messages_sent"] >= FREE_PROMPT_LIMIT:
        await update.message.reply_text(MAX_MESSAGES_STRING, parse_mode=ParseMode.MARKDOWN_V2)


def generate_chatbot_response(user_message: str, conversation: List[Dict]) -> str:
    """
    Generates a response from the ChatGPT model given the user's message and the conversation history.

    Args:
        user_message (str): The message sent by the user to the chatbot.
        conversation (List[Dict]): A list of dictionary objects representing the conversation history, with each
            dictionary containing "role" (the speaker) and "content" (the message content).

    Returns:
        str: The response generated by the ChatGPT model.
    """
    logger_chatgpt.info("generate_chatbot_response()")

    conversation.append({"role": "user", "content": user_message})
    try:
        completion = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=conversation,
            temperature=TEMPERATURE,
            max_tokens=MAX_RESPONSE_TOKENS,
            top_p=TOP_P,
            frequency_penalty=FREQUENCY_PENALTY,
            presence_penalty=PRESENCE_PENALTY
        )
    except InvalidRequestError as e:
        logger_chatgpt.error(f"InvalidRequestError: {e}")
        # Appending the context.user_data["conversation"]
        conversation[-1]["content"] = "[TOO_LONG]"

        response = "An error occurred while processing your request. Please try again with shorter text."
        conversation.append({"role": "assistant", "content": response})
        return response

    # Appending the context.user_data["conversation"]
    conversation.append({"role": "assistant", "content": completion.choices[0].message["content"]})
    response = re.sub(r'^\n{2}', '', completion.choices[0].message["content"])
    return response


async def gpt_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs the ChatGPT service that uses the API. Handles the request after it has been checked."""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_request".format(user.id, user.name, user.first_name))

    is_valid_prompt = await validate_prompt(update, context)
    if not is_valid_prompt:
        return

    user_level = context.user_data["GPT_level"]
    prompt = update.effective_message.text
    conversation = context.user_data["GPT_premium_conversation"] if context.user_data["GPT_premium"] else \
        context.user_data["GPT_conversation"]
    is_premium = context.user_data["GPT_premium"]

    # Send a gif to let the user know the prompt is being handled
    with open('clientcommands/chatgpt_module/chatgpt_data/loading_gif.mp4', 'rb') as gif_file:
        loading_gif = await update.message.reply_video(gif_file)

    # First time using the chat feature
    if user_level == 0:
        context.user_data["GPT_level"] = 1
        conversation_size_check, conversation_tokens = check_conversation_tokens(prompt, conversation)
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {FREE_PROMPT_LIMIT - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(conversation_tokens, LIMIT_CONVERSATION_TOKENS))

    # Previously used the chat feature but still within test limit and not premium yet
    elif user_level == 1 and context.user_data["GPT_messages_sent"] < FREE_PROMPT_LIMIT and not is_premium:
        conversation_size_check, conversation_tokens = check_conversation_tokens(prompt, conversation)
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {FREE_PROMPT_LIMIT - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(conversation_tokens, LIMIT_CONVERSATION_TOKENS))

    # Check if user sent 5 messages but did not upgrade to premium
    elif user_level == 1 and context.user_data["GPT_messages_sent"] >= FREE_PROMPT_LIMIT and not is_premium:
        # Propose CHATGPT extension by payment at end of 5 free messages
        await update.message.reply_text(MAX_MESSAGES_STRING, parse_mode=ParseMode.MARKDOWN_V2)

    # Check if user paid for chatgpt service
    else:
        conversation_size_check, conversation_tokens = check_conversation_tokens(prompt, conversation)
        # Check for conversation token size
        if conversation_size_check:
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            # Update the response message to include the remaining tokens
            response += f"\n\nОсталось {conversation_tokens} токенов"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(conversation_tokens, LIMIT_CONVERSATION_TOKENS))


async def gpt_payment_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to pay for more interactions."""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_payment_yes".format(user.id, user.name, user.first_name))

    chat_id = update.message.chat_id
    title = "YaService-GPT Premium"
    description = "Увеличить длину разговора до 4096 токенов."
    # select a payload just for you to recognize its the donation from your bot
    payload = EXTENDED_PAYLOAD
    currency = "RUB"
    price = 100
    # price * 100 to include 2 decimal points
    prices = [LabeledPrice(LABEL, price * 100)]

    await context.bot.send_invoice(
        chat_id, title, description, payload, constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA_TEST"), currency, prices
    )


async def gpt_precheckout_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreCheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is it from this bot and about this service?
    if query.invoice_payload == EXTENDED_PAYLOAD:
        print("EXTENDED_PAYLOAD: ", EXTENDED_PAYLOAD)
        logger_chatgpt.info("/gpt_precheckout_callback")
        await query.answer(ok=True)


async def gpt_successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the successful payment. Set the user to Premium category and update conversation data"""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /successful_payment_callback".format(user.id, user.name, user.first_name))

    context.user_data["GPT_premium"] = True
    context.user_data["GPT_premium_conversation"] = context.user_data["GPT_history"]
    context.user_data["GPT_history"] = GPT_CONVERSATION_START

    await update.message.reply_text("Thank you for your payment!")


async def gpt_payment_no(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to not pay for more interactions."""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_payment_no".format(user.id, user.name, user.first_name))

    await update.message.reply_text("Ваш ответ был получен. Спасибо за использование нашего сервиса!"
                                    "Пожалуйста, не стесняйтесь возвращаться в любое время!")


async def gpt_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsets the flag in the user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_stop".format(user.id, user.name, user.first_name))

    # Check if there is a chat to stop
    if context.user_data.get("GPT_active", False):
        context.user_data["GPT_active"] = False
        await update.message.reply_text("YaService-GPT остановлен. "
                                        "Ваши сообщения больше не будут отправляться на YaService-GPT.")


async def gpt_get_remaining_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to the user with the amount of tokens he has left in his current conversation"""
    conversation_history = context.user_data["GPT_premium_conversation"] if context.user_data["GPT_premium"] \
        else context.user_data["GPT_conversation"]
    conversation_tokens = sum(num_tokens_from_string(message["content"]) for message in conversation_history)
    remaining_tokens = LIMIT_CONVERSATION_TOKENS - conversation_tokens

    await update.message.reply_text("You currently have {} tokens left".format(remaining_tokens))


gpt_handler_command = CommandHandler("chat", gpt_start)
gpt_handler_message = MessageHandler(filters.Regex(r"^🤖Чат с подержкой$"), gpt_start)

gpt_request_handler = MessageHandler(filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND), gpt_request)

gpt_payment_yes_handler = MessageHandler(filters.Regex(r"^{}$".format(CONFIRM_PAYMENT)), gpt_payment_yes)
gpt_precheckout_handler = PreCheckoutQueryHandler(gpt_precheckout_callback)
# TODO add condition specific to chatgpt payment
gpt_successful_payment_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, gpt_successful_payment_callback)
gpt_payment_no_handler = MessageHandler(filters.Regex(r"^{}$".format(DECLINE_PAYMENT)), gpt_payment_no)

gpt_stop_handler_command = CommandHandler("chat_stop", gpt_stop)
gpt_stop_handler_message = MessageHandler(filters.Regex(r"^❌Отменить$"), gpt_stop)

gpt_get_remaining_tokens_handler = CommandHandler("token", gpt_get_remaining_tokens)
