from typing import Any, List, Dict, Tuple

from src.command.client.chatgpt.config import ChatGPTModelConfig


class ModuleManager:
    def __init__(self, tg_modules: Dict, modules: Dict, wiki_folder_path: str):
        self.modules = modules
        self.tg_modules = tg_modules
        self.wiki_folder_path = wiki_folder_path

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

    def get_prepped_tg_module_handlers(self) -> Tuple[List, Any]:
        """
        Prepares and returns the handlers for Telegram modules based on their configuration.

        For the majority of the modules, this method instantiates the handlers and prepares them
        for use with the given application. Specifically, it handles special cases like the
        `error_logging` module differently from others.

        Parameters:
        - global_fallback_ignore_messages_re (str): Regular expression to ignore messages for global fallback.
        - vector_database_model (Model): The model to be used with the `prompt_validator` module.

        Returns:
        - tuple: A tuple containing a list of normal handlers and the special error handler.
        """
        handlers = []
        error_handler = None
        commands, messages = self.get_tg_commands_messages()

        for module_name, module_handler in self.tg_modules.items():
            if module_name == "error_logging":
                error_handler = module_handler().get_handler()
            elif module_name == "global_fallback":
                global_fallback = module_handler(commands, messages)
                handlers.extend(global_fallback.get_handlers())
            elif module_name == "prompt_validator":
                prompt_validator = module_handler(
                    ChatGPTModelConfig(),
                    self.modules["vector_database"],
                    global_fallback.ignore_messages_re,
                )
                handlers.extend(prompt_validator.get_handlers())
            elif module_name == "wiki":
                handlers.extend(module_handler(self.wiki_folder_path).get_handlers())
            else:
                handlers.extend(module_handler().get_handlers())

        return handlers, error_handler
