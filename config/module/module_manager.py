import yaml
from importlib import import_module


class ModuleManager:
    def __init__(self, yaml_path):
        self.commands = {}
        self.messages = {}
        self.location = {}
        self.handler_name = {}
        self.config = self._load_yaml(yaml_path)
        self._populate_dict()

    def _load_yaml(self, yaml_path):
        with open(yaml_path, 'r') as file:
            return yaml.safe_load(file)

    def _populate_dict(self):
        for module_name, module_info in self.config.items():
            self.location[module_name] = module_info['location']
            self.handler_name[module_name] = module_info['handler_name']
            if 'command' in module_info:
                self.commands[module_name] = module_info['command']
            if 'message' in module_info:
                self.messages[module_name] = module_info['message']

    def load_modules(self):
        module_handlers = {}

        # Accumulate all commands and messages
        all_commands = []
        all_messages = []
        for module_info in self.config.values():
            all_commands.extend(module_info.get('command', []))
            all_messages.extend(module_info.get('message', []))

        for module_name in self.config:
            module = import_module(self.location[module_name])

            # special module that needs all commands and messages
            if module_name == 'global_fallback':
                kwargs = {
                    'commands': all_commands,
                    'messages': all_messages
                }
            else:
                # Prepare the kwargs for initialization for other modules
                kwargs = {}
                if 'command' in self.config[module_name]:
                    kwargs['commands'] = self.config[module_name]['command']
                if 'message' in self.config[module_name]:
                    kwargs['messages'] = self.config[module_name]['message']

            handler_class = getattr(module, self.handler_name[module_name])

            # Use **kwargs to pass commands and messages if they exist
            handler_instance = handler_class(**kwargs)
            module_handlers[module_name] = handler_instance

        return module_handlers

