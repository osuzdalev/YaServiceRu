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

from clientcommands.wiki_module import wiki_share
from clientcommands.wiki_module.wiki_data import DATA_DICT

logger_wiki = logging.getLogger(__name__)


# All States for /wiki_module Conversation
class States(Enum):
    OS = 1
    W_DEVICE = 2
    W_C_CATEGORY = 3
    W_C_BIOS_PROBLEMS = 4
    W_C_BIOS_Change_Loading_Priority = 5
    W_C_SlowingBugging_PROBLEMS = 6
    W_C_SlowingBugging_Booting = 7
    A_DEVICE = 8


# Basic callback_data
class Navigation(Enum):
    CANCEL = 0
    BACK = 1
    OTHER = 2


BUTTON_TEXT_CANCEL = "CANCEL"
BUTTON_TEXT_BACK = "<< BACK"
BUTTON_TEXT_OTHER = "Другие/Иное"
BUTTON_TEXT_SHARE = "SHARE 🔗"


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Union[States, int]:
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
        [InlineKeyboardButton(text="Apple", callback_data=DATA_DICT["Apple"]["Callback_Data"]),
         InlineKeyboardButton(text="Windows", callback_data=DATA_DICT["Windows"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a Brand/OS", reply_markup=inline_markup)

    return States.OS.value


async def wiki_back(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("wiki_module()")
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Apple", callback_data=DATA_DICT["Apple"]["Callback_Data"]),
         InlineKeyboardButton(text="Windows", callback_data=DATA_DICT["Windows"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a Brand/OS", reply_markup=inline_markup)

    return States.OS.value


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


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `wiki_module` does but not as new message"""
    logger_wiki.info("apple()")
    context.user_data["Device_Context"]["OS"] = "Apple"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Computer", callback_data=DATA_DICT["Windows"]["Computer"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return States.A_DEVICE.value


async def windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """OS.Windows"""
    logger_wiki.info("windows()")
    context.user_data["Device_Context"]["OS"] = "Windows"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Computer", callback_data=DATA_DICT["Windows"]["Computer"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return States.W_DEVICE.value


async def windows_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("windows_computer()")
    W_COMPUTER_DICT = DATA_DICT["Windows"]["Computer"]
    context.user_data["Device_Context"]["Device"] = W_COMPUTER_DICT["Device_Title"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=W_COMPUTER_DICT["Slowing_Bugging"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Slowing_Bugging"]["Callback_Data"]),
         InlineKeyboardButton(text=W_COMPUTER_DICT["Update_Driver"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Update_Driver"]["Callback_Data"])],
        [InlineKeyboardButton(text=W_COMPUTER_DICT["Devices_Periphery"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Devices_Periphery"]["Callback_Data"]),
         InlineKeyboardButton(text=W_COMPUTER_DICT["Switching_Charging"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Switching_Charging"]["Callback_Data"])],
        [InlineKeyboardButton(text=W_COMPUTER_DICT["Network_Internet"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Network_Internet"]["Callback_Data"]),
         InlineKeyboardButton(text=W_COMPUTER_DICT["Installation_Recovery"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Installation_Recovery"]["Callback_Data"])],
        [InlineKeyboardButton(text=W_COMPUTER_DICT["Display_Graphics"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Display_Graphics"]["Callback_Data"]),
         InlineKeyboardButton(text=W_COMPUTER_DICT["System_Settings"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["System_Settings"]["Callback_Data"])],
        [InlineKeyboardButton(text=W_COMPUTER_DICT["Saving_Data"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["Saving_Data"]["Callback_Data"]),
         InlineKeyboardButton(text=W_COMPUTER_DICT["BIOS"]["Category_Title_RU"],
                              callback_data=W_COMPUTER_DICT["BIOS"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=Navigation.OTHER.value)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a category", reply_markup=inline_markup)

    return States.W_C_CATEGORY.value


async def windows_computer_bios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """STUFF"""
    logger_wiki.info("windows_computer_bios()")
    BIOS_DICT = DATA_DICT["Windows"]["Computer"]["BIOS"]
    context.user_data["Device_Context"]["Category"] = BIOS_DICT["Category_Title_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BIOS_DICT["Change_Loading_Priority"]["Problem_Title_RU"],
                              callback_data=BIOS_DICT["Change_Loading_Priority"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=Navigation.OTHER.value)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return States.W_C_BIOS_PROBLEMS.value


async def windows_computer_bios_changeLoadingPriority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """STUFF"""
    logger_wiki.info("windows_computer_bios_ChangeLoadingPriority()")
    CHANGE_LOADING_PRIORITY_DICT = DATA_DICT["Windows"]["Computer"]["BIOS"][
        "Change_Loading_Priority"]
    context.user_data["Device_Context"]["Problem"] = CHANGE_LOADING_PRIORITY_DICT["Problem_Title_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=CHANGE_LOADING_PRIORITY_DICT["Problem_Title_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=CHANGE_LOADING_PRIORITY_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return States.W_C_BIOS_Change_Loading_Priority.value


async def windows_computer_slowingBugging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging()")
    SLOWING_BUGGING_DICT = DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]
    context.user_data["Device_Context"]["Category"] = SLOWING_BUGGING_DICT["Category_Title_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SLOWING_BUGGING_DICT["Booting"]["Problem_Title_RU"],
                              callback_data=SLOWING_BUGGING_DICT["Booting"]["Callback_Data"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=Navigation.OTHER.value)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return States.W_C_SlowingBugging_PROBLEMS.value


async def windows_computer_slowingBugging_Booting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """STUFF"""
    logger_wiki.info("windows_computer_slowingBugging_Booting()")
    BOOTING_DICT = DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"][
        "Booting"]
    context.user_data["Device_Context"]["Problem"] = BOOTING_DICT["Problem_Title_RU"]
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=BOOTING_DICT["Problem_Title_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=Navigation.BACK.value),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=Navigation.CANCEL.value)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=BOOTING_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return States.W_C_SlowingBugging_Booting.value


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("wiki", wiki)],
    states={
        States.OS.value: [
            CallbackQueryHandler(apple, "^" + str(DATA_DICT["Apple"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(windows, "^" + str(DATA_DICT["Windows"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_DEVICE.value: [
            CallbackQueryHandler(wiki_back, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(windows_computer, "^" + str(DATA_DICT["Windows"]["Computer"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_C_CATEGORY.value: [
            CallbackQueryHandler(windows, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(windows_computer_bios, "^" + str(DATA_DICT["Windows"]["Computer"]["BIOS"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(windows_computer_slowingBugging,
                                 "^" + str(DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_C_BIOS_PROBLEMS.value: [
            CallbackQueryHandler(windows_computer, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(windows_computer_bios_changeLoadingPriority,
                                 "^" + str(DATA_DICT["Windows"]["Computer"]["BIOS"]["Change_Loading_Priority"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_C_BIOS_Change_Loading_Priority.value: [
            CallbackQueryHandler(windows_computer_bios, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_C_SlowingBugging_PROBLEMS.value: [
            CallbackQueryHandler(windows_computer, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(windows_computer_slowingBugging_Booting,
                                 "^" + str(DATA_DICT["Windows"]["Computer"]["Slowing_Bugging"]["Booting"]["Callback_Data"]) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
        States.W_C_SlowingBugging_Booting.value: [
            CallbackQueryHandler(windows_computer_slowingBugging, "^" + str(Navigation.BACK.value) + "$"),
            CallbackQueryHandler(cancel_callback, "^" + str(Navigation.CANCEL.value) + "$")
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_command)],
    allow_reentry=True,
    conversation_timeout=15
)

share_inline_query_handler = InlineQueryHandler(wiki_share.share)
