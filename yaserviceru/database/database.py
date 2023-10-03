"""Collection of silent functions gathering database about every user that interacts with the app"""

import inspect
import logging
from typing import Tuple, Optional

from telegram import Update, User, Message
from telegram.ext import (
    ContextTypes,
)

from yaserviceru.database import utils as tldb

logger_data_collector = logging.getLogger(__name__)


async def get_postgres(_: Update, context: ContextTypes.DEFAULT_TYPE) -> dict:
    DB_AUTH = {
        "host": context.bot_data["config"]["database"]["host"],
        "dbname": context.bot_data["config"]["database"]["dbname"],
        "user": context.bot_data["config"]["database"]["user"],
        "port": context.bot_data["config"]["database"]["port"],
        "password": context.bot_data["config"]["database"]["secret"]["password"],
    }
    return DB_AUTH


async def collect_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Is called everytime a message/Update is sent to bot.
    Writes user info and message to DB"""

    # Extract user and message information
    user, message = extract_user_and_message(update)

    # Log user details if user exists
    if user:
        logger_data_collector.info(
            f"({user.id}, {user.name}, {user.first_name}) {inspect.currentframe().f_code.co_name}"
        )

    # Log the callback data if it exists
    log_callback_data(update)

    # Write to database
    if user and message:
        db_auth = await get_postgres(update, context)
        tldb.insert_new_user(
            user.id, user.username, user.first_name, user.last_name, db_auth
        )
        tldb.insert_message(message.message_id, user.id, message.text, db_auth)
    else:
        logger_data_collector.info("Update cannot be collected")


def log_callback_data(update: Update) -> None:
    """Log the callback data if it exists."""
    try:
        callback_data = update.callback_query.data
        logger_data_collector.info(f"CALLBACK_DATA: {callback_data}")
    except (AttributeError, TypeError):
        logger_data_collector.info("NO CALLBACK DATA")


def extract_user_and_message(
    update: Update,
) -> Tuple[Optional[User], Optional[Message]]:
    """
    Extract the user and message from a given update.

    This function handles the extraction of the user and message from
    an update object, which can originate from either a direct message
    or a callback query. The function checks the type of update and
    extracts the user and message accordingly. If neither is found,
    it returns (None, None).

    Parameters:
    - update: The update object containing the incoming update.

    Returns:
    - A tuple containing the User object and Message object extracted
      from the update. If no user or message is found, returns (None, None).

    Example:
    - user, message = extract_user_and_message(update)
    """

    user = None
    message = None

    if update.message:
        user = getattr(update.message, "from_user", None)
        message = update.effective_message
    elif update.callback_query:
        user = getattr(update.callback_query, "from_user", None)
        message = getattr(update.callback_query, "message", None)

    return user, message


async def collect_phone_number(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if Phone# in DB and adds it to appropriate UserID"""
    logger_data_collector.debug({inspect.currentframe().f_code.co_name})
    user = update.effective_user
    phone_number = update.message.contact.phone_number

    # Check if PhoneNumber already in Database
    if tldb.get_user_data(user.id)[4] is None:
        tldb.insert_user_phone_number(user.id, phone_number)
    else:
        await update.message.reply_text("Phone number already in Database")


async def user_status(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Keeps track of users interacting with the app or blocking it and updates flag in DB"""
    logger_data_collector.info({inspect.currentframe().f_code.co_name})
    logger_data_collector.info(
        "update.my_chat_member.new_chat_member.status: {}".format(
            update.my_chat_member.new_chat_member.status
        )
    )
