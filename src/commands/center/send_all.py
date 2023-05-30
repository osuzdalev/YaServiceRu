"""NOT A SPAM"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger_send_all = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to ALL Users"""
    logger_send_all.info("send_all()")
