"""Collection of silent functions gathering data about every user that interacts with the bot"""

from configparser import ConfigParser
import logging
from typing import Tuple, Optional

from telegram import Update, User, Message
from telegram.ext import ContextTypes, TypeHandler, MessageHandler, filters, ChatMemberHandler

import background.telegram_database_utils as tldb

logger_data_collector = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


def extract_user_and_message(update: Update) -> Tuple[Optional[User], Optional[Message]]:
    """Extract user and message from the update."""

    user = update.message.from_user if update.message else update.callback_query.from_user if update.callback_query else None
    message = update.effective_message if update.message else update.callback_query.message if update.callback_query else None

    return user, message


def log_callback_data(update: Update) -> None:
    """Log callback data if it exists."""
    try:
        callback_data = update.callback_query.data
        logger_data_collector.info(f"CALLBACK_DATA: {callback_data}")
    except (AttributeError, TypeError):
        logger_data_collector.info("NO CALLBACK DATA")


async def collect_data(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Add user data and message data to DB"""

    # Extract user and message information
    user, message = extract_user_and_message(update)

    # Log user details if user exists
    if user:
        logger_data_collector.info(f"({user.id}, {user.name}, {user.first_name}) collect_data")

    # Log callback data if it exists
    log_callback_data(update)

    # Check if user and message are extracted successfully
    if user and message:
        tldb.insert_new_user(user.id, user.username, user.first_name, user.last_name)
        tldb.insert_message(message.message_id, user.id, message.text)
    else:
        logger_data_collector.info("Update cannot be collected")


async def collect_phone_number(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if Phone# in DB and adds it to appropriate UserID"""
    logger_data_collector.debug("collect_phone_number()")
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
    logger_data_collector.info(
        "update.my_chat_member.new_chat_member.status: {}".format(update.my_chat_member.new_chat_member.status))


data_collection_handler = TypeHandler(Update, collect_data)
collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
user_status_handler = ChatMemberHandler(user_status, ChatMemberHandler.CHAT_MEMBER)
