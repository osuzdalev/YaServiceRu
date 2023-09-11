import logging

from telegram import Update
from telegram.ext import ContextTypes

from src.common.markups import DEFAULT_CLIENT_MARKUP
from src.common.data_reader.data_reader import DataReader


logger_start = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Needs to be used first after every reboot of the Bot."""
    # Get the name of the current function
    user = update.message.from_user
    logger_start.info(f"({user.id}, {user.name}, {user.first_name})")

    context.user_data["in_conversation"] = ""
    context.user_data["Device_Context"] = []

    await update.message.reply_text(
        "Добро пожаловать!", reply_markup=DEFAULT_CLIENT_MARKUP
    )
    # Send introduction video
    await update.message.reply_video(DataReader(context.bot_data["config"]["name"]).start.get_introduction_video())
