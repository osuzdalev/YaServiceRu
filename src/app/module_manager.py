from typing import List, Dict, Tuple


class ModuleManager:
    def __init__(self, tg_modules: Dict, modules: Dict, wiki_folder_path: str):
        self.modules = modules
        self.tg_modules = tg_modules
        self.wiki_folder_path = wiki_folder_path

    def get_tg_commands_messages(self) -> Tuple[List, List]:
        all_commands = []
        all_messages = []
        for module_name, module_handler in self.tg_modules.items():
            all_commands.extend(getattr(module_handler, "commands", []))
            all_messages.extend(getattr(module_handler, "messages", []))

        return all_commands, all_messages
