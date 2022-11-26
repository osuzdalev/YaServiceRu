import logging
from pprint import pformat

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

logger_wiki = logging.getLogger(__name__)

# All States for /wiki Conversation
DEVICE_OS, DEVICE, DEVICE_COMPUTER, DEVICE_COMPUTER_SCREEN, DEVICE_COMPUTER_SCREEN_P1, DEVICE_PHONE = range(6)

# State DEVICE_OS
DEVICE_OS_CANCEL, APPLE, ANDROID_LINUX, WINDOWS = range(4)

# State DEVICE
DEVICE_BACK, DEVICE_CANCEL, COMPUTER, PHONE = range(4)

COMPUTER_BACK_APPLE, COMPUTER_BACK_ANDROID, COMPUTER_BACK_WINDOWS, COMPUTER_CANCEL,\
COMPUTER_SCREEN, COMPUTER_KEYBOARD, COMPUTER_PROCESSOR, COMPUTER_GRAPHIC_CARD = range(8)

COMPUTER_SCREEN_BACK, COMPUTER_SCREEN_CANCEL, COMPUTER_SCREEN_P1, COMPUTER_SCREEN_P2, COMPUTER_SCREEN_P3, COMPUTER_SCREEN_P4 = range(6)
COMPUTER_SCREEN_P1_BACK, COMPUTER_SCREEN_P1_CANCEL = range(2)

PHONE_BACK, PHONE_CANCEL, PHONE_SCREEN, PHONE_KEYBOARD, PHONE_PROCESSOR, PHONE_GRAPHIC_CARD = range(6)


