from dotenv import load_dotenv

from src.common.app.bot_launcher import BotLauncher

load_dotenv()


if __name__ == "__main__":
    load_dotenv()
    bot_launcher = BotLauncher()
    bot_launcher.launch()
