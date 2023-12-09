import pathlib
from typing import Any, List, Dict, Tuple

from loguru import logger

from .bot_config_manager import AppConfig

from ..vector_database import VectorDatabase
from ..user.chatbot import ChatGPTModelConfig
from ..common.types import TgModuleType, StdModuleType


class ModuleManager:
    """
    Manages the modules used in a Telegram bot application.

    This class is responsible for loading configuration files for modules, preparing
    standard and Telegram-specific module instances, and aggregating commands and messages
    associated with Telegram modules.
    """

    def __init__(
        self, tg_modules: List, std_modules: List, config: AppConfig, log_level: str
    ):
        """
        Params:
            std_modules (list): A list of standard modules used in the application.
            tg_modules (dict): Telegram-specific modules.
            config (dict): Stores the processed configuration settings for modules.
        """
        self.std_modules = std_modules
        self.std_module_instances = {}
        self.tg_modules = tg_modules
        self.config = config
        self.log_level = log_level

    def _init_std_module_objects(self) -> None:
        """
        Prepares and returns the instances for standard modules based on their configuration.

        For each of the standard modules, this method instantiates the instances and prepares them
        for use with the given application based on the configuration provided.

        Returns:
            - dict: A dictionary containing instances of each standard module.
        """
        for module in self.std_modules:
            if module.TYPE == StdModuleType.VECTOR_DATABASE:
                vector_database_config = self.config.vector_database
                vector_database_instance = VectorDatabase(
                    api_url=vector_database_config.api_url,
                    sentence_transformer=vector_database_config.sentence_transformer,
                    semantic_threshold=vector_database_config.semantic_threshold,
                    query_limit=vector_database_config.query_limit,
                    classes_config=vector_database_config.classes,
                    filters_config=vector_database_config.filters,
                )
                self.std_module_instances[
                    StdModuleType.VECTOR_DATABASE
                ] = vector_database_instance

    def _get_tg_commands_and_messages(self) -> Tuple[List, List]:
        """
        Retrieves the commands and messages associated with each Telegram module.

        This method iterates through all the registered Telegram modules and aggregates
        their associated commands and messages, if any.

        Returns:
        - tuple: A tuple containing two lists:
            1. List of all commands associated with the Telegram modules.
            2. List of all messages associated with the Telegram modules.
        """
        all_commands = []
        all_messages = []
        for module in self.tg_modules:
            all_commands.extend(getattr(module, "COMMANDS", []))
            all_messages.extend(getattr(module, "MESSAGES", []))
        logger.info(f"COMMANDS: {all_commands}")
        logger.info(f"MESSAGES: {all_messages}")

        return all_commands, all_messages

    def get_tg_module_handlers(self) -> Tuple[List, Any]:
        """
        Prepares and returns the instances for Telegram modules based on their configuration.

        For the majority of the modules, this method instantiates the instances and prepares them
        for use with the given application. Specifically, it handles special cases like the
        `error_logging` module differently from others.

        Returns:
        - tuple: A tuple containing a list of normal instances and the special error handler.
        """
        self._init_std_module_objects()
        commands, messages = self._get_tg_commands_and_messages()
        tg_modules = {module.TYPE: module for module in self.tg_modules}

        error_handler_type = tg_modules.pop(TgModuleType.ERROR_LOGGING)
        error_handler = error_handler_type(
            self.config.core.contact.email.smtp.url,
            self.config.core.contact.email.smtp.port,
            self.log_level,
        )

        global_fallback_type = tg_modules.pop(TgModuleType.GLOBAL_FALLBACK)
        global_fallback = global_fallback_type(commands, messages)
        handlers = [global_fallback]

        for module in tg_modules.values():
            if module.TYPE == TgModuleType.PROMPT_VALIDATOR:
                prompt_validator = module(
                    ChatGPTModelConfig(
                        self.config.deployment,
                        pathlib.Path(self.config.core.media),
                    ),
                    self.std_module_instances[StdModuleType.VECTOR_DATABASE],
                    global_fallback.ignore_messages_re,
                )
                handlers.append(prompt_validator)
            elif module.TYPE == TgModuleType.START:
                handlers.append(
                    module(
                        self.config.deployment,
                        pathlib.Path(self.config.core.media),
                    )
                )
            elif module.TYPE == TgModuleType.WIKI:
                logger.warning(f"Media path: {self.config.core.media}")
                handlers.append(
                    module(
                        self.config.wiki,
                        pathlib.Path(self.config.core.media),
                    )
                )
            elif module.TYPE == TgModuleType.CHATBOT:
                handlers.append(
                    module(
                        self.config.deployment,
                        pathlib.Path(self.config.core.media),
                        global_fallback.ignore_messages_re,
                    )
                )
            else:
                handlers.append(module())

        return handlers, error_handler
