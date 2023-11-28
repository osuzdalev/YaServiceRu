from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger_global_fallback.info(f"({user.id}, {user.name}, {user.first_name})")
    await update.message.reply_text("Incorrect user")
