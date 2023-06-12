from telegram import Update
from telegram.ext import (
    ChatMemberHandler,
    MessageHandler,
    filters,
    TypeHandler,
)

from src.common.types import HandlerGroupType
from .collector import collect_data, collect_phone_number, user_status


class CollectorHandler:
    def __init__(self):
        self.data_collection_handler = TypeHandler(Update, collect_data)
        # TODO
        # collection_phone_number_handler = MessageHandler(filters.CONTACT, collect_phone_number)
        # user_status_handler = ChatMemberHandler(user_status, ChatMemberHandler.CHAT_MEMBER)

    def get_handlers(self):
        return {
            HandlerGroupType.MESSAGE_COLLECTION.value: [self.data_collection_handler]
        }