async def wiki(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("wiki()")
    device_context = {"Device_OS_Brand": '', "Device": '', "Part": '', "Problem": ''}
    context.user_data["Device_Context"] = device_context

    keyboard = [
        [InlineKeyboardButton(text="Apple/iOS", callback_data=APPLE)],
        [InlineKeyboardButton(text="Android / Linux", callback_data=ANDROID_LINUX),
         InlineKeyboardButton(text="Windows", callback_data=WINDOWS)],
        [InlineKeyboardButton(text="Cancel", callback_data=DEVICE_OS_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select a Brand/OS", reply_markup=inline_markup)

    return DEVICE_OS


async def wiki_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("wiki()")
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Apple/iOS", callback_data=APPLE)],
        [InlineKeyboardButton(text="Android / Linux", callback_data=ANDROID_LINUX),
         InlineKeyboardButton(text="Windows", callback_data=WINDOWS)],
        [InlineKeyboardButton(text="Cancel", callback_data=DEVICE_OS_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a Brand/OS", reply_markup=inline_markup)

    return DEVICE_OS


async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Canceled")
    return ConversationHandler.END


async def apple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `wiki` does but not as new message"""
    logger_wiki.info("apple()")
    context.user_data["Device_Context"]["Device_OS_Brand"] = "Apple"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Computer", callback_data=COMPUTER),
         InlineKeyboardButton(text="Phone", callback_data=PHONE)],
        [InlineKeyboardButton(text="<< BACK", callback_data=DEVICE_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=DEVICE_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return DEVICE


async def android(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `wiki` does but not as new message"""
    logger_wiki.info("android_linux()")
    context.user_data["Device_Context"]["Device_OS_Brand"] = "Android"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Computer", callback_data=COMPUTER),
         InlineKeyboardButton(text="Phone", callback_data=PHONE)],
        [InlineKeyboardButton(text="<< BACK", callback_data=DEVICE_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=DEVICE_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return DEVICE


async def windows(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """WINDOWS"""
    logger_wiki.info("windows()")
    context.user_data["Device_Context"]["Device_OS_Brand"] = "Windows"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()
    keyboard = [
        [InlineKeyboardButton(text="Computer", callback_data=COMPUTER),
         InlineKeyboardButton(text="Phone", callback_data=PHONE)],
        [InlineKeyboardButton(text="<< BACK", callback_data=DEVICE_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=DEVICE_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select a device", reply_markup=inline_markup)

    return DEVICE


async def computer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("computer()")
    context.user_data["Device_Context"]["Device"] = "Computer"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    computer_back = 0
    if context.user_data["Device_Context"]["Device_OS_Brand"] == "Apple":
        computer_back = COMPUTER_BACK_APPLE
    elif context.user_data["Device_Context"]["Device_OS_Brand"] == "Android":
        computer_back = COMPUTER_BACK_ANDROID
    else:
        computer_back = COMPUTER_BACK_WINDOWS

    keyboard = [
        [InlineKeyboardButton(text="Computer Screen", callback_data=COMPUTER_SCREEN),
         InlineKeyboardButton(text="Computer Keyboard", callback_data=COMPUTER_KEYBOARD)],
        [InlineKeyboardButton(text="Computer Processor", callback_data=COMPUTER_PROCESSOR),
         InlineKeyboardButton(text="Computer Graphic Card", callback_data=COMPUTER_GRAPHIC_CARD)],
        [InlineKeyboardButton(text="<< BACK", callback_data=computer_back),
         InlineKeyboardButton(text="Cancel", callback_data=COMPUTER_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a component", reply_markup=inline_markup)

    return DEVICE_COMPUTER


async def computer_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    logger_wiki.info("computer_screen()")
    context.user_data["Device_Context"]["Part"] = "Screen"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Computer Screen P1", callback_data=COMPUTER_SCREEN_P1),
         InlineKeyboardButton(text="Computer Screen P2", callback_data=COMPUTER_SCREEN_P2)],
        [InlineKeyboardButton(text="Computer Screen P3", callback_data=COMPUTER_SCREEN_P3),
         InlineKeyboardButton(text="Computer Screen P4", callback_data=COMPUTER_SCREEN_P4)],
        [InlineKeyboardButton(text="<< BACK", callback_data=COMPUTER_SCREEN_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=COMPUTER_SCREEN_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a problem", reply_markup=inline_markup)

    return DEVICE_COMPUTER_SCREEN


async def computer_screen_p1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """STUFF"""
    logger_wiki.info("computer_screen_p1()")
    context.user_data["Device_Context"]["Problem"] = "Broken Screen"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="<< BACK", callback_data=COMPUTER_SCREEN_P1_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=COMPUTER_SCREEN_P1_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Here is the answer to your question:\n"
                                       "Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                                       "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, "
                                       "when an unknown printer took a galley of type and scrambled it to make a"
                                       "type specimen book. It has survived not only five centuries, but also the leap "
                                       "into electronic typesetting, remaining essentially unchanged. "
                                       "It was popularised in the 1960s with the release of Letraset sheets containing "
                                       "Lorem Ipsum passages, and more recently with desktop publishing software "
                                       "like Aldus PageMaker including versions of Lorem Ipsum.", reply_markup=inline_markup)
    # await context.bot.send_photo(query.message.chat_id,
    # "https://i.pcmag.com/imagery/roundups/05ersXu1oMXozYJa66i9GEo-38..v1657319390.jpg")

    return DEVICE_COMPUTER_SCREEN_P1


async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stuff"""
    logger_wiki.info("phone()")
    context.user_data["Device_Context"]["Device"] = "Phone"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Phone Screen", callback_data=PHONE_SCREEN),
         InlineKeyboardButton(text="Phone Keyboard", callback_data=PHONE_KEYBOARD)],
        [InlineKeyboardButton(text="Phone Processor", callback_data=PHONE_PROCESSOR),
         InlineKeyboardButton(text="Phone Graphic Card", callback_data=PHONE_GRAPHIC_CARD)],
        [InlineKeyboardButton(text="<< BACK", callback_data=PHONE_BACK),
         InlineKeyboardButton(text="Cancel", callback_data=PHONE_CANCEL)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Select a component", reply_markup=inline_markup)

    return PHONE


async def phone_screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    logger_wiki.info("phone_screen()")
    context.user_data["Device_Context"]["Part"] = "Screen"
    logger_wiki.info("context.user_data: {}".format(pformat(context.user_data)))

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="Here is the answer to your question:\n"
                                       "Lorem Ipsum is simply dummy text of the printing and typesetting industry. "
                                       "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, "
                                       "when an unknown printer took a galley of type and scrambled it to make a"
                                       "type specimen book. It has survived not only five centuries, but also the leap "
                                       "into electronic typesetting, remaining essentially unchanged. "
                                       "It was popularised in the 1960s with the release of Letraset sheets containing "
                                       "Lorem Ipsum passages, and more recently with desktop publishing software "
                                       "like Aldus PageMaker including versions of Lorem Ipsum.")
    await context.bot.send_photo(query.message.chat_id,
                                 "AgACAgQAAxkBAAEaA5pjdOcrgVo49SOVfjOGoKWDQU5ejAACLa8xG_6apVMGam1ZdlbEYwEAAwIAA3MAAysE")
    return ConversationHandler.END


wiki_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("wiki", wiki)],
    states={
        DEVICE_OS: [
            CallbackQueryHandler(apple, "^" + str(APPLE) + "$"),
            CallbackQueryHandler(android, "^" + str(ANDROID_LINUX) + "$"),
            CallbackQueryHandler(windows, "^" + str(WINDOWS) + "$"),
            CallbackQueryHandler(cancel, "^" + str(DEVICE_OS_CANCEL) + "$")
        ],
        DEVICE: [
            CallbackQueryHandler(wiki_back, "^" + str(DEVICE_BACK) + "$"),
            CallbackQueryHandler(computer, "^" + str(COMPUTER) + "$"),
            CallbackQueryHandler(phone, "^" + str(PHONE) + "$"),
            CallbackQueryHandler(cancel, "^" + str(DEVICE_CANCEL) + "$")
        ],
        DEVICE_COMPUTER: [
            CallbackQueryHandler(apple, "^" + str(COMPUTER_BACK_APPLE) + "$"),
            CallbackQueryHandler(android, "^" + str(COMPUTER_BACK_ANDROID) + "$"),
            CallbackQueryHandler(windows, "^" + str(COMPUTER_BACK_WINDOWS) + "$"),
            CallbackQueryHandler(computer_screen, "^" + str(COMPUTER_SCREEN) + "$"),
            CallbackQueryHandler(cancel, "^" + str(COMPUTER_CANCEL) + "$")
        ],
        DEVICE_COMPUTER_SCREEN: [
            CallbackQueryHandler(computer, "^" + str(COMPUTER_SCREEN_BACK) + "$"),
            CallbackQueryHandler(computer_screen_p1, "^" + str(COMPUTER_SCREEN_P1) + "$"),
            CallbackQueryHandler(cancel, "^" + str(COMPUTER_SCREEN_CANCEL) + "$")
        ],
        DEVICE_COMPUTER_SCREEN_P1: [
            CallbackQueryHandler(computer_screen, "^" + str(COMPUTER_SCREEN_P1_BACK) + "$"),
            CallbackQueryHandler(cancel, "^" + str(COMPUTER_SCREEN_P1_CANCEL) + "$")
        ],
        DEVICE_PHONE: [
            CallbackQueryHandler(phone, "^" + str(PHONE_BACK) + "$"),
            CallbackQueryHandler(phone_screen, "^" + str(PHONE_SCREEN) + "$"),
            CallbackQueryHandler(cancel, "^" + str(PHONE_CANCEL) + "$")
        ]
    },
    fallbacks=[],
    allow_reentry=True,
    conversation_timeout=15
)
