import datetime
import logging
import os
from typing import Tuple, List, Any

from telegram import Update
from telegram.ext import ContextTypes

from src import common as tldb
from dotenv import load_dotenv

logger_helpers = logging.getLogger(__name__)

load_dotenv()


def get_order_message_str(
    order_id: int, user_data: Any, device_context: Any, phone_number: int = None
) -> str:
    """Creates a nice string with all the relevant database of an Order to be sent as a message to Contractor"""
    logger_helpers.info("get_order_message_str()")
    user_info = ""
    if isinstance(user_data, List):
        user_info = (
            user_data[1]
            + "\n"
            + user_data[2]
            + "\n"
            + user_data[3]
            + "\n"
            + str(phone_number)
            + "\n"
            + "id:"
            + str(user_data[0])
        )
    elif isinstance(user_data, Tuple):
        user_info = (
            "@"
            + user_data[1]
            + "\n"
            + user_data[2]
            + "\n"
            + user_data[3]
            + "\n"
            + str(phone_number)
            + "\n"
            + "id:"
            + str(user_data[0])
        )

    device_info = "\n".join(device_context)
    logger_helpers.debug(f"device_context: {device_context}")

    order_message_str = "\n\n".join(
        [
            "Customer service required",
            f"Order# {str(order_id)}",
            user_info,
            device_info,
        ]
    )

    return order_message_str


def get_timestamp_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def check_order_id_exists(
    update: Update, _: ContextTypes.DEFAULT_TYPE, order_id: int
) -> Tuple:
    """Checks if given order exists"""
    logger_helpers.info("check_order_id_exists()")
    order = tldb.get_order_data(order_id)
    if order is not None:
        return True, order
    else:
        await update.effective_message.reply_text("Order does not exist")
        return False, None


def clearance_contractor(user_id: int) -> bool:
    """Verify if the user sending the command is a Contractor and has clearance"""
    logger_helpers.info("clearance_contractor()")
    all_contractor_id = tldb.get_all_contractor_id()
    return user_id in all_contractor_id


def clearance_center(user_id: int) -> bool:
    """Verify if the user sending the command is an owner of a CenterID and has clearance"""
    logger_helpers.info("check_CenterID()")
    return user_id == int(os.getenv("ID_DEV_MAIN"))
