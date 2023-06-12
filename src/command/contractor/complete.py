import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from src.common import helpers
from src.common.database import utils as tldb

logger_assign = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def complete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Marks and Order as Completed with a timestamp.
    Can only be used by CenterID or ContractorID assigned the Order"""
    logger_assign.info("complete()")
    OrderID = int(context.args[0])
    user_id = update.effective_user.id
    CenterID = constants.get("ID", "OLEG_RU")

    if not helpers.clearance_contractor(user_id):
        await update.effective_message.reply_text("You cannot use this command")
        return

    check_order, order_data = await helpers.check_OrderID_exists(
        update, context, OrderID
    )

    if check_order and (user_id == order_data[2] or user_id == CenterID):
        tldb.update_order_Complete(OrderID, helpers.get_timestamp_str())
    elif check_order and (user_id != order_data[2] or user_id != CenterID):
        await update.effective_message.reply_text("Not your Order")


complete_handler = CommandHandler("complete", complete)
