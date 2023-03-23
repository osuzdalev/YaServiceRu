import logging
import sys
import yaml

from telethon.sync import TelegramClient
from telethon import events
from telegram.constants import ParseMode

from resources.constants_loader import load_constants
from clientcommands.wiki_module.telegram_website import Loader

# Enable logging
logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

CONSTANTS = load_constants()

api_id = int(CONSTANTS.get("API", "ID"))
api_hash = CONSTANTS.get("API", "HASH")
token = CONSTANTS.get("TOKEN", "MAIN_BOT")
main_id = chat_id = int(CONSTANTS.get("ID", "OLEG_RU"))
bot_id = CONSTANTS.get("USERNAME", "MAIN_BOT")

client = TelegramClient('test', api_id, api_hash)
