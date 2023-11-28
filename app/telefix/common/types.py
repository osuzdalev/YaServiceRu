from enum import Enum


class HandlerGroupType(Enum):
    DB_MESSAGE_COLLECTION = -3
    RESTART = -2
    PROMPT_VALIDATION = -1
    CLIENT_BASIC = 0
    CLIENT_WIKI = 1
    CLIENT_PAY = 2
    CONTRACTOR_BASIC = 3
    CONTRACTOR_ASSIGN = 4
    GLOBAL_FALLBACK = 5


class TgModuleType(Enum):
    GLOBAL_FALLBACK = 0
    START = 1
    RESTART = 2
    WIKI = 3
    REQUEST = 4
    PROMPT_VALIDATOR = 5
    DATABASE = 6
    ERROR_LOGGING = 7
    CHATBOT = 8


class StdModuleType(Enum):
    VECTOR_DATABASE = 0
