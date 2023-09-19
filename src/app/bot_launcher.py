import logging
import os
import sys

from telegram import Update
from telegram.ext import Application, PicklePersistence
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from .bot_config_manager import BotConfigurationManager
from .module_manager import ModuleManager
from src.command.client.chatgpt.config import Model

# from src.command.center import orders
# from contractor import assign, complete, command


class BotLauncher:
    def __init__(
        self,
        bot_config_manager: BotConfigurationManager,
        module_manager: ModuleManager,
        log_level=logging.INFO,
    ):
        self.bot_config_manager = bot_config_manager
        self.module_manager = module_manager
        self.log_level = log_level

    def add_tg_module_handlers(self, application):
        commands, messages = self.module_manager.get_tg_commands_messages()
        for module_name, module_handler in self.module_manager.tg_modules.items():
            if module_name == "error_logging":
                application.add_error_handler(module_handler().get_handler())
            elif module_name == "global_fallback":
                global_fallback = module_handler(commands, messages)
                application.add_handlers(handlers=global_fallback.get_handlers())
            elif module_name == "prompt_validator":
                prompt_validator = module_handler(
                    Model(),
                    self.module_manager.modules["vector_database"],
                    global_fallback.ignore_messages_re,
                )
                application.add_handlers(handlers=prompt_validator.get_handlers())
            elif module_name == "wiki":
                application.add_handlers(
                    handlers=module_handler(
                        self.module_manager.wiki_folder_path
                    ).get_handlers()
                )
            else:
                application.add_handlers(handlers=module_handler().get_handlers())

    def setup_logging(self):
        logging.basicConfig(
            format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
            level=self.log_level,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(
                    self.bot_config_manager.config["yaserviceru"]["network"]["logs"],
                    mode="a",
                ),
            ],
        )

    async def post_init(self, application: Application) -> None:
        """
        Loading the configs into the app data_reader. This is done just after the init but before the run_polling()
        of the application.
        The configs in dict form is now accessible codebase wide.
        """
        application.bot_data["config"] = self.bot_config_manager.config
        application.bot_data["restart"] = False

    def launch(self):
        # Ignore "per_message=False" ConversationHandler warning message
        filterwarnings(
            action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
        )
        self.setup_logging()

        persistence = PicklePersistence(
            filepath=self.bot_config_manager.config["yaserviceru"]["network"][
                "persistence"
            ]
        )

        application = (
            Application.builder()
            .token(
                self.bot_config_manager.config["yaserviceru"]["secret"][
                    "token_telegram"
                ]
            )
            .persistence(persistence)
            .arbitrary_callback_data(True)
            .post_init(self.post_init)
            .build()
        )

        # Call the method to add module handlers
        self.add_tg_module_handlers(application)

        # TODO make the wiki objects compatible with inline queries
        # application.add_handler(wiki_share.share_inline_query_handler, CLIENT_WIKI)

        application.run_polling(allowed_updates=Update.ALL_TYPES)

        if application.bot_data["restart"]:
            os.execl(sys.executable, sys.executable, *sys.argv)
