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

    def get_prepped_tg_module_objects(self) -> Tuple[List, Any]:
        """
        Prepares and returns the instances for Telegram modules based on their configuration.

        For the majority of the modules, this method instantiates the instances and prepares them
        for use with the given application. Specifically, it handles special cases like the
        `error_logging` module differently from others.

        Returns:
        - tuple: A tuple containing a list of normal instances and the special error handler.
        """
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
                    self.modules["vector_database"],
                    global_fallback.ignore_messages_re,
                )
                handlers.append(prompt_validator)
            elif module_name == "wiki":
                handlers.append(module_handler(self.wiki_folder_path))
            else:
                handlers.append(module_handler())

        return handlers, error_handler
