import yaml
from importlib import import_module


class ModuleManager:
    def __init__(self, yaml_path):
        with open(yaml_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def load_modules(self):
        module_handlers = {}

        for category, modules in self.config['modules'].items():
            for module_name, module_info in modules.items():
                module = import_module(module_info['location'])
                handler = getattr(module, module_info['handler_name'])
                module_handlers[module_name] = handler

        return module_handlers
