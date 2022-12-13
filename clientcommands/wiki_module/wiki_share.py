import logging
from uuid import uuid4
from typing import Union

from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler, InlineQueryHandler

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
    # ============================================= DEVICES_PERIPHERY ==================================================
    # ----------------------------------------------- NO_SOUND ---------------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Devices_Periphery"]["No_Sound"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Devices_Periphery"]["No_Sound"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Devices_Periphery"]["No_Sound"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Devices_Periphery"]["No_Sound"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # ============================================= INSTALLATION_RECOVERY ==============================================
    # -------------------------------------- MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS --------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Installation_Recovery"][
        "Missing_Disk_Partitions_When_Installing_OS"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Installation_Recovery"][
                    "Missing_Disk_Partitions_When_Installing_OS"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Installation_Recovery"][
                            "Missing_Disk_Partitions_When_Installing_OS"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Installation_Recovery"][
                        "Missing_Disk_Partitions_When_Installing_OS"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # ============================================== NETWORK_INTERNET ==================================================
    # -------------------------------------------- NO_AVAILABLE_WIFI ---------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Available_Wifi"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Available_Wifi"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Available_Wifi"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Available_Wifi"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # -------------------------------------------- NO_INTERNET_CONNECTION ----------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Internet_Connection"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Internet_Connection"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Internet_Connection"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Network_Internet"]["No_Internet_Connection"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # ============================================= SAVING_DATA ====================================================
    # --------------------------------------------- REMOVING_TEMP_FILES ------------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Saving_Data"]["Removing_Temp_Files"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Saving_Data"]["Removing_Temp_Files"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(WIKI_DATA_DICT["Windows"]["Computer"]["Saving_Data"]["Removing_Temp_Files"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Saving_Data"]["Removing_Temp_Files"]["Text"],
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
    # ============================================= UPDATE_DRIVER ======================================================
    # --------------------------------------------- DRIVER_INSTALLATION_UPDATE -----------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Driver_Installation_Update"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Driver_Installation_Update"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Driver_Installation_Update"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Driver_Installation_Update"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # --------------------------------------------- UPDATE_WINDOWS_10_11 -----------------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Update_Windows_10_11"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Update_Windows_10_11"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Update_Windows_10_11"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Update_Windows_10_11"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]
    # --------------------------------------------- TURN_OFF_AUTOMATIC_UPDATES -----------------------------------------
    elif query_text == WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Turn_Off_Automatic_Updates"]["0_EN"]:
        results = [
            InlineQueryResultArticle(
                id=str(uuid4()),
                title=WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Turn_Off_Automatic_Updates"]["0_EN"],
                input_message_content=InputTextMessageContent(
                    get_answer_path(
                        WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Turn_Off_Automatic_Updates"]["0_EN"])
                    + WIKI_DATA_DICT["Windows"]["Computer"]["Update_Driver"]["Turn_Off_Automatic_Updates"]["Text"],
                    parse_mode=ParseMode.MARKDOWN)
            )
        ]

    await update.inline_query.answer(results)
    return ConversationHandler.END

share_inline_query_handler = InlineQueryHandler(share)
