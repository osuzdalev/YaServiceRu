import logging
import os
import re
from typing import List, Tuple, Dict

import openai
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
chatgpt_history_start = [{"role": "system", "content": instructions}]

MODEL_NAME = "gpt-3.5-turbo"
TEMPERATURE = 0.6
MAX_TOKENS = 350
TOP_P = 0.9
FREQUENCY_PENALTY = 1.0
PRESENCE_PENALTY = 0.3

FREE_CHATGPT_LIMIT = 5
CONFIRM_PAYMENT = "CONFIRM_CHATGPT_PAYMENT"
DECLINE_PAYMENT = "DECLINE_CHATGPT_PAYMENT"
EXTENDED_PAYLOAD = "chatgpt_extended_payload"
LABEL = "ChatGPT extension"
MAX_TOKEN = 4096


async def chatgpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets flag in user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    logger_chatgpt.info("chatgpt_start()")

    # First time calling the chat feature
    if "chatgpt_level" not in context.user_data:
        context.user_data["chatgpt_active"] = True
        context.user_data["chatgpt_level"] = 0
        context.user_data["chatgpt_messages_sent"] = 0
        context.user_data["chatgpt_premium"] = False
        context.user_data["chatgpt_history"] = chatgpt_history_start
        context.user_data["chatgtp_premium_history"] = chatgpt_history_start

        await update.message.reply_text("Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
                                        "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop"
                                        .format(5 - context.user_data["chatgpt_messages_sent"]))

    # Already previously called the chat feature
    elif context.user_data["chatgpt_level"] in (0, 1) and context.user_data["chatgpt_messages_sent"] < 5:
        context.user_data["chatgpt_active"] = True
        await update.message.reply_text("Чат с ChatGPT начат. Вы можете отправить еще {} сообщений в чат."
                                        "\n\nЧтобы остановить ChatGPT, просто отправьте /chat_stop"
                                        .format(5 - context.user_data["chatgpt_messages_sent"]))
    # Test if user already used 5 messages
    elif context.user_data["chatgpt_level"] == 1 and context.user_data["chatgpt_messages_sent"] >= 5:
        message_text = (
            "Вы достигли лимита бесплатного взаимодействия с нашим LLM. "
            "Если вы хотите продолжить получать помощь от нашего LLM, мы предлагаем опцию оплаты за использование, "
            "которая позволяет продлить разговор. "
            "Пожалуйста, обратите внимание, что этот продленный разговор будет ограничен 4096 символами, "
            "обеспечивая фокусированное и эффективное взаимодействие. "
            "\n\nЧтобы продолжить с опцией оплаты за использование, введите {}, "
            "а затем следуйте инструкциям для оплаты."
            " Если вы не хотите продолжать, введите {} и не стесняйтесь обращаться к нам в будущем, "
            "если вам потребуется помощь.".format(CONFIRM_PAYMENT, DECLINE_PAYMENT)
        )
        await update.message.reply_text(message_text)


def get_chatgpt_response(user_message: str, conversation_history: List[Dict]) -> Tuple[str, List[Dict]]:
    """Sends the requests over the openAI API"""
    logger_chatgpt.info("get_chatgpt_response()")

    conversation_history.append({"role": "user", "content": user_message})

    completion = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=conversation_history,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        top_p=TOP_P,
        frequency_penalty=FREQUENCY_PENALTY,
        presence_penalty=PRESENCE_PENALTY
    )
    conversation_history.append({"role": "assistant", "content": completion.choices[0].message["content"]})

    response = re.sub(r'^\n{2}', '', completion.choices[0].message["content"])

    return response, conversation_history


