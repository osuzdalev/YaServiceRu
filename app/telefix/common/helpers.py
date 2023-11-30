import datetime
from loguru import logger
from typing import Tuple

from telegram import Update
from telegram.ext import ContextTypes
import tiktoken

from ..database import utils as tgdb


def get_timestamp_str(dt=None) -> str:
    dt = dt or datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


async def exists_order_id(
    update: Update, _: ContextTypes.DEFAULT_TYPE, order_id: int, db_auth: dict
) -> Tuple:
    """Checks if given order exists"""
    logger.info(f" ")
    order = tgdb.get_order_data(order_id, db_auth)
    if order is None:
        await update.effective_message.reply_text("Order does not exist")
        return False, None
    else:
        return True, order


def clearance_contractor(user_id: int, db_auth: dict) -> bool:
    """Verify if the user sending the user is a Contractor and has clearance"""
    logger.info(f" ")
    all_contractor_id = tgdb.get_all_contractor_id(db_auth)
    return user_id in all_contractor_id


def clearance_center(user_id: int, tg_id_dev) -> bool:
    """Verify if the user sending the user is an owner of a CenterID and has clearance"""
    logger.info(f" ")
    return user_id == int(tg_id_dev)


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    logger.info(f" ")
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
