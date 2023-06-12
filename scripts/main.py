from src.common.app.bot_launcher import BotLauncher

from dotenv import load_dotenv


load_dotenv()

if __name__ == "__main__":
    bot_launcher = BotLauncher()
    bot_launcher.launch()
