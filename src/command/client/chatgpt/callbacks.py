import logging
import re
from typing import List, Dict
import os

import openai
from openai import InvalidRequestError

from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
)
from telegram.constants import ParseMode

from dotenv import load_dotenv
from src.command.client.chatgpt.config import ChatGPTConfig
from src.common.data.reader import DataReader
from src.command.client.chatgpt.utils import num_tokens_from_string
from src.command.client.prompt_filter.prompt_validation import (
    validate_prompt,
    check_conversation_tokens,
)

logger_chatgpt = logging.getLogger(__name__)
load_dotenv()

openai.api_key = os.getenv("API_OPENAI")

request_inline_keyboard = [
    [InlineKeyboardButton("Обратиться к специалисту", callback_data="REQUEST_COMMAND")]
]
reply_request_inline_markup = InlineKeyboardMarkup(request_inline_keyboard)

CHATGPT_CONFIG = ChatGPTConfig()
DataReader = DataReader()


async def gpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Activates the ChatGPT feature for the user by setting a flag in their context that sends every incoming message
    to ChatGPT through the API. If the user has not used the ChatGPT feature before, initializes the necessary
    context variables.
    If the user has used the ChatGPT feature before, checks if they have reached the free prompts limit
    """
    user = update.message.from_user
    logger_chatgpt.info(f"({user.id}, {user.name}, {user.first_name}) /gpt_start")

    # First time calling the chat feature
    if "GPT_level" not in context.user_data:
        context.user_data["GPT_active"] = True
        context.user_data["GPT_level"] = 0
        context.user_data["GPT_messages_sent"] = 0
        context.user_data["GPT_premium"] = False
        context.user_data["GPT_conversation"] = CHATGPT_CONFIG.model.conversation_init
        context.user_data[
            "GPT_premium_conversation"
        ] = CHATGPT_CONFIG.model.conversation_init

        await update.message.reply_text(
            "Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
            "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop".format(
                CHATGPT_CONFIG.model.free_prompt_limit
                - context.user_data["GPT_messages_sent"]
            )
        )

    # Already previously called the chat feature
    elif (
        context.user_data["GPT_level"] in (0, 1)
        and context.user_data["GPT_messages_sent"] < CHATGPT_CONFIG.model.free_prompt_limit
    ):
        context.user_data["GPT_active"] = True
        await update.message.reply_text(
            "Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
            "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop".format(
                CHATGPT_CONFIG.model.free_prompt_limit
                - context.user_data["GPT_messages_sent"]
            )
        )
    # tests if user already used 5 messages
    elif (
        context.user_data["GPT_level"] == 1
        and context.user_data["GPT_messages_sent"] >= CHATGPT_CONFIG.model.free_prompt_limit
    ):
        await update.message.reply_text(
            CHATGPT_CONFIG.messages.max_messages, parse_mode=ParseMode.MARKDOWN_V2
        )


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
            model=CHATGPT_CONFIG.model.name,
            messages=conversation,
            temperature=CHATGPT_CONFIG.model.temperature,
            max_tokens=CHATGPT_CONFIG.model.max_response_tokens,
            top_p=CHATGPT_CONFIG.model.top_p,
            frequency_penalty=CHATGPT_CONFIG.model.frequency_penalty,
            presence_penalty=CHATGPT_CONFIG.model.presence_penalty,
        )
    except InvalidRequestError as e:
        logger_chatgpt.error(f"InvalidRequestError: {e}")
        # Appending the context.user_data["conversation"]
        conversation[-1]["content"] = "[TOO_LONG]"

        response = "An error occurred while processing your request. Please try again with shorter text."
        conversation.append({"role": "assistant", "content": response})
        return response

    # Appending the context.user_data["conversation"]
    conversation.append(
        {"role": "assistant", "content": completion.choices[0].message["content"]}
    )
    response = re.sub(r"^\n{2}", "", completion.choices[0].message["content"])
    return response


async def gpt_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Runs the ChatGPT service that uses the API. Handles the request after it has been checked."""
    user = update.message.from_user
    logger_chatgpt.info(f"({user.id}, {user.name}, {user.first_name}) /gpt_request")

    # Checking if user prompt is a valid question
    is_valid_prompt = await validate_prompt(update, context)
    if not is_valid_prompt:
        return

    user_level = context.user_data["GPT_level"]
    prompt = update.effective_message.text
    conversation = (
        context.user_data["GPT_premium_conversation"]
        if context.user_data["GPT_premium"]
        else context.user_data["GPT_conversation"]
    )
    is_premium = context.user_data["GPT_premium"]

    # Send a gif to let the user know the prompt is being handled
    loading_gif = await update.message.reply_video(DataReader.chatgpt.get_loading_gif())

    # First time using the chat feature
    if user_level == 0:
        context.user_data["GPT_level"] = 1
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {CHATGPT_CONFIG.model.free_prompt_limit - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens, CHATGPT_CONFIG.model.limit_conversation_tokens
                )
            )

    # Previously used the chat feature but still within test limit and not premium yet
    elif (
        user_level == 1
        and context.user_data["GPT_messages_sent"] < CHATGPT_CONFIG.model.free_prompt_limit
        and not is_premium
    ):
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            print("CONVERSATION_TOKENS: ", conversation_tokens)
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            context.user_data["GPT_messages_sent"] += 1
            response += f"\n\nОсталось {CHATGPT_CONFIG.model.free_prompt_limit - context.user_data['GPT_messages_sent']} сообщений"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens, CHATGPT_CONFIG.model.limit_conversation_tokens
                )
            )

    # Check if user sent 5 messages but did not upgrade to premium
    elif (
        user_level == 1
        and context.user_data["GPT_messages_sent"] >= CHATGPT_CONFIG.model.free_prompt_limit
        and not is_premium
    ):
        # Propose CHATGPT extension by payment at end of 5 free messages
        await update.message.reply_text(
            CHATGPT_CONFIG.messages.max_messages, parse_mode=ParseMode.MARKDOWN_V2
        )

    # Check if user paid for chatgpt service
    else:
        conversation_size_check, conversation_tokens = check_conversation_tokens(
            prompt, conversation
        )
        # Check for conversation token size
        if conversation_size_check:
            # get the response
            response = generate_chatbot_response(prompt, conversation)
            # Update the response message to include the remaining tokens
            response += f"\n\nОсталось {conversation_tokens} токенов"
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                response, reply_markup=reply_request_inline_markup
            )
        else:
            await context.bot.delete_message(update.effective_chat.id, loading_gif.id)
            await update.message.reply_text(
                "Conversation too long: {} tokens (MAX {})".format(
                    conversation_tokens, CHATGPT_CONFIG.model.limit_conversation_tokens
                )
            )


