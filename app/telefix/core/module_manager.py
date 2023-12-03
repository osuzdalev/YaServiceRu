import pathlib
from typing import Any, List, Dict, Tuple

from ..vector_database import VectorDatabase
from ..user.chatbot import ChatGPTModelConfig
from ..common.types import TgModuleType, StdModuleType


class ModuleManager:
    """
    Manages the modules used in a Telegram bot application.

    This class is responsible for loading configuration files for modules, preparing
    standard and Telegram-specific module instances, and aggregating commands and messages
    associated with Telegram modules.

    Methods:
        _init_std_module_objects(): Prepares and returns instances of standard modules.
        _get_tg_commands_and_messages(): Retrieves commands and messages for Telegram modules.
        get_tg_module_handlers(): Prepares and returns instances of Telegram modules.
    """

    def __init__(
        self, tg_modules: List, std_modules: List, config: Dict, log_level: str
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
                vector_database_instance = VectorDatabase(
                    api_url=self.config["vector_database"]["api_url"],
                    sentence_transformer=self.config["vector_database"][
                        "sentence_transformer"
                    ],
                    semantic_threshold=self.config["vector_database"][
                        "semantic_threshold"
                    ],
                    query_limit=self.config["vector_database"]["query_limit"],
                    classes_config=self.config["vector_database"]["classes"],
                    filters_config=self.config["vector_database"]["filters"],
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
            all_commands.extend(getattr(module, "commands", []))
            all_messages.extend(getattr(module, "messages", []))

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
        # Prepare the std_modules object instances
        self._init_std_module_objects()

        handlers = []
        error_handler = None
        global_fallback = None
        commands, messages = self._get_tg_commands_and_messages()

        for module in self.tg_modules:
            if module.TYPE == TgModuleType.GLOBAL_FALLBACK:
                global_fallback = module(commands, messages)
                handlers.insert(0, global_fallback)
            elif module.TYPE == TgModuleType.PROMPT_VALIDATOR:
                prompt_validator = module(
                    ChatGPTModelConfig(
                        self.config["deployment"],
                        pathlib.Path(self.config["telefix"]["media"]),
                    ),
                    self.std_module_instances[StdModuleType.VECTOR_DATABASE],
                    global_fallback.ignore_messages_re,
                )
                handlers.append(prompt_validator)
            elif module.TYPE == TgModuleType.START:
                handlers.append(
                    module(
                        self.config["deployment"],
                        pathlib.Path(self.config["telefix"]["media"]),
                    )
                )
            elif module.TYPE == TgModuleType.WIKI:
                handlers.append(module(self.config["wiki"]))
            elif module.TYPE == TgModuleType.CHATBOT:
                handlers.append(
                    module(
                        self.config["deployment"],
                        pathlib.Path(self.config["telefix"]["media"]),
                        global_fallback.ignore_messages_re,
                    )
                )
            elif module.TYPE == TgModuleType.ERROR_LOGGING:
                error_handler = module(
                    self.config["telefix"]["contact"]["email"]["smtp"]["url"],
                    self.config["telefix"]["contact"]["email"]["smtp"]["port"],
                    self.log_level,
                )
            else:
                handlers.append(module())

        return handlers, error_handler
