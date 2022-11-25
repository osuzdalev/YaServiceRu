import logging

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from background import telegram_database as tldb

logger_start = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stuff"""
    logger_start.info("start()")

    user = update.message.from_user
    logger_start.info("Bot started by user {}".format(user.username))
    tldb.insert_new_customer(user.id, user.username, user.first_name, user.last_name)

    context.user_data["Device_Context"] = None

    await update.message.reply_text("Welcome!\n"
                                    "/faq - find an easy fix\n"
                                    "/request - contact customer service")
