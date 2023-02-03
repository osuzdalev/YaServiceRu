import logging
from typing import Union

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

from clientcommands.wiki_module.wiki_apple_computer import (
    apple,
    a_computer,
    a_c_InstallationRecovery,
    a_c_SavingData,
    a_c_SlowingBugging,
    a_c_SlowingBugging_ResetCmosNvram,
    a_c_SystemSettings
)

from clientcommands.wiki_module.wiki_windows_computer import (
    windows,
    w_computer,
    w_c_BIOS,
    w_c_BIOS_ChangeLoadingPriority,
    w_c_DevicesPeriphery,
    w_c_DevicesPeriphery_NoSound,
    w_c_InstallationRecovery,
    w_c_InstallationRecovery_MissingDiskPartitionsWhenInstallingOS,
    w_c_NetworkInternet,
    w_c_NetworkInternet_NoAvailableWifi,
    w_c_NetworkInternet_NoInternetConnection,
    w_c_SavingData,
    w_c_SavingData_RemovingTempFiles,
    w_c_SlowingBugging,
    w_c_SlowingBugging_Booting,
    w_c_SlowingBugging_HardDiskSSD,
    w_c_SlowingBugging_Heating,
    w_c_UpdateDriver,
    w_c_UpdateDriver_DriverInstallationUpdate,
    w_c_UpdateDriver_UpdateWindows1011,
    w_c_UpdateDriver_TurnOffAutomaticUpdates
)
from clientcommands.wiki_module.wiki_json_utils import WIKI_DATA_DICT

logger_wiki = logging.getLogger(__name__)

# Basic callback_data
CANCEL = "CANCEL"
BACK = "BACK"
OTHER = "OTHER"

# Omnipresent buttons
BUTTON_TEXT_CANCEL = "CANCEL"
BUTTON_TEXT_BACK = "<< BACK"
BUTTON_TEXT_OTHER = "Другие/Иное"
BUTTON_TEXT_SHARE = "SHARE 🔗"

