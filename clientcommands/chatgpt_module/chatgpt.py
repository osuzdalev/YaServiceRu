import logging
import os
import re
from typing import List, Tuple, Dict

import openai
from openai import InvalidRequestError
from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler
from telegram.constants import ParseMode

from resources.constants_loader import load_constants
from background.global_fallback import ignored_texts_re

from clientcommands.chatgpt_module.token_count import num_tokens_from_string

logger_chatgpt = logging.getLogger(__name__)
constants = load_constants()

openai.api_key = constants.get("API", "OPENAI")

INSTRUCTIONS_PATH = "system_instructions.txt"
FULL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), INSTRUCTIONS_PATH)
with open(FULL_PATH, "r") as file:
    instructions = file.read()
GPT_conversation_start = [{"role": "system", "content": instructions}]

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.6
MAX_RESPONSE_TOKENS = 350
TOP_P = 0.9
FREQUENCY_PENALTY = 1.0
PRESENCE_PENALTY = 0.3

FREE_PROMPT_LIMIT = 3
EXTENDED_PAYLOAD = "GPT_extended_payload"
LABEL = "YaService-GPT extension"

MAX_CONVERSATION_TOKENS = 4096
# Amount of tokens in a conversation to at least get a minimum response
LIMIT_CONVERSATION_TOKENS = MAX_CONVERSATION_TOKENS - MAX_RESPONSE_TOKENS
INSTRUCTIONS_TOKENS = num_tokens_from_string(instructions)
MAX_SUM_RESPONSE_TOKENS = FREE_PROMPT_LIMIT * MAX_RESPONSE_TOKENS
# max size prompt to at least get one answer
MAX_PROMPT_TOKENS = MAX_CONVERSATION_TOKENS - INSTRUCTIONS_TOKENS - MAX_RESPONSE_TOKENS

CONFIRM_PAYMENT = "CONFIRM_CHATGPT_PAYMENT"
DECLINE_PAYMENT = "DECLINE_CHATGPT_PAYMENT"
MAX_MESSAGES_STRING = "Вы достигли лимита бесплатного взаимодействия с нашим LLM\. " \
                      "Если вы хотите продолжить получать помощь от нашего LLM, " \
                      "мы предлагаем опцию оплаты за использование, которая позволяет продлить разговор\. " \
                      "Пожалуйста, обратите внимание, что этот продленный разговор будет ограничен 4096 символами, " \
                      "обеспечивая фокусированное и эффективное взаимодействие\. " \
                      "\n\nЧтобы продолжить с опцией оплаты за использование, введите `{}`, " \
                      "а затем следуйте инструкциям для оплаты\. " \
                      "Если вы не хотите продолжать, введите `{}` и не стесняйтесь обращаться к нам в будущем, " \
                      "если вам потребуется помощь\.".format(CONFIRM_PAYMENT, DECLINE_PAYMENT)


async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets flag in user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_start".format(user.id, user.name, user.first_name))

    # First time calling the chat feature
    if "GPT_level" not in context.user_data:
        context.user_data["GPT_active"] = True
        context.user_data["GPT_level"] = 0
        context.user_data["GPT_messages_sent"] = 0
        context.user_data["GPT_premium"] = False
        context.user_data["GPT_conversation"] = GPT_conversation_start
        context.user_data["GPT_premium_conversation"] = GPT_conversation_start

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


def check_prompt_tokens(prompt: str) -> Tuple[bool, int]:
    """Check if the sent message size is within bounds"""
    # Calculate tokens
    prompt_tokens = num_tokens_from_string(prompt)
    remaining_tokens = MAX_PROMPT_TOKENS - prompt_tokens
    logger_chatgpt.info("prompt_size_check: {}".format(prompt_tokens))

    return (True, remaining_tokens) if prompt_tokens < MAX_PROMPT_TOKENS else (False, prompt_tokens)


