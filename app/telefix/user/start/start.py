from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

from app.telefix.core.data_reader import StartReader
from app.telefix.common.markups import DEFAULT_CLIENT_MARKUP


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, start_reader: StartReader
) -> None:
    """
    # NOTE Needs to be used first by user/admin after every reboot of the Bot.
    """
    user = update.message.from_user
    logger.info(f"({user.id}, {user.name}, {user.first_name})")

    context.user_data["in_conversation"] = ""
    context.user_data["Device_Context"] = []

    await update.message.reply_text(
        "Добро пожаловать!", reply_markup=DEFAULT_CLIENT_MARKUP
    )
    # Send introduction video
    await update.message.reply_video(start_reader.get_introduction_video())
