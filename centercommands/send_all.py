"""NOT A SPAM"""

from configparser import ConfigParser
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler

from background import helpers, telegram_database_utils as tldb


logger_send_all = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to ALL Users"""
    logger_send_all.info("send_all()")
