from configparser import ConfigParser
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import ContextTypes, CommandHandler

from background import helpers, telegram_database as tldb


logger_req = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if Customer's PhoneNumber is in Database before sending request to Customer Service
        if not asks for contact details permission and then sends a CONTACT message to bot"""
    logger_req.info("request()")
    user = update.message.from_user
    user_data = [user.id, user.name, user.first_name, user.last_name]

    try:
        device_context = context.user_data["Device_Context"]
    except KeyError:
        logger_req.info("Empty device_context")
        device_context = {"Device_OS_Brand": None, "Device": None, "Part": None, "Problem": None}

    tldb.insert_new_order(user.id, device_context)

    OrderID = tldb.get_customer_last_OrderID(user.id)
    order_message_str = helpers.get_order_message_str(OrderID, user_data, device_context)

    await context.bot.sendMessage(constants.get("ID", "FR"), order_message_str)
    await update.message.reply_text("Customer service will contact you", reply_markup=ReplyKeyboardRemove())

request_handler = CommandHandler("request", request)
