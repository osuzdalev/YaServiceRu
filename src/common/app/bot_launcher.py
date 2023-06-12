import logging
import os
import sys

from telegram.ext import Application, PicklePersistence
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from src.common.error_logging.error_logging_handler import ErrorHandler
from src.common.global_fallback.global_fallback_handler import GlobalFallbackHandler
from src.common.database.collector_handler import CollectorHandler

from src.command.client.request.handler import RequestHandler
from src.command.client.start.handler import StartHandler
from src.command.client.chatgpt.handler import ChatGptHandler
from src.command.client.wiki.wiki_handler import WikiHandler
from src.command.center import orders
# from contractor import assign, complete, command


class BotLauncher:
    def __init__(
            self,
            token=os.getenv("TOKEN_TG_MAIN_BOT"),
            filepath_logger=os.getenv("FILEPATH_LOGGER"),
            filepath_persistence=os.getenv("FILEPATH_PERSISTENCE"),
            module_handlers=None,
            log_level=logging.INFO
    ):
        if module_handlers is None:
            module_handlers = [
                StartHandler,
                RequestHandler,
                WikiHandler,
                ChatGptHandler,
                ErrorHandler,
                CollectorHandler,
                GlobalFallbackHandler,
                "CenterOrders"  # Special keyword for center handlers
            ]
        self.module_handlers = module_handlers
        self.token = token
        self.filepath_logger = filepath_logger
        self.filepath_persistence = filepath_persistence
        self.log_level = log_level

    def setup_logging(self):
        logging.basicConfig(
            format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
            level=self.log_level,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.filepath_logger, mode="a"),
            ],
        )

    def add_module_handlers(self, application):
        # Add module handlers specified by the user
        for module_handler in self.module_handlers:
            if module_handler == ErrorHandler:
                application.add_error_handler(ErrorHandler().get_handler())

            elif module_handler == GlobalFallbackHandler:
                application.add_handler(
                    GlobalFallbackHandler().get_handler(),
                    GlobalFallbackHandler().get_handler_group(),
                )
            elif module_handler == "CenterOrders":
                application.add_handler(orders.orders_handler)
            else:
                application.add_handlers(handlers=module_handler().get_handlers())

    def launch(self):
        # Ignore "per_message=False" ConversationHandler warning message
        filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
        self.setup_logging()

        persistence = PicklePersistence(filepath=self.filepath_persistence)

        application = (
            Application.builder()
            .token(self.token)
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .build()
        )

        # Call the method to add module handlers
        self.add_module_handlers(application)

        # TODO make the wiki objects compatible with inline queries
        # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

        application.run_polling()
