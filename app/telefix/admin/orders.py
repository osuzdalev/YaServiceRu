from loguru import logger

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from telefix.common import helpers
from telefix.database import utils as tgdb


async def orders(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends message with all the unassigned and incomplete orders"""
    logger_orders.info(f" ")

    if helpers.clearance_center(update.effective_user.id):
        open_orders = tgdb.get_open_orders()
        assigned_orders = tgdb.get_assigned_orders()

        text = "Open Orders:\n\n"
        for i in range(len(open_orders)):
            text += "#" + str(open_orders[i][0]) + "\n"

        text += "\nAssigned Orders\n\n"
        for i in range(len(assigned_orders)):
            text += "#" + str(assigned_orders[i][0]) + "\n"

        await update.effective_message.reply_text(text)
    else:
        await update.effective_message.reply_text("Not allowed to use this user")


orders_handler = CommandHandler("orders", orders)
