from configparser import ConfigParser
import logging

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from background import helpers, telegram_database as tldb

logger_assign = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")

# States for /assign Conversation
ASSIGN_PAGE_1, ASSIGN_PAGE_2, ASSIGN_PAGE_3 = range(3)
ASSIGN_PAGE_1_NEXT = 0
ASSIGN_PAGE_2_BACK, ASSIGN_PAGE_2_NEXT = range(2)
ASSIGN_PAGE_3_BACK = 0


async def assign(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Contractor command: opens Converstation to select which ContractorID to send current Order to"""
    logger_assign.info("assign()")
    # Save current OrderID in the user_data
    logger_assign.info("context.args")
    context.bot_data["Current Order"] = context.args[0]

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=ASSIGN_PAGE_1_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Select Contractor", reply_markup=inline_markup)
    logger_assign.info("assign()")

    return ASSIGN_PAGE_1


async def assign_start_over(update: Update, context: ContextTypes.DEFAULT_TYPE, query) -> int:
    logger_assign.info("assign_start_over()")
    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=ASSIGN_PAGE_1_NEXT)]
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Already assigned to this person, choose someone else or cancel.", reply_markup=inline_markup)
    return ASSIGN_PAGE_1


async def assign_page_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """First page of the /assign Inline Menu as a Callback Query"""
    logger_assign.info("assign_page_1()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="NEXT >>", callback_data=ASSIGN_PAGE_1_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return ASSIGN_PAGE_1


async def assign_page_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Second page of the /assign Inline Menu"""
    logger_assign.info("assign_page_2()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="<< PREVIOUS", callback_data=ASSIGN_PAGE_2_BACK),
         InlineKeyboardButton(text="NEXT >>", callback_data=ASSIGN_PAGE_2_NEXT)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return ASSIGN_PAGE_2


async def assign_page_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Third page of the /assign Inline Menu"""
    logger_assign.info("assign_page_3()")

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton(text="Oleg (Ru)", callback_data=constants.get("ID", "MAIN")),
         InlineKeyboardButton(text="Oleg (Fr)", callback_data=constants.get("ID", "FR"))],
        [InlineKeyboardButton(text="<< PREVIOUS", callback_data=ASSIGN_PAGE_3_BACK)],
    ]
    inline_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Select Contractor", reply_markup=inline_markup)

    return ASSIGN_PAGE_3


async def assign_to_contractor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ContractID in current Order is changed to new contractor selected
    then Order details are sent as a message to Contractor"""
    logger_assign.info("assign_to_contractor()")

    query = update.callback_query
    await query.answer()

    old_ContractorID = update.effective_user.id

    order_data = tldb.get_order_data(context.bot_data["Current Order"])
    OrderID = order_data[0]

    contractor_data = tldb.get_contractor_data(int(query.data))
    new_ContractorID = contractor_data[0]

    # Check if this particular transaction was already done
    assign_exists = tldb.check_assign(old_ContractorID, OrderID, new_ContractorID)

    if assign_exists:
        await assign_start_over(update, context, query)
    else:
        # Assign data saved in memory to be accessed during new_Contractor answer
        context.bot_data["assignment_"+str(new_ContractorID)] = {"old_ContractorID": old_ContractorID,
                                                                 "OrderID": OrderID,
                                                                 "new_ContractorID": new_ContractorID}

        # Assignment proposed to new_Contractor with Order data
        customer_data = tldb.get_customer_data(order_data[1])
        customer_phone_number = customer_data[-1]
        order_message_str = helpers.get_order_message_str(OrderID, customer_data, order_data, customer_phone_number)

        assignment_keyboard = [["❌", "✅"]]
        assignment_markup = ReplyKeyboardMarkup(assignment_keyboard, one_time_keyboard=True)
        await context.bot.sendMessage(new_ContractorID, order_message_str, reply_markup=assignment_markup)

        # old_Contractor notified that assignment was sent
        await query.edit_message_text("Order passed to \n{}\n{}\n{}\n{}"
                                      .format(contractor_data[1], contractor_data[2], contractor_data[3], contractor_data[4]))
        return ConversationHandler.END


async def assignment_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """STUFF"""
    logger_assign.info("assignment_answer()")
    logger_assign.info("context.bot_data: {}".format(context.bot_data))

    answer = True if update.message.text == "✅" else False
    assignment_data = context.bot_data["assignment_"+str(update.effective_user.id)]
    old_ContractorID = assignment_data["old_ContractorID"]
    OrderID = assignment_data["OrderID"]
    new_ContractorID = assignment_data["new_ContractorID"]
    new_Contractor_username = tldb.get_contractor_data(new_ContractorID)[1]

    if answer:
        # Change the ContractID for the Order
        tldb.update_order_ContractorID(OrderID, new_ContractorID)
        # Keep a record of this transaction
        tldb.insert_assign(old_ContractorID, OrderID, new_ContractorID)

        # Notify both contractors of successful assignment
        await update.effective_message.reply_text("Order successfully assigned to you ✅")
        await context.bot.sendMessage(old_ContractorID, "Order successfully assigned to {} ✅".format(new_Contractor_username))
    else:
        context.bot_data["Current Order"] = ''
        del context.bot_data["assignment_"+str(update.effective_user.id)]
        # Notify both contractors of refused assignment
        await update.effective_message.reply_text("Order refused ❌")
        await context.bot.sendMessage(old_ContractorID, "Order refused by {} ❌".format(new_Contractor_username))


assign_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("assign", assign)],
    states={
        ASSIGN_PAGE_1: [
            CallbackQueryHandler(assign_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(assign_page_2, "^" + str(ASSIGN_PAGE_1_NEXT) + "$")
        ],
        ASSIGN_PAGE_2: [
            CallbackQueryHandler(assign_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(assign_page_1, "^" + str(ASSIGN_PAGE_2_BACK) + "$"),
            CallbackQueryHandler(assign_page_3, "^" + str(ASSIGN_PAGE_2_NEXT) + "$")
        ],
        ASSIGN_PAGE_3: [
            CallbackQueryHandler(assign_to_contractor, r"\d{8,10}"),
            CallbackQueryHandler(assign_page_2, "^" + str(ASSIGN_PAGE_3_BACK) + "$")
        ],
    },
    fallbacks=[],
    allow_reentry=True,
    conversation_timeout=15
)

assignment_response_handler = MessageHandler(filters.User(user_id=tldb.get_all_ContractorID())
                                             & filters.Regex(r"✅|❌"), assignment_answer)
