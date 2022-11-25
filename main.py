from configparser import ConfigParser
import logging
import sys

from telegram.ext import Application, CommandHandler, MessageHandler, filters, PreCheckoutQueryHandler

from clientcommands import request as req, start, wiki, payment
from contractorcommand import forward
from background import global_fallback

# Enable logging
logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

constants = ConfigParser()
constants.read("constants.ini")

# Group Handlers
CLIENT_BASIC, CLIENT_WIKI, CLIENT_PAY, CONTRACT_FORWARD, GLOBAL_FORWARD = range(1, 6)

if __name__ == "__main__":
    application = Application.builder() \
        .token(constants.get("TOKEN", "TOKEN"))\
        .build()

    # Client Handlers
    application.add_handler(CommandHandler("start", start.start), CLIENT_BASIC)
    application.add_handler(CommandHandler("request", req.request), CLIENT_BASIC)
    application.add_handler(MessageHandler(filters.CONTACT, req.reach_customer_service), CLIENT_BASIC)

    application.add_handler(wiki.wiki_conversation_handler, CLIENT_WIKI)

    # Payment
    application.add_handler(CommandHandler("pay", payment.start_without_shipping_callback), CLIENT_PAY)
    # application.add_handler(CommandHandler("shipping", start_with_shipping_callback))
    # Optional handler if your product requires shipping
    # application.add_handler(ShippingQueryHandler(shipping_callback))
    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(payment.precheckout_callback), CLIENT_PAY)
    # Notify user of successful payment
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, payment.successful_payment_callback), CLIENT_PAY)

    # Contractor Handlers
    application.add_handler(forward.forward_conversation_handler, CONTRACT_FORWARD)

    # Global fallback Handler stopping every ConversationHandlers
    application.add_handler(global_fallback.global_fallback_handler, GLOBAL_FORWARD)

    application.run_polling()
