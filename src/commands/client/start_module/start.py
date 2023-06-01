import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from src.common.markups_default import default_client_markup

logger_start = logging.getLogger(__name__)

with open('data/start_data/file_id.txt') as file:
    start_video_file_id = file.readline().strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Needs to be used first after every reboot of the Bot."""
    user = update.message.from_user
    logger_start.info("({}, {}, {}) /start".format(user.id, user.name, user.first_name))

    context.user_data["in_conversation"] = ""
    context.user_data["Device_Context"] = []

    await update.message.reply_text(
        "Добро пожаловать!", reply_markup=default_client_markup
    )
    # Send introduction video
    await update.message.reply_document("BAACAgIAAxkDAAIJ1WR4pdC8CNUnYGVIfYAHM6agFN5JAAIWLwACVIfJS1b_wHklPwzKLwQ")

start_handler = CommandHandler("start", start)