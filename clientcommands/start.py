import logging

from telegram import Update, PhotoSize
from telegram.ext import ContextTypes, CommandHandler

from background import telegram_database as tldb

logger_start = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stuff"""
    logger_start.info("start()")

    context.user_data["Device_Context"] = None

    file_id = "AgACAgIAAxkBAAEaZ8Zjg_V9gCfMtNcDSjgJkDskCLjIpQAC28gxG-wcIEjay-bnmleibAEAAwIAA3MAAysE"
    file_unique_id = "AQAD28gxG-wcIEh4"
    test_size = PhotoSize(file_id, file_unique_id, 10, 10)
    path = "/Users/osuz/Downloads/photo_2022-11-18 23.52.33.jpeg"
    await update.message.reply_photo(path, caption="Some Caption")
    await update.message.reply_text("Welcome!\n"
                                    "/wiki - find an easy fix\n"
                                    "/request - contact customer service\n"
                                    "/pay - send a payment")

start_handler = CommandHandler("start", start)
