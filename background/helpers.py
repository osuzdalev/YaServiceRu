from configparser import ConfigParser
import datetime
import logging

from telegram import Update
from telegram.ext import ContextTypes

import background.telegram_database as tldb

logger_helpers = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")


def get_order_message_str(OrderID: int, user_data: any, device_context: any, phone_number: int = None) -> str:
    """Creates a nice string with all the relevant data of an Order to be sent as a message to Contractor"""
    logger_helpers.info("get_order_message_str()")
    user_info = ""
    if type(user_data) == list:
        user_info = user_data[1] + '\n' + \
                    user_data[2] + '\n' + user_data[3] + '\n' + str(phone_number) + '\n' + \
                    "id:" + str(user_data[0])
    elif type(user_data) == tuple:
        user_info = '@' + user_data[1] + '\n' + \
                    user_data[2] + '\n' + user_data[3] + '\n' + str(phone_number) + '\n' + \
                    "id:" + str(user_data[0])

    device_info = ""
    logger_helpers.info("device_context: {}".format(device_context))
    if type(device_context) == dict:
        if device_context == {"Device_OS_Brand": None, "Device": None, "Part": None, "Problem": None}:
            device_info = "Device_OS: " + "-" + '\n' + \
                          "Device: " + "-" + '\n' + \
                          "Part: " + "-" + '\n' + \
                          "Problem: " + "-"
        else:
            device_info = "Device_OS: " + device_context["Device_OS_Brand"] + '\n' + \
                          "Device: " + device_context["Device"] + '\n' + \
                          "Part: " + device_context["Part"] + '\n' + \
                          "Problem: " + device_context["Problem"]
    elif type(device_context) == tuple:
        device_info = "Device_OS: " + device_context[4] + '\n' + \
                      "Device: " + device_context[5] + '\n' + \
                      "Part: " + device_context[6] + '\n' + \
                      "Problem: " + device_context[7]

    order_message_str = "Customer service required\n\n" \
                        "Order# {}\n\n{}\n\n{}".format(str(OrderID), user_info, device_info)

    return order_message_str


def get_timestamp_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def check_OrderID_exists(update: Update, _: ContextTypes.DEFAULT_TYPE, OrderID: int) -> tuple:
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
