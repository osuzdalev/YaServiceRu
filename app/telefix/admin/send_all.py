"""NOT A SPAM"""

from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes

constants = ConfigParser()
constants.read("constants.ini")


async def send_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message to ALL Users"""
    logger_send_all.info("send_all()")
