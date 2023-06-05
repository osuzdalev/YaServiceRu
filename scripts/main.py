import logging
import os
import sys

from telegram.ext import Application, PicklePersistence

from dotenv import load_dotenv

from src.common.error_logging.error_logging_handler import ErrorHandler
from src.common.global_fallback.global_fallback_handler import GlobalFallbackHandler

from src.command.client.request.request_handler import RequestHandler
from src.command.client.start.start_handler import StartHandler
from src.command.client.chatgpt.chatgpt_handler import ChatGptHandler
from src.command.client.wiki.wiki_handler import WikiHandler

# from contractor import assign, complete, command
from src.command.center import orders
from src.common.data.collector_handler import CollectorHandler

load_dotenv()

logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.getenv("FILEPATH_LOGGER"), mode="a"),
    ],
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    persistence = PicklePersistence(filepath=os.getenv("FILEPATH_PERSISTENCE"))
    application = (
        Application.builder()
        .token(os.getenv("TOKEN_TG_MAIN_BOT"))
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    # DATA COLLECTION
    application.add_handler(CollectorHandler().get_handlers())

    # ERROR HANDLER
    application.add_error_handler(ErrorHandler().get_handler())

    # CLIENT HANDLERS
    application.add_handlers(handlers=StartHandler().get_handlers())

    # REQUEST
    application.add_handlers(handlers=RequestHandler().get_handlers())

    # WIKI
    application.add_handlers(handlers=WikiHandler().get_handlers())
    # TODO make the wiki objects compatible with inline queries
    # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

    # CHATGPT
    application.add_handlers(handlers=ChatGptHandler().get_handlers())

    # CONTRACTOR HANDLERS
    # application.add_handler(assign.assign_conversation_handler, CONTRACTOR_ASSIGN)
    # application.add_handler(assign.assignment_response_handler)
    # application.add_handler(complete.complete_handler, CONTRACTOR_BASIC)
    # application.add_handler(command.commands_handler, CONTRACTOR_BASIC)

    # CENTER HANDLERS
    application.add_handler(orders.orders_handler)

    # Global fallback Handler stopping every ConversationHandlers
    application.add_handler(
        GlobalFallbackHandler().get_handler(),
        GlobalFallbackHandler().get_handler_group(),
    )

    application.run_polling()
