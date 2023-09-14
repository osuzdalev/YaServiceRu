import logging
import sys

from telegram.ext import Application, PicklePersistence
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from src.app.bot_config_manager import BotConfigurationManager
from src.app.module_manager import ModuleManager

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
                application.add_error_handler(module_handler.get_handler())
            else:
                application.add_handlers(handlers=module_handler.get_handlers())

    def setup_logging(self):
        logging.basicConfig(
            format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
            level=self.log_level,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(self.bot_config_manager.config["yaserviceru"]["network"]["logs"], mode="a"),
            ],
        )

    async def post_init(self, application: Application) -> None:
        """
        Loading the configs into the app data_reader. This is done just after the init but before the run_polling()
        of the application.
        The configs in dict form is now accessible codebase wide.
        """
        application.bot_data['config'] = self.bot_config_manager.config

    def launch(self):
        # Ignore "per_message=False" ConversationHandler warning message
        filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)
        self.setup_logging()

        persistence = PicklePersistence(filepath=self.bot_config_manager.config["yaserviceru"]["network"]["persistence"])

        application = (
            Application.builder()
            .token(self.bot_config_manager.config["yaserviceru"]["secret"]["token_telegram"])
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .post_init(self.post_init)
            .build()
        )

        # Call the method to add module handlers
        self.add_module_handlers(application)

        # TODO make the wiki objects compatible with inline queries
        # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

        application.run_polling()
