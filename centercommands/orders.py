from configparser import ConfigParser
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler

from background import helpers, telegram_database_utils as tldb


logger_orders = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends message with all the unassigned and incomplete orders"""
    logger_orders.info("orders()")

    if helpers.clearance_Center(update.effective_user.id):
        open_orders = tldb.get_open_orders()
        assigned_orders = tldb.get_assigned_orders()

        text = "Open Orders:\n\n"
        for i in range(len(open_orders)):
            text += "#" + str(open_orders[i][0]) + "\n"

        text += "\nAssigned Orders\n\n"
        for i in range(len(assigned_orders)):
            text += "#" + str(assigned_orders[i][0]) + "\n"

        await update.effective_message.reply_text(text)
    else:
        await update.effective_message.reply_text("Not allowed to use this command")


orders_handler = CommandHandler("orders", orders)
