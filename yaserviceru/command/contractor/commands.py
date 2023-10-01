import logging

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from yaserviceru.common import helpers

logger_assign = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with all the available command for a Contractor"""
    logger_assign.info("command()")
    user_id = update.effective_user.id

    if not helpers.clearance_contractor(user_id) or not helpers.clearance_center(
        user_id
    ):
        await update.effective_message.reply_text("You cannot use this command")
        return

    text = (
        "Available Commands:\n\n"
        + "/assign # - assign an Order to another Contractor\n"
        + "/complete # - mark an Order as completed\n"
        + "/orders - show all the currently open Orders\n"
        + "/order # - get the details of an Order\n"
    )

    await update.effective_message.reply_text(text)


commands_handler = CommandHandler("command", commands)
