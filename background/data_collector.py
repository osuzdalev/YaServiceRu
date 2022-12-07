"""Collection of silent functions gathering data about every user that interacts with the bot"""

from configparser import ConfigParser
import logging

from telegram import Update
from telegram.ext import ContextTypes, TypeHandler, MessageHandler, filters, ChatMemberHandler

import background.telegram_database_utils as tldb

logger_data_collector = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def collect_data(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Add user data and message data to DB"""
    logger_data_collector.info("collect_data()")
    logger_data_collector.debug(
        "update.chat_member: {}".format(update.chat_member))
    user = None
    # logger_data_collector.info("update.effective_user: {}".format(update.effective_user))
    message = None
    # logger_data_collector.info("update.effective_message: {}".format(update.effective_message))
    try:
        logger_data_collector.debug("try 1")
        user = update.message.from_user
        # logger_data_collector.info("update.message.from_user: {}".format(update.message.from_user))
        message = update.effective_message
        # logger_data_collector.info("update.effective_message: {}".format(update.effective_message))
    except AttributeError:
        try:
            logger_data_collector.debug("try 2")
            user = update.callback_query.from_user
            # logger_data_collector.info("update.callback_query.from_user: {}".format(update.callback_query.from_user))
            message = update.callback_query.message
            # logger_data_collector.info("update.callback_query.message: {}".format(update.callback_query.message))
        except AttributeError:
            logger_data_collector.info("Update cannot be collected")
            return

    tldb.insert_new_user(user.id, user.username, user.first_name, user.last_name)
    tldb.insert_message(message.message_id, user.id, message.text)

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


async def user_status(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Keeps track of users interacting with the bot or blocking it and updates flag in DB"""
    logger_data_collector.info("user_status()")
    logger_data_collector.info("update.my_chat_member.new_chat_member.status: {}".format(update.my_chat_member.new_chat_member.status))

data_collection_handler = TypeHandler(Update, collect_data)
collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
user_status_handler = ChatMemberHandler(user_status, ChatMemberHandler.CHAT_MEMBER)
