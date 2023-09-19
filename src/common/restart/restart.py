import inspect
import logging

from telegram import (
    Update
)
from telegram.ext import ContextTypes

logger_start = logging.getLogger(__name__)


async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger_start.info(f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}")

    context.bot_data["restart"] = True
    context.application.stop_running()
