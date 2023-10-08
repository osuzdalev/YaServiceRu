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
    GLOBAL_FALLBACK = "global_fallback"
    START = "start"
    RESTART = "restart"
    WIKI = "wiki"
    REQUEST = "request"
    PROMPT_VALIDATOR = "prompt_validator"
    DATABASE = "database"
    ERROR_LOGGING = "error_logging"


class StdModuleType(Enum):
    VECTOR_DATABASE = "vector_database"
