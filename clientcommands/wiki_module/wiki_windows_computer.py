import logging
from pprint import pformat

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from clientcommands.wiki_module.wiki_json_utils import WIKI_DATA_DICT

logger_wiki_windows_computer = logging.getLogger(__name__)

# Basic callback_data
CANCEL = "CANCEL"
BACK = "BACK"
OTHER = "OTHER"

# Omnipresent buttons
BUTTON_TEXT_CANCEL = "CANCEL"
BUTTON_TEXT_BACK = "<< BACK"
BUTTON_TEXT_OTHER = "Другие/Иное"
BUTTON_TEXT_SHARE = "SHARE 🔗"

WINDOWS_COMPUTER = WIKI_DATA_DICT["Windows"]["Computer"]


async def windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """OS.Windows"""
    logger_wiki_windows_computer.info("windows()")
    context.user_data["Device_Context"]["OS"] = WIKI_DATA_DICT["Windows"]["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text=WINDOWS_COMPUTER["0_RU"],
                              callback_data=WINDOWS_COMPUTER["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return WIKI_DATA_DICT["Windows"]["0_EN"]


async def w_computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Stuff"""
    logger_wiki_windows_computer.info("w_computer()")
    COMPUTER_DICT = WINDOWS_COMPUTER
    context.user_data["Device_Context"]["Device"] = COMPUTER_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

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


async def w_c_BIOS(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_BIOS()")
    BIOS_DICT = WINDOWS_COMPUTER["BIOS"]
    context.user_data["Device_Context"]["Category"] = BIOS_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

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


async def w_c_BIOS_ChangeLoadingPriority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_BIOS_ChangeLoadingPriority()")
    CHANGE_LOADING_PRIORITY_DICT = WINDOWS_COMPUTER["BIOS"][
        "Change_Loading_Priority"]
    context.user_data["Device_Context"]["Problem"] = CHANGE_LOADING_PRIORITY_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
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


async def w_c_DevicesPeriphery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_DevicesPeriphery()")
    DEVICES_PERIPHERY_DICT = WINDOWS_COMPUTER["Devices_Periphery"]
    context.user_data["Device_Context"]["Category"] = DEVICES_PERIPHERY_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=DEVICES_PERIPHERY_DICT["No_Sound"]["0_RU"],
                              callback_data=DEVICES_PERIPHERY_DICT["No_Sound"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return DEVICES_PERIPHERY_DICT["0_EN"]


async def w_c_DevicesPeriphery_NoSound(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_DevicesPeriphery_NoSound()")
    NO_SOUND_DICT = WINDOWS_COMPUTER["Devices_Periphery"]["No_Sound"]
    context.user_data["Device_Context"]["Problem"] = NO_SOUND_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=NO_SOUND_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=NO_SOUND_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return NO_SOUND_DICT["0_EN"]


async def w_c_InstallationRecovery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_InstallationRecovery()")
    INSTALLATION_RECOVERY_DICT = WINDOWS_COMPUTER["Installation_Recovery"]
    context.user_data["Device_Context"]["Category"] = INSTALLATION_RECOVERY_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=INSTALLATION_RECOVERY_DICT["Missing_Disk_Partitions_When_Installing_OS"]["0_RU"],
                              callback_data=INSTALLATION_RECOVERY_DICT["Missing_Disk_Partitions_When_Installing_OS"][
                                  "0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return INSTALLATION_RECOVERY_DICT["0_EN"]


async def w_c_InstallationRecovery_MissingDiskPartitionsWhenInstallingOS(update: Update,
                                                                         context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_InstallationRecovery_MissingDiskPartitionsWhenInstallingOS()")
    MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS_DICT = WINDOWS_COMPUTER["Installation_Recovery"][
        "Missing_Disk_Partitions_When_Installing_OS"]
    context.user_data["Device_Context"]["Problem"] = MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return MISSING_DISK_PARTITIONS_WHEN_INSTALLING_OS_DICT["0_EN"]


async def w_c_NetworkInternet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_NetworkInternet()")
    NETWORK_INTERNET_DICT = WINDOWS_COMPUTER["Network_Internet"]
    context.user_data["Device_Context"]["Category"] = NETWORK_INTERNET_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=NETWORK_INTERNET_DICT["No_Available_Wifi"]["0_RU"],
                              callback_data=NETWORK_INTERNET_DICT["No_Available_Wifi"]["0_EN"]),
         InlineKeyboardButton(text=NETWORK_INTERNET_DICT["No_Internet_Connection"]["0_RU"],
                              callback_data=NETWORK_INTERNET_DICT["No_Internet_Connection"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return NETWORK_INTERNET_DICT["0_EN"]


async def w_c_NetworkInternet_NoAvailableWifi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_NetworkInternet_NoAvailableWifi()")
    NO_AVAILABLE_WIFI_DICT = WINDOWS_COMPUTER["Network_Internet"]["No_Available_Wifi"]
    context.user_data["Device_Context"]["Problem"] = NO_AVAILABLE_WIFI_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=NO_AVAILABLE_WIFI_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=NO_AVAILABLE_WIFI_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return NO_AVAILABLE_WIFI_DICT["0_EN"]


async def w_c_NetworkInternet_NoInternetConnection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_NetworkInternet_NoInternetConnection()")
    NO_INTERNET_CONNECTION_DICT = WINDOWS_COMPUTER["Network_Internet"]["No_Internet_Connection"]
    context.user_data["Device_Context"]["Problem"] = NO_INTERNET_CONNECTION_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=NO_INTERNET_CONNECTION_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=NO_INTERNET_CONNECTION_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return NO_INTERNET_CONNECTION_DICT["0_EN"]


async def w_c_SavingData(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SavingData()")
    SAVING_DATA_DICT = WINDOWS_COMPUTER["Saving_Data"]
    context.user_data["Device_Context"]["Category"] = SAVING_DATA_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=SAVING_DATA_DICT["Removing_Temp_Files"]["0_RU"],
                              callback_data=SAVING_DATA_DICT["Removing_Temp_Files"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return SAVING_DATA_DICT["0_EN"]


async def w_c_SavingData_RemovingTempFiles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SavingData_RemovingTempFiles()")
    REMOVING_TEMP_FILES_DICT = WINDOWS_COMPUTER["Saving_Data"]["Removing_Temp_Files"]
    context.user_data["Device_Context"]["Problem"] = REMOVING_TEMP_FILES_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=REMOVING_TEMP_FILES_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=REMOVING_TEMP_FILES_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return REMOVING_TEMP_FILES_DICT["0_EN"]


async def w_c_SlowingBugging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SlowingBugging()")
    SLOWING_BUGGING_DICT = WINDOWS_COMPUTER["Slowing_Bugging"]
    context.user_data["Device_Context"]["Category"] = SLOWING_BUGGING_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

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


async def w_c_SlowingBugging_Booting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SlowingBugging_Booting()")
    BOOTING_DICT = WINDOWS_COMPUTER["Slowing_Bugging"]["Booting"]
    context.user_data["Device_Context"]["Problem"] = BOOTING_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
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


async def w_c_SlowingBugging_HardDiskSSD(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SlowingBugging_Booting()")
    HARD_DISK_SSD_DICT = WINDOWS_COMPUTER["Slowing_Bugging"]["Hard_Disk_SSD"]
    context.user_data["Device_Context"]["Problem"] = HARD_DISK_SSD_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
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


async def w_c_SlowingBugging_Heating(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_SlowingBugging_Heating()")
    HEATING_DICT = WINDOWS_COMPUTER["Slowing_Bugging"]["Heating"]
    context.user_data["Device_Context"]["Problem"] = HEATING_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
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


async def w_c_UpdateDriver(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_UpdateDriver()")
    UPDATE_DRIVER_DICT = WINDOWS_COMPUTER["Update_Driver"]
    context.user_data["Device_Context"]["Category"] = UPDATE_DRIVER_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=UPDATE_DRIVER_DICT["Driver_Installation_Update"]["0_RU"],
                              callback_data=UPDATE_DRIVER_DICT["Driver_Installation_Update"]["0_EN"]),
         InlineKeyboardButton(text=UPDATE_DRIVER_DICT["Update_Windows_10_11"]["0_RU"],
                              callback_data=UPDATE_DRIVER_DICT["Update_Windows_10_11"]["0_EN"])],
        [InlineKeyboardButton(text=UPDATE_DRIVER_DICT["Turn_Off_Automatic_Updates"]["0_RU"],
                              callback_data=UPDATE_DRIVER_DICT["Turn_Off_Automatic_Updates"]["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_OTHER, callback_data=OTHER)],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return UPDATE_DRIVER_DICT["0_EN"]


async def w_c_UpdateDriver_DriverInstallationUpdate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_UpdateDriver_DriverInstallationUpdate()")
    DRIVER_INSTALLATION_UPDATE_DICT = WINDOWS_COMPUTER["Update_Driver"]["Driver_Installation_Update"]
    context.user_data["Device_Context"]["Problem"] = DRIVER_INSTALLATION_UPDATE_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=DRIVER_INSTALLATION_UPDATE_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=DRIVER_INSTALLATION_UPDATE_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return DRIVER_INSTALLATION_UPDATE_DICT["0_EN"]


async def w_c_UpdateDriver_UpdateWindows1011(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_UpdateDriver_UpdateWindows1011()")
    UPDATE_WINDOWS_10_11_DICT = WINDOWS_COMPUTER["Update_Driver"]["Update_Windows_10_11"]
    context.user_data["Device_Context"]["Problem"] = UPDATE_WINDOWS_10_11_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=UPDATE_WINDOWS_10_11_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=UPDATE_WINDOWS_10_11_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return UPDATE_WINDOWS_10_11_DICT["0_EN"]


async def w_c_UpdateDriver_TurnOffAutomaticUpdates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """STUFF"""
    logger_wiki_windows_computer.info("w_c_UpdateDriver_TurnOffAutomaticUpdates()")
    TURN_OFF_AUTOMATIC_UPDATES_DICT = WINDOWS_COMPUTER["Update_Driver"]["Turn_Off_Automatic_Updates"]
    context.user_data["Device_Context"]["Problem"] = TURN_OFF_AUTOMATIC_UPDATES_DICT["0_RU"]
    logger_wiki_windows_computer.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text=BUTTON_TEXT_SHARE,
                              switch_inline_query=TURN_OFF_AUTOMATIC_UPDATES_DICT["0_EN"])],
        [InlineKeyboardButton(text=BUTTON_TEXT_BACK, callback_data=BACK),
         InlineKeyboardButton(text=BUTTON_TEXT_CANCEL, callback_data=CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=TURN_OFF_AUTOMATIC_UPDATES_DICT["Text"],
                                  reply_markup=inline_markup, parse_mode=ParseMode.MARKDOWN)

    return TURN_OFF_AUTOMATIC_UPDATES_DICT["0_EN"]
