from telegram import Update
from telegram.ext import TypeHandler

from ..common.types import TgHandlerPriority, TgModuleType
from .database import collect_data


class DatabaseHandler:
    TYPE = TgModuleType.DATABASE

    def __init__(self):
        self.data_collection_handler = TypeHandler(Update, collect_data)
        # Note check if needs to be implemented once overall features done
        # collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
        # user_status_handler = ChatMemberHandler(user_status, ChatMemberHandler.CHAT_MEMBER)

    def get_handlers(self):
        return {TgHandlerPriority.DB_MESSAGE_COLLECTION: [self.data_collection_handler]}
