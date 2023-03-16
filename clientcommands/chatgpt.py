import logging
import re

import openai
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from resources.constants_loader import load_constants
from background.global_fallback import ignored_messages_re

logger_chatgpt = logging.getLogger(__name__)
constants = load_constants()

openai.api_key = constants.get("API", "OPENAI")

chatgpt_history = [{"role": "system", "content": "You are a helpful assistant."}]


async def chatgpt_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sets flag in user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    logger_chatgpt.info("chatgpt_start()")

    context.user_data["chatgpt"] = 1
    context.user_data["chatgpt_history"] = chatgpt_history

    await update.message.reply_text("ChatGPT started. You may write 5 times to the chat. Please write your 1st question")


async def chatgpt_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the Chatgpt service that uses the api"""
    logger_chatgpt.info("chatgpt_request()")

    # Check if the user used the "/chat" command to start send API requests
    chatgpt_active = context.user_data.get("chatgpt", 0)
    if chatgpt_active == 0:
        await update.message.reply_text("It seems you did not start the Chat. To do so, send the '/chat' command")
        return

    context.user_data["chatgpt_history"].append({"role": "user", "content": update.effective_message.text})

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context.user_data["chatgpt_history"]
    )

    response = re.sub(r'^\n{2}', '', completion.choices[0].message["content"])

    context.user_data["chatgpt_history"].append({"role": "assistant", "content": completion.choices[0].message["content"]})
    chatgpt_requests_sent = (len(context.user_data["chatgpt_history"]) - 1) // 2

    await update.message.reply_text(response + "\n\n {} / 5".format(chatgpt_requests_sent))


async def chatgpt_stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Unsets the flag in the user context that sends every incoming message from the user
    as a request to ChatGPT through the API"""
    logger_chatgpt.info("chatgpt_stop()")

    context.user_data["chatgpt"] = 0

    await update.message.reply_text("ChatGPT stopped. Your messages will no longer be sent to ChatGPT.")


chatgpt_handler_command = CommandHandler("chat", chatgpt_start)
chatgpt_handler_message = MessageHandler(filters.Regex(r"^chat$"), chatgpt_start)

chatgpt_request_handler = MessageHandler(filters.TEXT & ~(filters.Regex(ignored_messages_re) | filters.COMMAND),
                                         chatgpt_request)

chatgpt_stop_handler_command = CommandHandler("chat_stop", chatgpt_stop)