async def get_conversation_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to the user with the amount of tokens he has left in his current conversation"""
    conversation_history = context.user_data["GPT_premium_conversation"] if context.user_data["GPT_premium"] \
        else context.user_data["GPT_conversation"]
    conversation_tokens = sum(num_tokens_from_string(message["content"]) for message in conversation_history)
    remaining_tokens = LIMIT_CONVERSATION_TOKENS - conversation_tokens

    await update.message.reply_text("You currently have {} tokens left".format(remaining_tokens))


def check_conversation_tokens(prompt: str, conversation: List[Dict]) -> Tuple[bool, int]:
    """Check if conversation size is within bounds. Takes into account the minimum response token size
    that needs to be left after everything for the user to get a response."""

    # Calculate tokens
    conversation_tokens = sum(num_tokens_from_string(message["content"]) for message in conversation) + \
                          num_tokens_from_string(prompt)
    remaining_tokens = LIMIT_CONVERSATION_TOKENS - conversation_tokens

    return (True, remaining_tokens) if conversation_tokens < LIMIT_CONVERSATION_TOKENS else (False, conversation_tokens)


def get_gpt_response(user_message: str, conversation: List[Dict]) -> str:
    """Sends the requests over the openAI API"""
    logger_chatgpt.info("get_gpt_response()")

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
    """Runs the Chatgpt service that uses the api. Will check several parameters including the user's level and
    prompt sent. Based on those parameters will handle the request accordingly """
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_request".format(user.id, user.name, user.first_name))

    # Check if the user activated the chat feature
    if not context.user_data.get("GPT_active", False):
        await update.message.reply_text("Похоже, вы не начали чат. Для этого используйте команду '/chat'")
        return

    user_level = context.user_data["GPT_level"]
    prompt = update.effective_message.text
    conversation = context.user_data["GPT_premium_conversation"] if context.user_data["GPT_premium"] else context.user_data["GPT_conversation"]
    is_premium = context.user_data["GPT_premium"]

    # Check if prompt is too long
    prompt_size_check, prompt_tokens = check_prompt_tokens(prompt)
    if not prompt_size_check:
        await update.message.reply_text(
            "Prompt too long: {} tokens (MAX {})".format(prompt_tokens, MAX_PROMPT_TOKENS))
        logger_chatgpt.info("({}, {}, {}) - prompt too long".format(user.id, user.name, user.first_name))
        return

    # letting user know the prompt is being handled
    loading_gif = await update.message.reply_video(open("clientcommands/chatgpt_module/loading-slow-internet.mp4", "rb"))

    # First time using the chat feature
    if user_level == 0:
        context.user_data["GPT_level"] = 1
        conversation_size_check, conversation_tokens = check_conversation_tokens(prompt, conversation)
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = get_gpt_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {FREE_PROMPT_LIMIT - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(conversation_tokens, LIMIT_CONVERSATION_TOKENS))

    # Previously used the chat feature but still within test limit and not premium yet
    elif user_level == 1 and context.user_data["GPT_messages_sent"] < FREE_PROMPT_LIMIT and not is_premium:
        conversation_size_check, conversation_tokens = check_conversation_tokens(prompt, conversation)
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = get_gpt_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {FREE_PROMPT_LIMIT - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
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
            response = get_gpt_response(prompt, conversation)
            # Update the response message to include the remaining tokens
            response += f"\n\nОсталось {conversation_tokens} токенов"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(response)
        else:
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(conversation_tokens, LIMIT_CONVERSATION_TOKENS))


async def gpt_payment_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to pay for more interactions."""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_payment_yes".format(user.id, user.name, user.first_name))

    chat_id = update.message.chat_id
    title = "CHATGPT EXTENDED"
    description = "Увеличить длину разговора до 4096 токенов."
    # select a payload just for you to recognize its the donation from your bot
    payload = EXTENDED_PAYLOAD
    currency = "RUB"
    price = 100
    # price * 100 to include 2 decimal points
    prices = [LabeledPrice(LABEL, price * 100)]

    # TODO which payment service?
    await context.bot.send_invoice(
        chat_id, title, description, payload, constants.get("TOKEN", "PAYMENT_PROVIDER_SBERBANK_TEST"), currency, prices
    )


async def gpt_precheckout_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreCheckoutQuery"""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /gpt_precheckout_callback".format(user.id, user.name, user.first_name))
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != EXTENDED_PAYLOAD:
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


async def gpt_successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    user = update.message.from_user
    logger_chatgpt.info("({}, {}, {}) /successful_payment_callback".format(user.id, user.name, user.first_name))

    context.user_data["GPT_premium"] = True
    context.user_data["GPT_premium_conversation"] = context.user_data["GPT_history"]
    context.user_data["GPT_history"] = GPT_conversation_start

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


gpt_handler_command = CommandHandler("chat", gpt_start)
gpt_handler_message = MessageHandler(filters.Regex(r"^🤖YaService-GPT$"), gpt_start)

gpt_request_handler = MessageHandler(filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND),
                                         gpt_request)

gpt_payment_yes_handler = MessageHandler(filters.Regex(r"^{}$".format(CONFIRM_PAYMENT)), gpt_payment_yes)
gpt_precheckout_handler = PreCheckoutQueryHandler(gpt_precheckout_callback)
# TODO add condition specific to chatgpt payment
gpt_successful_payment_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, gpt_successful_payment_callback)
gpt_payment_no_handler = MessageHandler(filters.Regex(r"^{}$".format(DECLINE_PAYMENT)), gpt_payment_no)

gpt_stop_handler_command = CommandHandler("chat_stop", gpt_stop)
gpt_stop_handler_message = MessageHandler(filters.Regex(r"^❌Отменить$"), gpt_stop)

gpt_get_conversation_tokens_handler = CommandHandler("token", get_conversation_tokens)