async def chatgpt_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the Chatgpt service that uses the api"""
    logger_chatgpt.info("chatgpt_request()")

    # Check if the user activated the chat feature
    if not context.user_data.get("chatgpt_active", False):
        await update.message.reply_text("Похоже, вы не начали чат. Для этого используйте команду '/chat'")
        return

    user_level = context.user_data["chatgpt_level"]
    # First time using the chat feature
    if user_level == 0:
        context.user_data["chatgpt_level"] = 1
        # get the response and the updated conversation
        response, context.user_data["chatgpt_history"] = get_chatgpt_response(update.effective_message.text,
                                                                              context.user_data["chatgpt_history"])
        context.user_data["chatgpt_messages_sent"] += 1
        messages_left = 5 - context.user_data["chatgpt_messages_sent"]
        response += f"\n\nОсталось {messages_left} сообщений"
        await update.message.reply_text(response)
    # Previously used the chat feature but still within test limit and not premium yet
    elif user_level == 1 and context.user_data["chatgpt_messages_sent"] < 5 and not context.user_data["chatgpt_premium"]:
        # get the response and the updated conversation
        response, context.user_data["chatgpt_history"] = get_chatgpt_response(update.effective_message.text,
                                                                              context.user_data["chatgpt_history"])
        context.user_data["chatgpt_messages_sent"] += 1
        messages_left = 5 - context.user_data["chatgpt_messages_sent"]
        response += f"\n\nОсталось {messages_left} сообщений"
        await update.message.reply_text(response)

    # Check if user sent 5 messages but did not upgrade to premium
    elif user_level == 1 and context.user_data["chatgpt_messages_sent"] >= 5 and not context.user_data["chatgpt_premium"]:
        # Propose CHATGPT extension by payment at end of 5 free messages
        message_text = (
            "Вы достигли лимита бесплатного взаимодействия с нашим LLM. "
            "Если вы хотите продолжить получать помощь от нашего LLM, мы предлагаем опцию оплаты за использование, "
            "которая позволяет продлить разговор. "
            "Пожалуйста, обратите внимание, что этот продленный разговор будет ограничен 4096 символами, "
            "обеспечивая фокусированное и эффективное взаимодействие. "
            "\n\nЧтобы продолжить с опцией оплаты за использование, введите {}, "
            "а затем следуйте инструкциям для оплаты."
            " Если вы не хотите продолжать, введите {} и не стесняйтесь обращаться к нам в будущем, "
            "если вам потребуется помощь.".format(CONFIRM_PAYMENT, DECLINE_PAYMENT)
        )
        await update.message.reply_text(message_text)

    # Check if user paid for chatgpt service
    else:
        # get the response and the updated conversation
        response, context.user_data["chatgpt_premium_history"] = get_chatgpt_response(update.effective_message.text,
                                                                              context.user_data["chatgpt_premium_history"])

        # Calculate the remaining tokens
        used_tokens = sum(num_tokens_from_string(message["content"]) for message in context.user_data["chatgpt_premium_history"])
        remaining_tokens = MAX_TOKEN - used_tokens

        # Update the response message to include the remaining tokens
        response += f"\n\nОсталось {remaining_tokens} токенов"

        await update.message.reply_text(response)


async def chatgpt_payment_yes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to pay for more interactions."""
    logger_chatgpt.info("chatgpt_payment_yes()")

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


async def chatgpt_precheckout_callback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreCheckoutQuery"""
    logger_chatgpt.info("chatgpt_precheckout_callback()")
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != EXTENDED_PAYLOAD:
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


async def chatgpt_successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    logger_chatgpt.info("successful_payment_callback()")

    context.user_data["chatgpt_premium"] = True
    context.user_data["chatgtp_premium_history"] = context.user_data["chatgtp_history"]
    context.user_data["chatgtp_history"] = chatgpt_history_start

    await update.message.reply_text("Thank you for your payment!")


async def chatgpt_payment_no(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles user's response to not pay for more interactions."""
    logger_chatgpt.info("chatgpt_payment_no()")

    await update.message.reply_text("Ваш ответ был получен. Спасибо за использование нашего сервиса!"
                                    "Пожалуйста, не стесняйтесь возвращаться в любое время!")


async def chatgpt_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsets the flag in the user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    logger_chatgpt.info("chatgpt_stop()")

    # Check if there is a chat to stop
    if context.user_data.get("chatgpt_active", False):
        context.user_data["chatgpt_active"] = False
        await update.message.reply_text("YaService-GPT остановлен. "
                                        "Ваши сообщения больше не будут отправляться на YaService-GPT.")


chatgpt_handler_command = CommandHandler("chat", chatgpt_start)
chatgpt_handler_message = MessageHandler(filters.Regex(r"^🤖YaService-GPT$"), chatgpt_start)

chatgpt_request_handler = MessageHandler(filters.TEXT & ~(filters.Regex(ignored_texts_re) | filters.COMMAND),
                                         chatgpt_request)

chatgpt_payment_yes_handler = MessageHandler(filters.Regex(r"^{}$".format(CONFIRM_PAYMENT)), chatgpt_payment_yes)
chatgpt_precheckout_handler = PreCheckoutQueryHandler(chatgpt_precheckout_callback)
# TODO add condition specific to chatgpt payment
chatgpt_successful_payment_handler = MessageHandler(filters.SUCCESSFUL_PAYMENT, chatgpt_successful_payment_callback)
chatgpt_payment_no_handler = MessageHandler(filters.Regex(r"^{}$".format(DECLINE_PAYMENT)), chatgpt_payment_no)


chatgpt_stop_handler_command = CommandHandler("chat_stop", chatgpt_stop)
chatgpt_stop_handler_message = MessageHandler(filters.Regex(r"^❌Отменить$"), chatgpt_stop)
