import logging
from pprint import pformat

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from clientcommands.wiki_module.wiki_json_utils import WIKI_DATA_DICT

logger_wiki_apple_computer = logging.getLogger(__name__)

# Basic callback_data
CANCEL = "CANCEL"
BACK = "BACK"
OTHER = "OTHER"

# Omnipresent buttons
BUTTON_TEXT_CANCEL = "CANCEL"
BUTTON_TEXT_BACK = "<< BACK"
BUTTON_TEXT_OTHER = "Другие/Иное"
BUTTON_TEXT_SHARE = "SHARE 🔗"

APPLE_COMPUTER = WIKI_DATA_DICT["Apple"]["Computer"]


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt same text & keyboard as `wiki_module` does but not as new message"""
    logger_wiki_apple_computer.info("apple()")
    context.user_data["Device_Context"]["OS"] = WIKI_DATA_DICT["Apple"]["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

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


async def a_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stuff"""
    logger_wiki_apple_computer.info("a_computer()")
    context.user_data["Device_Context"]["Device"] = APPLE_COMPUTER["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=APPLE_COMPUTER["Slowing_Bugging"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Slowing_Bugging"]["0_EN"]),
         InlineKeyboardButton(text=APPLE_COMPUTER["Update_Driver"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Update_Driver"]["0_EN"])],
        [InlineKeyboardButton(text=APPLE_COMPUTER["Devices_Periphery"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Devices_Periphery"]["0_EN"]),
         InlineKeyboardButton(text=APPLE_COMPUTER["Switching_Charging"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Switching_Charging"]["0_EN"])],
        [InlineKeyboardButton(text=APPLE_COMPUTER["Network_Internet"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Network_Internet"]["0_EN"]),
         InlineKeyboardButton(text=APPLE_COMPUTER["Installation_Recovery"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Installation_Recovery"]["0_EN"])],
        [InlineKeyboardButton(text=APPLE_COMPUTER["Display_Graphics"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Display_Graphics"]["0_EN"]),
         InlineKeyboardButton(text=APPLE_COMPUTER["System_Settings"]["0_RU"],
                              callback_data=APPLE_COMPUTER["System_Settings"]["0_EN"])],
        [InlineKeyboardButton(text=APPLE_COMPUTER["Saving_Data"]["0_RU"],
                              callback_data=APPLE_COMPUTER["Saving_Data"]["0_EN"]),
         InlineKeyboardButton(text=APPLE_COMPUTER["BIOS"]["0_RU"],
                              callback_data=APPLE_COMPUTER["BIOS"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a category", reply_markup=inline_markup)

    print(APPLE_COMPUTER["0_EN"])
    return APPLE_COMPUTER["0_EN"]


async def a_c_InstallationRecovery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_apple_computer.info("a_c_InstallationRecovery()")
    INSTALLATION_RECOVERY_DICT = APPLE_COMPUTER["Installation_Recovery"]
    context.user_data["Device_Context"]["Category"] = INSTALLATION_RECOVERY_DICT["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=INSTALLATION_RECOVERY_DICT["Reset_CMOS_NVRAM"]["0_RU"],
                              callback_data=INSTALLATION_RECOVERY_DICT["Reset_CMOS_NVRAM"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return INSTALLATION_RECOVERY_DICT["0_EN"]


async def a_c_SavingData(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_apple_computer.info("a_c_SavingData()")
    SAVING_DATA_DICT = APPLE_COMPUTER["Saving_Data"]
    context.user_data["Device_Context"]["Category"] = SAVING_DATA_DICT["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SAVING_DATA_DICT["Reset_CMOS_NVRAM"]["0_RU"],
                              callback_data=SAVING_DATA_DICT["Reset_CMOS_NVRAM"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return SAVING_DATA_DICT["0_EN"]


async def a_c_SlowingBugging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_apple_computer.info("a_c_SlowingBugging()")
    SLOWING_BUGGING_DICT = APPLE_COMPUTER["Slowing_Bugging"]
    context.user_data["Device_Context"]["Category"] = SLOWING_BUGGING_DICT["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SLOWING_BUGGING_DICT["Reset_CMOS_NVRAM"]["0_RU"],
                              callback_data=SLOWING_BUGGING_DICT["Reset_CMOS_NVRAM"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    print('SLOWING_BUGGING_DICT["0_EN"]', SLOWING_BUGGING_DICT["0_EN"])
    return SLOWING_BUGGING_DICT["0_EN"]


async def a_c_SlowingBugging_ResetCmosNvram(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_apple_computer.info("a_c_SlowingBugging_ResetCmosNvram()")
    RESET_CMOS_NVRAM_DICT = APPLE_COMPUTER["Slowing_Bugging"]["Reset_CMOS_NVRAM"]
    context.user_data["Device_Context"]["Problem"] = RESET_CMOS_NVRAM_DICT["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=RESET_CMOS_NVRAM_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=RESET_CMOS_NVRAM_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return RESET_CMOS_NVRAM_DICT["0_EN"]


async def a_c_SystemSettings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_apple_computer.info("a_c_SystemSettings()")
    SYSTEM_SETTINGS_DICT = APPLE_COMPUTER["System_Settings"]
    context.user_data["Device_Context"]["Category"] = SYSTEM_SETTINGS_DICT["0_RU"]
    logger_wiki_apple_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SYSTEM_SETTINGS_DICT["Reset_CMOS_NVRAM"]["0_RU"],
                              callback_data=SYSTEM_SETTINGS_DICT["Reset_CMOS_NVRAM"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return SYSTEM_SETTINGS_DICT["0_EN"]
