from configparser import ConfigParser
import datetime
import logging
from typing import Tuple, List, Dict, Any

from telegram import Update
from telegram.ext import ContextTypes

import background.telegram_database_utils as tldb

logger_helpers = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


def get_order_message_str(OrderID: int, user_data: Any, device_context: Any, phone_number: int = None) -> str:
    """Creates a nice string with all the relevant data of an Order to be sent as a message to Contractor"""
    logger_helpers.info("get_order_message_str()")
    user_info = ""
    if isinstance(user_data, List):
        user_info = user_data[1] + '\n' + \
                    user_data[2] + '\n' + user_data[3] + '\n' + str(phone_number) + '\n' + \
                    "id:" + str(user_data[0])
    elif isinstance(user_data, Tuple):
        user_info = '@' + user_data[1] + '\n' + \
                    user_data[2] + '\n' + user_data[3] + '\n' + str(phone_number) + '\n' + \
                    "id:" + str(user_data[0])

    device_info = ""
    logger_helpers.debug("device_context: {}".format(device_context))
    if isinstance(device_context, Dict):
        if device_context == {"OS": None, "Device": None, "Category": None, "Problem": None}:
            device_info = "OS: " + "-" + '\n' + \
                          "Device: " + "-" + '\n' + \
                          "Category: " + "-" + '\n' + \
                          "Problem: " + "-"
        else:
            device_info = "OS: " + device_context["OS"] + '\n' + \
                          "Device: " + device_context["Device"] + '\n' + \
                          "Category: " + device_context["Category"] + '\n' + \
                          "Problem: " + device_context["Problem"]
    elif isinstance(device_context, Tuple):
        device_info = "OS: " + device_context[4] + '\n' + \
                      "Device: " + device_context[5] + '\n' + \
                      "Category: " + device_context[6] + '\n' + \
                      "Problem: " + device_context[7]

    order_message_str = "\n\n".join(["Customer service required", "Order# {}".format(str(OrderID)), user_info, device_info])

    return order_message_str


def get_timestamp_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def check_OrderID_exists(update: Update, _: ContextTypes.DEFAULT_TYPE, OrderID: int) -> Tuple:
    """Checks if Order given exists"""
    logger_helpers.info("check_OrderID_exists()")
    order = tldb.get_order_data(OrderID)
    if order is not None:
        return True, order
    else:
        await update.effective_message.reply_text("Order does not exist")
        return False, None


def clearance_Contractor(user_id: int) -> bool:
    """Verify if the user sending the command is a Contractor and has clearance"""
    logger_helpers.info("clearance_Contractor()")
    ContractorIDs = tldb.get_all_ContractorID()
    return True if user_id in ContractorIDs else False


def clearance_Center(user_id: int) -> bool:
    """Verify if the user sending the command is an owner of a CenterID and has clearance"""
    logger_helpers.info("check_CenterID()")
    return True if user_id == int(constants.get("ID", "MAIN")) else False