async def gpt_payment_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to pay for more interactions."""
    user = update.message.from_user
    logger_chatgpt.info(f"({user.id}, {user.name}, {user.first_name}) /gpt_payment_yes")

    chat_id = update.message.chat_id
    title = "YaService-GPT Premium"
    description = "Увеличить длину разговора до 4096 токенов."
    # select a payload just for you to recognize its the donation from your bot
    payload = CHATGPT_CONFIG.checkout_variables.extended_payload
    currency = "RUB"
    price = 100
    # price * 100 to include 2 decimal points
    prices = [LabeledPrice(CHATGPT_CONFIG.checkout_variables.extended_label, price * 100)]

    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        os.getenv("TOKEN_PAYMENT_PROVIDER_YOOKASSA"),
        currency,
        prices,
    )


async def gpt_precheckout_callback(
    update: Update, _: ContextTypes.DEFAULT_TYPE
) -> None:
    """Answers the PreCheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is it from this bot and about this service?
    if query.invoice_payload == CHATGPT_CONFIG.checkout_variables.extended_payload:
        print("EXTENDED_PAYLOAD: ", CHATGPT_CONFIG.checkout_variables.extended_payload)
        logger_chatgpt.info("/gpt_precheckout_callback")
        await query.answer(ok=True)


async def gpt_successful_payment_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Handle the successful payment. Set the user to Premium category and update conversation database"""
    user = update.message.from_user
    logger_chatgpt.info(
        f"({user.id}, {user.name}, {user.first_name}) /successful_payment_callback"
    )

    context.user_data["GPT_premium"] = True
    context.user_data["GPT_premium_conversation"] = context.user_data["GPT_history"]
    context.user_data["GPT_history"] = CHATGPT_CONFIG.model.conversation_init

    await update.message.reply_text("Thank you for your payment!")


async def gpt_payment_no(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to not pay for more interactions."""
    user = update.message.from_user
    logger_chatgpt.info(f"({user.id}, {user.name}, {user.first_name}) /gpt_payment_no")

    await update.message.reply_text(
        "Ваш ответ был получен. Спасибо за использование нашего сервиса!"
        "Пожалуйста, не стесняйтесь возвращаться в любое время!"
    )


async def gpt_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsets the flag in the user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    user = update.message.from_user
    logger_chatgpt.info(f"({user.id}, {user.name}, {user.first_name}) /gpt_stop")

    # Check if there is a chat to stop
    if context.user_data.get("GPT_active", False):
        context.user_data["GPT_active"] = False
        await update.message.reply_text(
            "YaService-GPT остановлен. "
            "Ваши сообщения больше не будут отправляться на YaService-GPT."
        )


async def gpt_get_remaining_tokens(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends a message to the user with the amount of tokens he has left in his current conversation"""
    conversation_history = (
        context.user_data["GPT_premium_conversation"]
        if context.user_data["GPT_premium"]
        else context.user_data["GPT_conversation"]
    )
    conversation_tokens = sum(
        num_tokens_from_string(message["content"]) for message in conversation_history
    )
    remaining_tokens = CHATGPT_CONFIG.model.limit_conversation_tokens - conversation_tokens

    await update.message.reply_text(
        f"You currently have {remaining_tokens} tokens left"
    )
