from typing import Any, List, Dict, Tuple
import yaml

from src.command.client.chatgpt.config import ChatGPTModelConfig
from src.app.data_reader import VectorDatabaseReader


class ModuleManager:
    def __init__(
        self,
        tg_modules: Dict,
        std_modules: Dict,
        config_file_path: str,
        wiki_folder_path: str,
    ):
        self.std_modules = std_modules
        self.std_module_objects = {}
        self.tg_modules = tg_modules
        self.config_file_path = config_file_path
        self.config = None
        self.wiki_folder_path = wiki_folder_path
        self._load_config_file()

    def _load_config_file(self):
        with open(self.config_file_path, "r") as config_file:
            self.config = yaml.safe_load(config_file)

    def get_prepped_std_module_objects(self) -> None:
        """
        Prepares and returns the instances for standard modules based on their configuration.

        For each of the standard modules, this method instantiates the instances and prepares them
        for use with the given application based on the configuration provided.

        Returns:
        - dict: A dictionary containing instances of each standard module.
        """
        for module_name, module_class in self.std_modules.items():
            if module_name == "vector_database":
                vector_database_data_reader = VectorDatabaseReader("test")
                vector_database_object = module_class(
                    api_url=self.config["vector_database"]["api_url"],
                    sentence_transformer=self.config["vector_database"][
                        "sentence_transformer"
                    ],
                    semantic_threshold=self.config["vector_database"][
                        "semantic_threshold"
                    ],
                    query_limit=self.config["vector_database"]["query_limit"],
                )
                vector_database_object.populate_vector_database(
                    vector_database_data_reader.get_classes(),
                    vector_database_data_reader.get_filters(),
                )
                self.std_module_objects["vector_database"] = vector_database_object

    def get_tg_commands_messages(self) -> Tuple[List, List]:
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
        for module_name, module_handler in self.tg_modules.items():
            all_commands.extend(getattr(module_handler, "commands", []))
            all_messages.extend(getattr(module_handler, "messages", []))

        return all_commands, all_messages

    def get_prepped_tg_module_objects(self) -> Tuple[List, Any]:
        """
        Prepares and returns the instances for Telegram modules based on their configuration.

        For the majority of the modules, this method instantiates the instances and prepares them
        for use with the given application. Specifically, it handles special cases like the
        `error_logging` module differently from others.

        Returns:
        - tuple: A tuple containing a list of normal instances and the special error handler.
        """
        # Prepare the std_modules object instances
        self.get_prepped_std_module_objects()

        handlers = []
        error_handler = None
        commands, messages = self.get_tg_commands_messages()

        for module_name, module_handler in self.tg_modules.items():
            if module_name == "error_logging":
                error_handler = module_handler()
            elif module_name == "global_fallback":
                global_fallback = module_handler(commands, messages)
                handlers.insert(0, global_fallback)
            elif module_name == "prompt_validator":
                prompt_validator = module_handler(
                    ChatGPTModelConfig(),
                    self.std_module_objects["vector_database"],
                    global_fallback.ignore_messages_re,
                )
                handlers.append(prompt_validator)
            elif module_name == "wiki":
                handlers.append(module_handler(self.wiki_folder_path))
            else:
                handlers.append(module_handler())

        return handlers, error_handler
