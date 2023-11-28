import inspect
from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

from ...core.data_reader import StartReader
from ...common.markups import DEFAULT_CLIENT_MARKUP


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
    await update.message.reply_video(
        StartReader(context.bot_data["config"]["name"]).get_introduction_video()
    )
