from enum import Enum
import logging
from pprint import pformat
from typing import Union

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    InlineQueryHandler
)
from telegram.constants import ParseMode

from clientcommands.wiki_module.wiki_json_utils import WIKI_DATA_DICT
from clientcommands.wiki_module import wiki_share


logger_wiki = logging.getLogger(__name__)


# Basic callback_data
CANCEL = "CANCEL"
BACK = "BACK"
OTHER = "OTHER"


BUTTON_TEXT_CANCEL = "CANCEL"
BUTTON_TEXT_BACK = "<< BACK"
BUTTON_TEXT_OTHER = "Другие/Иное"
BUTTON_TEXT_SHARE = "SHARE 🔗"


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[str, int]:
    """Customer command: Opens an Inline Menu to search for some information. As Buttons are pressed and going
    through the decision tree, the user_data 'device_context' is updated.
    This Conversation first needs to check the user 'in_conversation flag' before it can start, otherwise it will ask
    the customer to first close the previous one."""
    logger_wiki.info("wiki_module()")
    device_context = {"OS": '', "Device": '', "Category": '', "Problem": ''}
    context.user_data["Device_Context"] = device_context
    in_conversation = context.user_data['in_conversation']

    # Check if user already in Conversation
    if not (in_conversation == '' or in_conversation == 'wiki_module'):
        await update.message.reply_text("Please press /cancel\n"
                                        "or push the 'CANCEL' button in the previous menu before proceeding")
        return ConversationHandler.END
    context.user_data["in_conversation"] = "wiki_module"

    keyboard = [
        [InlineKeyboardButton(text=WIKI_DATA_DICT["Apple"]["0_RU"], callback_data=WIKI_DATA_DICT["Apple"]["0_EN"]),
         InlineKeyboardButton(text=WIKI_DATA_DICT["Windows"]["0_RU"], callback_data=WIKI_DATA_DICT["Windows"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a Brand/OS", reply_markup=inline_markup)

    return WIKI_DATA_DICT["0_EN"]


async def wiki_back(update: Update, _: ContextTypes.DEFAULT_TYPE) -> str:
    """Stuff"""
    logger_wiki.info("wiki_module()")
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=WIKI_DATA_DICT["Apple"]["0_EN"], callback_data=WIKI_DATA_DICT["Apple"]["0_EN"]),
         InlineKeyboardButton(text=WIKI_DATA_DICT["Windows"]["0_RU"], callback_data=WIKI_DATA_DICT["Windows"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a Brand/OS", reply_markup=inline_markup)

    return WIKI_DATA_DICT["0_EN"]


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger_wiki.info("cancel_callback()")
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    context.user_data["in_conversation"] = ""
    return ConversationHandler.END


async def cancel_command(_: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger_wiki.info("cancel_command()")
    context.user_data["in_conversation"] = ""
    return ConversationHandler.END


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt same text & keyboard as `wiki_module` does but not as new message"""
    logger_wiki.info("apple()")
    context.user_data["Device_Context"]["OS"] = WIKI_DATA_DICT["Apple"]["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text=WIKI_DATA_DICT["Apple"]["Computer"]["0_RU"],
                              callback_data=WIKI_DATA_DICT["Apple"]["Computer"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return WIKI_DATA_DICT["Apple"]["0_EN"]


async def windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """OS.Windows"""
    logger_wiki.info("windows()")
    context.user_data["Device_Context"]["OS"] = WIKI_DATA_DICT["Windows"]["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text=WIKI_DATA_DICT["Windows"]["Computer"]["0_RU"],
                              callback_data=WIKI_DATA_DICT["Windows"]["Computer"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return WIKI_DATA_DICT["Windows"]["0_EN"]


async def windows_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stuff"""
    logger_wiki.info("windows_computer()")
    COMPUTER_DICT = WIKI_DATA_DICT["Windows"]["Computer"]
    context.user_data["Device_Context"]["Device"] = COMPUTER_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=COMPUTER_DICT["Slowing_Bugging"]["0_RU"],
                              callback_data=COMPUTER_DICT["Slowing_Bugging"]["0_EN"]),
         InlineKeyboardButton(text=COMPUTER_DICT["Update_Driver"]["0_RU"],
                              callback_data=COMPUTER_DICT["Update_Driver"]["0_EN"])],
        [InlineKeyboardButton(text=COMPUTER_DICT["Devices_Periphery"]["0_RU"],
                              callback_data=COMPUTER_DICT["Devices_Periphery"]["0_EN"]),
         InlineKeyboardButton(text=COMPUTER_DICT["Switching_Charging"]["0_RU"],
                              callback_data=COMPUTER_DICT["Switching_Charging"]["0_EN"])],
        [InlineKeyboardButton(text=COMPUTER_DICT["Network_Internet"]["0_RU"],
                              callback_data=COMPUTER_DICT["Network_Internet"]["0_EN"]),
         InlineKeyboardButton(text=COMPUTER_DICT["Installation_Recovery"]["0_RU"],
                              callback_data=COMPUTER_DICT["Installation_Recovery"]["0_EN"])],
        [InlineKeyboardButton(text=COMPUTER_DICT["Display_Graphics"]["0_RU"],
                              callback_data=COMPUTER_DICT["Display_Graphics"]["0_EN"]),
         InlineKeyboardButton(text=COMPUTER_DICT["System_Settings"]["0_RU"],
                              callback_data=COMPUTER_DICT["System_Settings"]["0_EN"])],
        [InlineKeyboardButton(text=COMPUTER_DICT["Saving_Data"]["0_RU"],
                              callback_data=COMPUTER_DICT["Saving_Data"]["0_EN"]),
         InlineKeyboardButton(text=COMPUTER_DICT["BIOS"]["0_RU"],
                              callback_data=COMPUTER_DICT["BIOS"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a category", reply_markup=inline_markup)

    return COMPUTER_DICT["0_EN"]


async def windows_computer_bios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_bios()")
    BIOS_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]
    context.user_data["Device_Context"]["Category"] = BIOS_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BIOS_DICT["Change_Loading_Priority"]["0_RU"],
                              callback_data=BIOS_DICT["Change_Loading_Priority"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return BIOS_DICT["0_EN"]


async def windows_computer_bios_changeLoadingPriority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_bios_ChangeLoadingPriority()")
    CHANGE_LOADING_PRIORITY_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"][
        "Change_Loading_Priority"]
    context.user_data["Device_Context"]["Problem"] = CHANGE_LOADING_PRIORITY_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=CHANGE_LOADING_PRIORITY_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=CHANGE_LOADING_PRIORITY_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return CHANGE_LOADING_PRIORITY_DICT["0_EN"]


async def windows_computer_slowingBugging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging()")
    SLOWING_BUGGING_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]
    context.user_data["Device_Context"]["Category"] = SLOWING_BUGGING_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SLOWING_BUGGING_DICT["Booting"]["0_RU"],
                              callback_data=SLOWING_BUGGING_DICT["Booting"]["0_EN"]),
         InlineKeyboardButton(text=SLOWING_BUGGING_DICT["Hard_Disk_SSD"]["0_RU"],
                              callback_data=SLOWING_BUGGING_DICT["Hard_Disk_SSD"]["0_EN"])],
        [InlineKeyboardButton(text=SLOWING_BUGGING_DICT["Heating"]["0_RU"],
                              callback_data=SLOWING_BUGGING_DICT["Heating"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return SLOWING_BUGGING_DICT["0_EN"]


async def windows_computer_slowingBugging_Booting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging_Booting()")
    BOOTING_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]
    context.user_data["Device_Context"]["Problem"] = BOOTING_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=BOOTING_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=BOOTING_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return BOOTING_DICT["0_EN"]


async def windows_computer_slowingBugging_hardDiskSSD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging_Booting()")
    HARD_DISK_SSD_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]
    context.user_data["Device_Context"]["Problem"] = HARD_DISK_SSD_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=HARD_DISK_SSD_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=HARD_DISK_SSD_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return HARD_DISK_SSD_DICT["0_EN"]


async def windows_computer_slowingBugging_Heating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging_Heating()")
    HEATING_DICT = WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]
    context.user_data["Device_Context"]["Problem"] = HEATING_DICT["0_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=HEATING_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=HEATING_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return HEATING_DICT["0_EN"]


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("wiki", wiki)],
    states={
        WIKI_DATA_DICT["0_EN"]: [
            CallbackQueryHandler(apple, WIKI_DATA_DICT["Apple"]["0_EN"]),
            CallbackQueryHandler(windows, WIKI_DATA_DICT["Windows"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["0_EN"]: [
            CallbackQueryHandler(wiki_back,  BACK),
            CallbackQueryHandler(windows_computer, WIKI_DATA_DICT["Windows"]["Computer"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["0_EN"]: [
            CallbackQueryHandler(windows,  BACK),
            CallbackQueryHandler(windows_computer_bios, WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["0_EN"]),
            CallbackQueryHandler(windows_computer_slowingBugging,
                                 WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["0_EN"]: [
            CallbackQueryHandler(windows_computer,  BACK),
            CallbackQueryHandler(windows_computer_bios_changeLoadingPriority,
                                 WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["0_EN"]: [
            CallbackQueryHandler(windows_computer_bios,  BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["0_EN"]: [
            CallbackQueryHandler(windows_computer,  BACK),
            CallbackQueryHandler(windows_computer_slowingBugging_Booting,
                                 WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"][
                                               "0_EN"]),
            CallbackQueryHandler(windows_computer_slowingBugging_hardDiskSSD,
                                 WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"][
                                               "0_EN"]),
            CallbackQueryHandler(windows_computer_slowingBugging_Heating,
                                 WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"][
                                               "0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["0_EN"]: [
            CallbackQueryHandler(windows_computer_slowingBugging,  BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WIKI_DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Heating"]["0_EN"]: [
            CallbackQueryHandler(windows_computer_slowingBugging,  BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_command)],
    allow_reentry=True,
    conversation_timeout=15
)

share_inline_query_handler = InlineQueryHandler(wiki_share.share)
