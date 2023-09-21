import logging

from telegram import Update
from telegram.ext import ContextTypes

logger_global_fallback = logging.getLogger(__name__)


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    logger_global_fallback.info("unknown_command()")
    await update.message.reply_text("Incorrect command")
