from configparser import ConfigParser
import logging.handlers
import sys

from telegram.ext import Application

from clientcommands import request as req, start, payment
from clientcommands.wiki_module import wiki_command
from contractorcommand import assign, complete, commands
from centercommand import orders
from background import global_fallback, data_collector, error_logging

constants = ConfigParser()
constants.read("constants.ini")

# Enable logging
logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    # Needs to be changed to ERROR
    level=logging.INFO,
    # Write logs to terminal
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# Group Handlers
MESSAGE_COLLECTION, USER_STATUS_COLLECTION, PHONE_COLLECTION, \
CLIENT_BASIC, CLIENT_WIKI, CLIENT_PAY, \
CONTRACTOR_BASIC, CONTRACTOR_ASSIGN, \
GLOBAL_FALLBACK = range(-3, 6)

if __name__ == "__main__":
    application = Application.builder() \
        .token(constants.get("TOKEN", "TOKEN")) \
        .build()

    # Data Collection
    application.add_handler(data_collector.data_collection_handler, MESSAGE_COLLECTION)
    # TODO
    # application.add_handler(data_collector.user_status_handler, USER_STATUS_COLLECTION)
    application.add_handler(data_collector.collection_phone_number_handler, PHONE_COLLECTION)

    # Error handler
    application.add_error_handler(error_logging.error_handler)

    # Client Handlers
    application.add_handler(start.start_handler, CLIENT_BASIC)
    application.add_handler(req.request_handler, CLIENT_BASIC)
    application.add_handler(req.request_replykeyboard_handler, CLIENT_BASIC)

    application.add_handler(wiki_command.conversation_handler, CLIENT_WIKI)
    application.add_handler(wiki_command.share_inline_query_handler, CLIENT_WIKI)

    # Payment
    application.add_handler(payment.pay_handler, CLIENT_PAY)
    # application.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    # Optional handler if your product requires shipping
    # application.add_handler(ShippingQueryHandler(shipping_callback))
    # Pre-checkout handler to final check
    application.add_handler(payment.precheckout_handler, CLIENT_PAY)
    # Notify user of successful payment
    application.add_handler(payment.successful_payment_handler, CLIENT_PAY)

    # Contractor Handlers
    application.add_handler(assign.assign_conversation_handler, CONTRACTOR_ASSIGN)
    application.add_handler(assign.assignment_response_handler)
    application.add_handler(complete.complete_handler, CONTRACTOR_BASIC)
    application.add_handler(commands.commands_handler, CONTRACTOR_BASIC)

    # Center Handlers
    application.add_handler(orders.orders_handler)

    # Global fallback Handler stopping every ConversationHandlers
    application.add_handler(global_fallback.global_fallback_handler, GLOBAL_FALLBACK)

    application.run_polling()
