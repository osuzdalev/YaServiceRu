from src.common.app.bot_launcher import BotLauncher
from config.config_manager import ConfigurationManager


if __name__ == "__main__":
    config_manager = ConfigurationManager("src/config/main.yaml")
    bot_launcher = BotLauncher(config_manager)
    bot_launcher.launch()
