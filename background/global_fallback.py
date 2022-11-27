import logging

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger_global_fallback = logging.getLogger(__name__)

commands_re = r"^(\/start|\/request|\/wiki|\/pay|\/assign \d*|\/orders|\/complete \d*|/commands)$"


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger_global_fallback.info("unknown_command()")
    await update.message.reply_text("Unknown command")

global_fallback_handler = MessageHandler(filters.COMMAND & (~ filters.Regex(commands_re)), unknown_command)
