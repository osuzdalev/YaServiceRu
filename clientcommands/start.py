import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from markups.default import default_client_markup

logger_start = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Needs to be used first after every reboot of the Bot."""
    logger_start.info("start()")

    context.user_data['in_conversation'] = ''
    context.user_data["Device_Context"] = None

    await update.message.reply_text("Добро пожаловать!", reply_markup=default_client_markup)

start_handler = CommandHandler("start", start)
