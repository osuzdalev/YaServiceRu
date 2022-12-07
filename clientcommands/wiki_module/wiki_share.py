import logging
from uuid import uuid4
from typing import Union

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from clientcommands.wiki_module.wiki_json_utils import WIKI_DATA_DICT, get_answer_path

logger_wiki_share = logging.getLogger(__name__)


async def share(update: Update, _: ContextTypes.DEFAULT_TYPE) -> Union[int, None]:
    """Handle the inline query. This is run when you type: @YaServiceRuBot <query>"""
    logger_wiki_share.info("share()")
    query_text = update.inline_query.query

    results = []
    if query_text == "":
        return

    # ############################################# WINDOWS ############################################################
    # ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ COMPUTER ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
    # ============================================= BIOS ===============================================================
    # -------------------------------------- CHANGE LOADING PRIORITY ---------------------------------------------------
    if query_text == WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # ============================================= SLOWING_BUGGING ====================================================
    # --------------------------------------------- BOOTING ------------------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # --------------------------------------------- HARD DISK SSD ------------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # --------------------------------------------- HEATING ------------------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]

    await update.inline_query.answer(results)
    return ConversationHandler.END
