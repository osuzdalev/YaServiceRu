import yaml
from importlib import import_module


class ModuleManager:
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def load_modules(self):
        module_handlers = {}

        for module_category, module_info in self.config.items():
            if isinstance(module_info, dict) and 'handler_name' in module_info and 'location' in module_info:
                # Top-level module like 'database'
                module = import_module(module_info['location'])
                handler = getattr(module, module_info['handler_name'])
                module_handlers[module_category] = handler
            else:
                # Nested modules like 'command' and 'common'
                for module_name, nested_module_info in module_info.items():
                    module = import_module(nested_module_info['location'])
                    handler = getattr(module, nested_module_info['handler_name'])
                    module_handlers[module_name] = handler

        return module_handlers
