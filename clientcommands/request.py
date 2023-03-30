import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from resources.constants_loader import load_constants
from background import helpers, telegram_database_utils as tldb
from markups.default import default_client_markup


logger_req = logging.getLogger(__name__)
constants = load_constants()


async def request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """sends a request (a message with all relevant/context information) to Customer Service"""
    logger_req.info("request()")
    user = update.message.from_user
    user_data = [user.id, user.name, user.first_name, user.last_name]

    device_context = context.user_data.get("Device_Context", [])

    tldb.insert_new_order(user.id, device_context)

    OrderID = tldb.get_customer_last_OrderID(user.id)
    order_message_str = helpers.get_order_message_str(OrderID, user_data, device_context)

    await context.bot.sendMessage(constants.get("ID", "DENIS"), order_message_str)
    await context.bot.sendMessage(constants.get("ID", "OLEG_RU"), order_message_str)
    await update.message.reply_text("Служба поддержки свяжется с вами.", reply_markup=default_client_markup)

request_handler = CommandHandler("request", request)
request_replykeyboard_handler = MessageHandler(filters.Regex(r"^(🤓Специалист)$"), request)
