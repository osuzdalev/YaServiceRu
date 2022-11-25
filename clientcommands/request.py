from configparser import ConfigParser
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
from telegram.ext import ContextTypes, ConversationHandler

from background import helpers, telegram_database as tldb


logger_req = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def request(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Checks if Customer's PhoneNumber is in Database before sending request to Customer Service
    if not asks for contact details permission and then sends a CONTACT message to bot"""
    logger_req.info("request()")

    try:
        phone_number = tldb.get_customer_data(update.effective_user.id)[-1]
        await reach_customer_service(update, _, phone_number)
    except (TypeError, AttributeError) as e:
        logger_req.info("customer phone number not in database")
        contact_button = KeyboardButton(text="send_contact", request_contact=True)
        contact_keyboard = [[contact_button]]
        reply_markup = ReplyKeyboardMarkup(contact_keyboard, one_time_keyboard=True)

        await update.message.reply_text(text="Contacting customer service, please share your contact details",
                                        reply_markup=reply_markup)


async def reach_customer_service(update: Update, context: ContextTypes.DEFAULT_TYPE, phone_number: int = None) -> None:
    """Stuff"""
    logger_req.info("reach_customer_service()")
    user = update.message.from_user
    user_data = [user.id, user.name, user.first_name, user.last_name]

    # Check if PhoneNumber already in Database
    if phone_number is None:
        phone_number = update.message.contact.phone_number

    tldb.insert_customer_phone_number(user.id, phone_number)

    try:
        device_context = context.user_data["Device_Context"]
    except KeyError:
        logger_req.info("Empty device_context")
        device_context = {"Device_OS_Brand": '', "Device": '', "Part": '', "Problem": ''}

    tldb.insert_new_order(user.id, device_context)
    OrderID = tldb.get_customer_last_OrderID(user.id)

    order_message_str = helpers.get_order_message_str(OrderID, user_data, device_context, phone_number)

    await context.bot.sendMessage(constants.get("ID", "FR"), order_message_str)

    await update.message.reply_text("Customer service will contact you", reply_markup=ReplyKeyboardRemove())
