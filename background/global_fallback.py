import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger_global_fallback = logging.getLogger(__name__)

# Customer commands
start = "/start"
request = "/request"
wiki = "/wiki"
pay = "/pay"
cancel = "/cancel"
chat = "/chat"
chat_stop = "/chat_stop"

customer_commands = [start, request, wiki, pay, cancel, chat, chat_stop]

# Customer ReplyKeyboardButtons
wiki_button = "📖Вики"
request_button = "🤓Специалист"
cancel_button = "❌Отменить"

customer_buttons = [wiki_button, request_button, cancel_button]

# Contractor commands
assign = "/assign \d*"
complete = "/complete \d*"
commands = "/commands"

contractor_commands = [assign, complete, commands]

# Center commands
orders = "/orders"
center_commands = [orders]

ignored_messages = customer_commands + customer_buttons + contractor_commands + center_commands
ignored_messages_re = r"^(" + "|".join("\\" + message for message in ignored_messages) + ")$"


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger_global_fallback.info("unknown_command()")
    await update.message.reply_text("Incorrect command")


global_fallback_handler = MessageHandler(filters.COMMAND & (~ filters.Regex(ignored_messages_re)), unknown_command)
