import logging
import os
import sys

from loguru import logger

from telegram import Update
from telegram.ext import Application, PicklePersistence

from .bot_config_manager import BotConfigurationManager
from .module_manager import ModuleManager

from ..common.logging import InterceptHandler, logging_format

# from telefix.user.admin import orders
# from contractor import assign, complete, user


class BotLauncher:
    """
    Manages the initialization and launch of a Telegram bot application.

    This class handles the configuration and setup of a Telegram bot application,
    including logging setup, adding module handlers, and managing post-initialization
    activities. It also provides functionality to restart the application if needed.

    Attributes:
        bot_config_manager (BotConfigurationManager): Manages the bot's configuration settings.
        module_manager (ModuleManager): Manages the modules that add functionality to the bot.
        log_level (logging.Level): Specifies the logging level for the application.

    Methods:
        add_tg_module_handlers(application): Adds Telegram module handlers to the application.
        setup_logging(): Sets up logging with specified format and handlers.
        post_init(application): Loads configurations into core data_reader after initialization.
        launch(): Initializes and starts the bot application, handling restarts if necessary.
    """

    def __init__(
        self,
        bot_config_manager: BotConfigurationManager,
        module_manager: ModuleManager,
        log_level: str = "INFO",
    ):
        self.bot_config_manager = bot_config_manager
        self.module_manager = module_manager
        self.log_level = log_level

    def launch(self):
        self.setup_logging()

        persistence = PicklePersistence(
            filepath=self.bot_config_manager.config["telefix"]["persistence"]
        )

        application = (
            Application.builder()
            .token(
                self.bot_config_manager.config["telefix"]["secret"]["token_telegram"]
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

    def setup_logging(self):
        """
        Set up the logging for the application. Both the standard library and the loguru. Loguru intercepts the logs
        from the standard one and reformats them accordingly.
        That is necessary because the PTB is written using the standard lib.

        This method configures the logging for the application by:
        1. Setting up a file logger with a specified file path derived from the application's configurations.
        2. Configuring the push notifications for logging errors using both Pushover and Telegram.

        Note:
            The logging is set up using an external logging library.
            Ensure the library is properly installed and imported before calling this method.
        """

        # Loguru file logger
        logger.add(
            self.bot_config_manager.config["telefix"]["logs"],
            level=f"{self.log_level}",
            colorize=False,
            serialize=False,
            format=logging_format,
        )

        # Initialize the standard logging
        logging.basicConfig(
            format="[%(asctime)s] [%(levelname)s] [%(name)s | %(funcName)s() | line %(lineno)d] %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=self.log_level,
            handlers=[InterceptHandler()],
        )

    async def post_init(self, application: Application) -> None:
        """
        Loading the configs into the core data_reader. This is done just after the init but before the run_polling()
        of the application.
        The configs in dict form are now accessible codebase wide.
        """
        application.bot_data["config"] = self.bot_config_manager.config
        application.bot_data["restart"] = False

    def add_tg_module_handlers(self, application: Application) -> None:
        """
        Adds Telegram module handlers to the given application.

        This method fetches the prepared handlers from the ModuleManager and appropriately adds
        them to the application. It handles the addition of normal handlers as well as the special
        error handler.

        Parameters:
            - application (object): The target telegram application to which the handlers will be added.

        Returns:
            - None
        """
        handlers, error_handler = self.module_manager.get_tg_module_handlers()

        application.add_error_handler(error_handler.get_handler())
        for handler in handlers:
            logger.info(f"Adding {handler.TYPE}")
            application.add_handlers(handlers=handler.get_handlers())
