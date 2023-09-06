from pprint import pprint
from src.common.app.bot_launcher import BotLauncher
from config.bot_config_manager import BotConfigurationManager
from config.modules.module_manager import ModuleManager


if __name__ == "__main__":
    bot_config_manager = BotConfigurationManager("config/dev.yaml")
    module_manager = ModuleManager("config/modules/test.yaml")
    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
