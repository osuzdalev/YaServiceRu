import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler, ConversationHandler

logger_global_fallback = logging.getLogger(__name__)

# Customer commands
start = "/start"
request = "/request"
wiki = "/wiki"
pay = "/pay"
cancel = "/cancel"

customer_commands = [start, request, wiki, pay, cancel]

# Contractor commands
assign = "/assign \d*"
complete = "/complete \d*"
commands = "/commands"

contractor_commands = [assign, complete, commands]

# Center commands
orders = "/orders"
center_commands = [orders]

commands = customer_commands + contractor_commands + center_commands
commands_re = ""
for i in range(len(commands)):
    commands_re += "\\" + commands[i] + "|"
commands_re = r"^(" + commands_re + ")$"


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger_global_fallback.info("unknown_command()")
    await update.message.reply_text("Incorrect command")


global_fallback_handler = MessageHandler(filters.COMMAND & (~ filters.Regex(commands_re)), unknown_command)
