import inspect
import logging

from telegram import Update
from telegram.ext import ContextTypes

logger_global_fallback = logging.getLogger(__name__)


async def unknown_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger_global_fallback.info(
        f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
    )
    await update.message.reply_text("Incorrect user")
