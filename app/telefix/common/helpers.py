import datetime
import inspect
import logging
from typing import Tuple

from telegram import Update
from telegram.ext import ContextTypes
import tiktoken

from telefix.database import utils as tgdb

logger_helpers = logging.getLogger(__name__)


def get_timestamp_str() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def check_order_id_exists(
    update: Update, _: ContextTypes.DEFAULT_TYPE, order_id: int, db_auth: dict
) -> Tuple:
    """Checks if given order exists"""
    logger_helpers.info(f"{inspect.currentframe().f_code.co_name}")
    order = tgdb.get_order_data(order_id, db_auth)
    if order is not None:
        return True, order
    else:
        await update.effective_message.reply_text("Order does not exist")
        return False, None


def clearance_contractor(user_id: int, db_auth: dict) -> bool:
    """Verify if the user sending the user is a Contractor and has clearance"""
    logger_helpers.info(f"{inspect.currentframe().f_code.co_name}")
    all_contractor_id = tgdb.get_all_contractor_id(db_auth)
    return user_id in all_contractor_id


def clearance_center(user_id: int, tg_id_dev) -> bool:
    """Verify if the user sending the user is an owner of a CenterID and has clearance"""
    logger_helpers.info(f"{inspect.currentframe().f_code.co_name}")
    return user_id == int(tg_id_dev)


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    logger_helpers.info(f"{inspect.currentframe().f_code.co_name}")

    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
