from telegram import Update
from telegram.ext import (
    TypeHandler,
)

from ..common.types import HandlerGroupType
from .database import collect_data


class DatabaseHandler:
    def __init__(self):
        self.data_collection_handler = TypeHandler(Update, collect_data)
        # Note check if needs to be implemented once overall features done
        # collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
        # user_status_handler = ChatMemberHandler(user_status, ChatMemberHandler.CHAT_MEMBER)

    def get_handlers(self):
        return {
            HandlerGroupType.DB_MESSAGE_COLLECTION.value: [self.data_collection_handler]
        }
