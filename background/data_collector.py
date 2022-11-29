"""Collection of silent functions gathering data about every user that interacts with the bot"""

from configparser import ConfigParser
import logging

from telegram import Update
from telegram.ext import ContextTypes, TypeHandler, MessageHandler, filters

import background.telegram_database as tldb

logger_data_collector = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def collect_data(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Add user data and message data to DB"""
    logger_data_collector.info("collect_data()")
    user = update.message.from_user
    tldb.insert_new_user(user.id, user.username, user.first_name, user.last_name)

    logger_data_collector.info("update.effective_message: {}".format(update.effective_message))
    logger_data_collector.info("update.effective_user: {}".format(update.effective_user))


async def collect_phone_number(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if Phone# in DB and adds it to appropriate UserID"""
    logger_data_collector.info("collect_phone_number()")
    user = update.effective_user
    phone_number = update.message.contact.phone_number

    # Check if PhoneNumber already in Database
    if tldb.get_user_data(user.id)[4] is None:
        tldb.insert_user_phone_number(user.id, phone_number)
    else:
        await update.message.reply_text("Phone number already in Database")


data_collection_handler = TypeHandler(Update, collect_data)
collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
