from configparser import ConfigParser
import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler

from background import helpers, telegram_database as tldb

logger_forward = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")

# States for /forward Conversation
FORWARD_PAGE_1, FORWARD_PAGE_2, FORWARD_PAGE_3 = range(3)
FORWARD_PAGE_1_NEXT = 0
FORWARD_PAGE_2_BACK, FORWARD_PAGE_2_NEXT = range(2)
FORWARD_PAGE_3_BACK = 0

async def forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Contractor command: opens Converstation to select which ContractorID to send current Order to"""
    logger_forward.info("forward()")
    # Save current OrderID in the user_data
    logger_forward.info("context.args")
    context.bot_data["Current Order"] = context.args[0]

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=FORWARD_PAGE_1_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select Contractor", reply_markup=inline_markup)
    logger_forward.info("forward()")

    return FORWARD_PAGE_1


async def forward_start_over(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    logger_forward.info("forward_start_over()")
    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=FORWARD_PAGE_1_NEXT)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Already forwarded to this person, choose someone else or cancel.", reply_markup=inline_markup)
    return FORWARD_PAGE_1


async def forward_page_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """First page of the /forward Inline Menu as a Callback Query"""
    logger_forward.info("forward_page_1()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=FORWARD_PAGE_1_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return FORWARD_PAGE_1


async def forward_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Second page of the /forward Inline Menu"""
    logger_forward.info("forward_page_2()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="<< PREVIOUS", callback_data=FORWARD_PAGE_2_BACK),
         InlineKeyboardButton(text="NEXT >>", callback_data=FORWARD_PAGE_2_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return FORWARD_PAGE_2


async def forward_page_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Third page of the /forward Inline Menu"""
    logger_forward.info("forward_page_3()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="<< PREVIOUS", callback_data=FORWARD_PAGE_3_BACK)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return FORWARD_PAGE_3


async def forward_to_contractor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ContractID in current Order is changed to new contractor selected
    then Order details are sent as a message to Contractor"""
    logger_forward.info("forward_to_contractor()")
    query = update.callback_query
    await query.answer()

    old_Contractor = update.effective_user.id

    order_data = tldb.get_order_data(context.bot_data["Current Order"])
    OrderID = order_data[0]

    contractor_data = tldb.get_contractor_data(int(query.data))
    new_ContractorID = contractor_data[0]

    # Check if this particular transaction was already done
    forward_exists = tldb.check_forward(old_Contractor, OrderID, new_ContractorID)

    if forward_exists:
        await forward_start_over(update, context, query)
    else:
        # Change the ContractID for the Order
        tldb.update_order_ContractID(OrderID, new_ContractorID)
        # Keep a record of this transaction
        tldb.insert_forward(old_Contractor, OrderID, new_ContractorID)

        # Send forwarded Order info to both old_Contractor and new_Contractor
        customer_data = tldb.get_customer_data(order_data[1])
        customer_phone_number = customer_data[-1]
        order_message_str = helpers.get_order_message_str(OrderID, customer_data, order_data, customer_phone_number)

        await context.bot.sendMessage(new_ContractorID, order_message_str)
        await query.edit_message_text("Order passed to \n{}\n{}\n{}\n{}"
                                      .format(contractor_data[1], contractor_data[2], contractor_data[3], contractor_data[4]))

        return ConversationHandler.END


forward_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("forward", forward)],
    states={
        FORWARD_PAGE_1: [
            CallbackQueryHandler(forward_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(forward_page_2, "^" + str(FORWARD_PAGE_1_NEXT) + "$")
        ],
        FORWARD_PAGE_2: [
            CallbackQueryHandler(forward_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(forward_page_1, "^" + str(FORWARD_PAGE_2_BACK) + "$"),
            CallbackQueryHandler(forward_page_3, "^" + str(FORWARD_PAGE_2_NEXT) + "$")
        ],
        FORWARD_PAGE_3: [
            CallbackQueryHandler(forward_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(forward_page_2, "^" + str(FORWARD_PAGE_3_BACK) + "$")
        ],
    },
    fallbacks=[],
    allow_reentry=True,
    conversation_timeout=15
)
