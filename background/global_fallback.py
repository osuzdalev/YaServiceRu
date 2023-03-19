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

customer_replykeyboard_buttons = [wiki_button, request_button, cancel_button]

# Customer special messages
chatgpt_confirm_pay_message = "CONFIRM_CHATGPT_PAYMENT"
chatgpt_decline_pay_message = "DECLINE_CHATGPT_PAYMENT"

customer_special_messages = [chatgpt_confirm_pay_message, chatgpt_decline_pay_message]

# Contractor commands
assign = "/assign \d*"
complete = "/complete \d*"
commands = "/commands"

contractor_commands = [assign, complete, commands]

# Center commands
orders = "/orders"
center_commands = [orders]

ignored_commands = customer_commands + contractor_commands + center_commands
ignored_commands_re = r"^(" + "|".join("\\" + message for message in ignored_commands) + ")$"

ignored_texts = customer_replykeyboard_buttons + customer_special_messages
ignored_texts_re = r"^(" + "|".join(message for message in ignored_texts) + ")$"


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger_global_fallback.info("unknown_command()")
    await update.message.reply_text("Incorrect command")


global_fallback_handler = MessageHandler(filters.COMMAND & (~ filters.Regex(ignored_commands_re)), unknown_command)
