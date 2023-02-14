from configparser import ConfigParser
import logging
import sys

from telethon.sync import TelegramClient, events

# Enable logging
logging.basicConfig(
    format="[%(asctime)s] {%(name)s:%(lineno)d} %(levelname)s - %(message)s",
    level=logging.INFO,
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

CONSTANTS = ConfigParser()
CONSTANTS.read("../constants.ini")

api_id = int(CONSTANTS.get("API", "ID"))
api_hash = CONSTANTS.get("API", "HASH")
token = CONSTANTS.get("TOKEN", "MAIN_BOT")
main_id = chat_id = int(CONSTANTS.get("ID", "OLEG_RU"))
bot_id = CONSTANTS.get("USERNAME", "YaServiceRuDevBot")

client = TelegramClient('test', api_id, api_hash)
