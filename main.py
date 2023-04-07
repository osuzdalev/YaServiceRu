import logging
import pickle
import sys
import pprint

from telegram.ext import Application, PicklePersistence

from resources.constants_loader import load_constants
from clientcommands import request as req, start
from clientcommands.chatgpt_module import chatgpt
from clientcommands.wiki_module import wiki_command
# from contractorcommands import assign, complete, commands
from centercommands import orders
from background import global_fallback, data_collector, error_logging

constants = load_constants()

# Enable logging

logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(constants.get("FILEPATH", "LOCAL_LOGGER"), mode='a')
    ]
)
logger = logging.getLogger(__name__)


# Group Handlers
MESSAGE_COLLECTION, USER_STATUS_COLLECTION, PHONE_COLLECTION, \
CLIENT_BASIC, CLIENT_WIKI, CLIENT_PAY, \
CONTRACTOR_BASIC, CONTRACTOR_ASSIGN, \
GLOBAL_FALLBACK = range(-3, 6)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath=constants.get("FILEPATH", "LOCAL_PERSISTENCE"))
    application = Application.builder()\
        .token(constants.get("TOKEN", "DEV_BOT"))\
        .persistence(persistence)\
        .arbitrary_callback_data(True)\
        .build()

    # DATA COLLECTION
    application.add_handler(data_collector.data_collection_handler, MESSAGE_COLLECTION)
    # TODO
    # application.add_handler(data_collector.user_status_handler, USER_STATUS_COLLECTION)
    application.add_handler(data_collector.collection_phone_number_handler, PHONE_COLLECTION)

    # ERROR HANDLER
    application.add_error_handler(error_logging.error_handler)

    # CLIENT HANDLERS
    application.add_handler(start.start_handler, CLIENT_BASIC)
    application.add_handler(req.request_handler, CLIENT_BASIC)
    application.add_handler(req.request_replykeyboard_handler, CLIENT_BASIC)

    application.add_handler(wiki_command.conversation_handler, CLIENT_WIKI)
    # TODO make the wiki objects compatible with inline queries
    # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

    # CHATGPT
    application.add_handler(chatgpt.gpt_handler_command, CLIENT_BASIC)
    application.add_handler(chatgpt.gpt_handler_message, CLIENT_BASIC)
    application.add_handler(chatgpt.gpt_request_handler, CLIENT_BASIC)
    application.add_handler(chatgpt.gpt_payment_yes_handler, CLIENT_PAY)
    application.add_handler(chatgpt.gpt_precheckout_handler, CLIENT_PAY)
    application.add_handler(chatgpt.gpt_successful_payment_handler, CLIENT_PAY)
    application.add_handler(chatgpt.gpt_payment_no_handler, CLIENT_PAY)
    application.add_handler(chatgpt.gpt_stop_handler_command, CLIENT_BASIC)
    application.add_handler(chatgpt.gpt_stop_handler_message, CLIENT_BASIC)
    application.add_handler(chatgpt.gpt_get_conversation_tokens_handler, CLIENT_BASIC)

    # CONTRACTOR HANDLERS
    # application.add_handler(assign.assign_conversation_handler, CONTRACTOR_ASSIGN)
    # application.add_handler(assign.assignment_response_handler)
    # application.add_handler(complete.complete_handler, CONTRACTOR_BASIC)
    # application.add_handler(commands.commands_handler, CONTRACTOR_BASIC)

    # CENTER HANDLERS
    application.add_handler(orders.orders_handler)

    # Global fallback Handler stopping every ConversationHandlers
    application.add_handler(global_fallback.global_fallback_handler, GLOBAL_FALLBACK)

    application.run_polling()
