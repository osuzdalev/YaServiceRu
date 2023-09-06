import logging
import sys

from telegram.ext import Application, PicklePersistence
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from config.bot_config_manager import BotConfigurationManager
from config.modules.module_manager import ModuleManager

# from src.command.center import orders
# from contractor import assign, complete, command


class BotLauncher:
    def __init__(
            self,
            bot_config_manager: BotConfigurationManager,
            module_manager: ModuleManager,
            log_level=logging.INFO
    ):
        self.bot_config_manager = bot_config_manager
        self.module_manager = module_manager
        self.log_level = log_level

    def add_module_handlers(self, application):
        modules = self.module_manager.load_modules()
        for module_name, module_handler in modules.items():
            if module_name == "error_logging":
                application.add_error_handler(module_handler().get_handler())
            elif module_name == "global_fallback":
                application.add_handler(
                    module_handler().get_handler(),
                    module_handler().get_handler_group(),
                )
            else:
                application.add_handlers(handlers=module_handler().get_handlers())

    def setup_logging(self):
        logging.basicConfig(
            format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
            level=self.log_level,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.bot_config_manager.config["technical"]["filepath"]["logger"], mode="a"),
            ],
        )

    def launch(self):
        # Ignore "per_message=False" ConversationHandler warning message
        filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
        self.setup_logging()

        persistence = PicklePersistence(filepath=self.bot_config_manager.config["technical"]["filepath"]["persistence"])

        application = (
            Application.builder()
            .token(self.bot_config_manager.config["secret"]["token_telegram"])
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .build()
        )

        # Call the method to add modules handlers
        self.add_module_handlers(application)

        # TODO make the wiki objects compatible with inline queries
        # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

        application.run_polling()
