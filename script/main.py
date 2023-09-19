from src import BotLauncher
from src import BotConfigurationManager
from src import ModuleManager


if __name__ == "__main__":
    bot_config_manager = BotConfigurationManager("config/app/dev.yaml")
    module_manager = ModuleManager("config/module/test.yaml")
    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