# Ultra repeated keys
APPLE_COMPUTER = WIKI_DATA_DICT["Apple"]["Computer"]
WINDOWS_COMPUTER = WIKI_DATA_DICT["Windows"]["Computer"]


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


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("wiki", wiki), MessageHandler(filters.Regex(r"^(📖Вики)$"), wiki)],
    states={
        WIKI_DATA_DICT["0_EN"]: [
            CallbackQueryHandler(apple, WIKI_DATA_DICT["Apple"]["0_EN"]),
            CallbackQueryHandler(windows, WIKI_DATA_DICT["Windows"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # ############################################# APPLE ##########################################################
        WIKI_DATA_DICT["Apple"]["0_EN"]: [
            CallbackQueryHandler(wiki_back, BACK),
            CallbackQueryHandler(a_computer, APPLE_COMPUTER["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ COMPUTER ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
        APPLE_COMPUTER["0_EN"]: [
            CallbackQueryHandler(apple, BACK),
            # CallbackQueryHandler(a_c_BIOS, APPLE_COMPUTER["BIOS"]["0_EN"]),
            # CallbackQueryHandler(a_c_DevicesPeriphery, APPLE_COMPUTER["Devices_Periphery"]["0_EN"]),
            CallbackQueryHandler(a_c_InstallationRecovery, APPLE_COMPUTER["Installation_Recovery"]["0_EN"]),
            # CallbackQueryHandler(a_c_NetworkInternet, APPLE_COMPUTER["Network_Internet"]["0_EN"]),
            CallbackQueryHandler(a_c_SavingData, APPLE_COMPUTER["Saving_Data"]["0_EN"]),
            CallbackQueryHandler(a_c_SlowingBugging, APPLE_COMPUTER["Slowing_Bugging"]["0_EN"]),
            CallbackQueryHandler(a_c_SystemSettings, APPLE_COMPUTER["System_Settings"]["0_EN"]),
            # CallbackQueryHandler(a_c_UpdateDriver, APPLE_COMPUTER["Update_Driver"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # ============================================= SLOWING_BUGGING ================================================
        APPLE_COMPUTER["Slowing_Bugging"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(a_c_SlowingBugging_ResetCmosNvram,
                                 APPLE_COMPUTER["Slowing_Bugging"]["Reset_CMOS_NVRAM"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        APPLE_COMPUTER["Slowing_Bugging"]["Reset_CMOS_NVRAM"]["0_EN"]: [
            CallbackQueryHandler(a_c_SlowingBugging, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # ############################################# WINDOWS ########################################################
        WIKI_DATA_DICT["Windows"]["0_EN"]: [
            CallbackQueryHandler(wiki_back, BACK),
            CallbackQueryHandler(w_computer, WINDOWS_COMPUTER["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡ COMPUTER ≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡
        WINDOWS_COMPUTER["0_EN"]: [
            CallbackQueryHandler(windows, BACK),
            CallbackQueryHandler(w_c_BIOS, WINDOWS_COMPUTER["BIOS"]["0_EN"]),
            CallbackQueryHandler(w_c_DevicesPeriphery, WINDOWS_COMPUTER["Devices_Periphery"]["0_EN"]),
            CallbackQueryHandler(w_c_InstallationRecovery, WINDOWS_COMPUTER["Installation_Recovery"]["0_EN"]),
            CallbackQueryHandler(w_c_NetworkInternet, WINDOWS_COMPUTER["Network_Internet"]["0_EN"]),
            CallbackQueryHandler(w_c_SavingData, WINDOWS_COMPUTER["Saving_Data"]["0_EN"]),
            CallbackQueryHandler(w_c_SlowingBugging, WINDOWS_COMPUTER["Slowing_Bugging"]["0_EN"]),
            CallbackQueryHandler(w_c_UpdateDriver, WINDOWS_COMPUTER["Update_Driver"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["BIOS"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_BIOS_ChangeLoadingPriority,
                                 WINDOWS_COMPUTER["BIOS"]["Change_Loading_Priority"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["BIOS"]["Change_Loading_Priority"]["0_EN"]: [
            CallbackQueryHandler(w_c_BIOS, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Devices_Periphery"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_DevicesPeriphery_NoSound,
                                 WINDOWS_COMPUTER["Devices_Periphery"]["No_Sound"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Devices_Periphery"]["No_Sound"]["0_EN"]: [
            CallbackQueryHandler(w_c_DevicesPeriphery, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Installation_Recovery"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_InstallationRecovery_MissingDiskPartitionsWhenInstallingOS,
                                 WINDOWS_COMPUTER["Installation_Recovery"][
                                     "Missing_Disk_Partitions_When_Installing_OS"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Installation_Recovery"]["Missing_Disk_Partitions_When_Installing_OS"]["0_EN"]: [
            CallbackQueryHandler(w_c_InstallationRecovery, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Network_Internet"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_NetworkInternet_NoAvailableWifi,
                                 WINDOWS_COMPUTER["Network_Internet"]["No_Available_Wifi"]["0_EN"]),
            CallbackQueryHandler(w_c_NetworkInternet_NoInternetConnection,
                                 WINDOWS_COMPUTER["Network_Internet"]["No_Internet_Connection"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Network_Internet"]["No_Available_Wifi"]["0_EN"]: [
            CallbackQueryHandler(w_c_NetworkInternet, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Network_Internet"]["No_Internet_Connection"]["0_EN"]: [
            CallbackQueryHandler(w_c_NetworkInternet, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Saving_Data"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_SavingData_RemovingTempFiles,
                                 WINDOWS_COMPUTER["Saving_Data"]["Removing_Temp_Files"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Saving_Data"]["Removing_Temp_Files"]["0_EN"]: [
            CallbackQueryHandler(w_c_SavingData, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Slowing_Bugging"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_SlowingBugging_Booting,
                                 WINDOWS_COMPUTER["Slowing_Bugging"]["Booting"][
                                     "0_EN"]),
            CallbackQueryHandler(w_c_SlowingBugging_HardDiskSSD,
                                 WINDOWS_COMPUTER["Slowing_Bugging"]["Hard_Disk_SSD"][
                                     "0_EN"]),
            CallbackQueryHandler(w_c_SlowingBugging_Heating,
                                 WINDOWS_COMPUTER["Slowing_Bugging"]["Heating"][
                                     "0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Slowing_Bugging"]["Booting"]["0_EN"]: [
            CallbackQueryHandler(w_c_SlowingBugging, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Slowing_Bugging"]["Hard_Disk_SSD"]["0_EN"]: [
            CallbackQueryHandler(w_c_SlowingBugging, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Slowing_Bugging"]["Heating"]["0_EN"]: [
            CallbackQueryHandler(w_c_SlowingBugging, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        # --------------------------------------------------------------------------------------------------------------
        WINDOWS_COMPUTER["Update_Driver"]["0_EN"]: [
            CallbackQueryHandler(w_computer, BACK),
            CallbackQueryHandler(w_c_UpdateDriver_DriverInstallationUpdate, WINDOWS_COMPUTER["Update_Driver"][
                "Driver_Installation_Update"]["0_EN"]),
            CallbackQueryHandler(w_c_UpdateDriver_UpdateWindows1011,
                                 WINDOWS_COMPUTER["Update_Driver"]["Update_Windows_10_11"]["0_EN"]),
            CallbackQueryHandler(w_c_UpdateDriver_TurnOffAutomaticUpdates, WINDOWS_COMPUTER["Update_Driver"][
                "Turn_Off_Automatic_Updates"]["0_EN"]),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Update_Driver"]["Driver_Installation_Update"]["0_EN"]: [
            CallbackQueryHandler(w_c_UpdateDriver, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Update_Driver"]["Update_Windows_10_11"]["0_EN"]: [
            CallbackQueryHandler(w_c_UpdateDriver, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
        WINDOWS_COMPUTER["Update_Driver"]["Turn_Off_Automatic_Updates"]["0_EN"]: [
            CallbackQueryHandler(w_c_UpdateDriver, BACK),
            CallbackQueryHandler(cancel_callback, CANCEL)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_command),
               MessageHandler(filters.Regex(r"^(❌Отменить)$"), cancel_command)],
    allow_reentry=True,
    conversation_timeout=15
)
