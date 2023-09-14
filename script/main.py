from src.app.bot_launcher import BotLauncher
from src.app.bot_config_manager import BotConfigurationManager
from src.app.module_manager import ModuleManager


if __name__ == "__main__":
    bot_config_manager = BotConfigurationManager("config/app/dev.yaml")
    module_manager = ModuleManager("config/module/test.yaml")
    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
