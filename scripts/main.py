import logging
import os
import sys

from telegram.ext import Application, PicklePersistence

from dotenv import load_dotenv
from src.commands.client import request as req
from src.commands.client import start
from src.commands.client.chatgpt_module.chatgpt_handler import ChatGptHandler
from src.commands.client.wiki_module import wiki_command

# from contractor import assign, complete, commands
from src.commands.center import orders
from src.common import error_logging
from src.common import global_fallback, data_collector

load_dotenv()

# Enable logging

logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.getenv("FILEPATH_LOGGER"), mode="a"),
    ],
)
logger = logging.getLogger(__name__)


# Group Handlers
(
    MESSAGE_COLLECTION,
    USER_STATUS_COLLECTION,
    PHONE_COLLECTION,
    CLIENT_BASIC,
    CLIENT_WIKI,
    CLIENT_PAY,
    CONTRACTOR_BASIC,
    CONTRACTOR_ASSIGN,
    GLOBAL_FALLBACK,
) = range(-3, 6)

if __name__ == "__main__":
    persistence = PicklePersistence(
        filepath=os.getenv("FILEPATH_PERSISTENCE")
    )
    application = (
        Application.builder()
        .token(os.getenv("TOKEN_TG_MAIN_BOT"))
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    # DATA COLLECTION
    #application.add_handler(data_collector.data_collection_handler, MESSAGE_COLLECTION)
    # TODO
    # application.add_handler(data_collector.user_status_handler, USER_STATUS_COLLECTION)
    application.add_handler(
        data_collector.collection_phone_number_handler, PHONE_COLLECTION
    )

    # ERROR HANDLER
    application.add_error_handler(error_logging.error_handler)

    # CLIENT HANDLERS
    application.add_handler(start.start_handler, CLIENT_BASIC)

    # REQUEST
    application.add_handler(req.request_command_handler, CLIENT_BASIC)
    application.add_handler(req.request_replykeyboard_handler, CLIENT_BASIC)
    application.add_handler(req.request_callback_handler, CLIENT_BASIC)
    application.add_handler(req.confirm_request_handler, CLIENT_BASIC)
    application.add_handler(req.cancel_request_handler, CLIENT_BASIC)
    application.add_handler(req.cancel_request_handler_message, CLIENT_BASIC)

    application.add_handler(wiki_command.conversation_handler, CLIENT_WIKI)
    # TODO make the wiki objects compatible with inline queries
    # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

    # CHATGPT
    application.add_handlers(handlers=ChatGptHandler().get_handlers())

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
