#!/usr/bin/env python3

from . import (
    BotLauncher,
    BotConfigurationManager,
    ModuleManager,
    StartHandler,
    RestartHandler,
    WikiHandler,
    RequestHandler,
    DatabaseHandler,
    ErrorHandler,
    GlobalFallbackHandler,
    PromptValidatorHandler,
)
from . import TgModuleType, StdModuleType


def main(deployment: str = "local"):
    core_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/core/{deployment}.yaml"
    database_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/database/{deployment}.yaml"
    vector_database_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/vector_database/{deployment}.yaml"
    wiki_module_path = "/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/data/user/wiki/data.yaml"

    file_paths = [
        core_config,
        database_config,
        vector_database_config,
        wiki_module_path,
    ]
    bot_config_manager = BotConfigurationManager(file_paths)

    # NOTE you could make the module name part of the class, and turn these
    # dictionaries into lists. Then, inside the module manage, you can do
    # if module.name == TgModuleType.VECTOR_DATABASE
    tg_modules = {
        TgModuleType.GLOBAL_FALLBACK.value: GlobalFallbackHandler,
        TgModuleType.START.value: StartHandler,
        TgModuleType.RESTART.value: RestartHandler,
        TgModuleType.WIKI.value: WikiHandler,
        TgModuleType.REQUEST.value: RequestHandler,
        TgModuleType.PROMPT_VALIDATOR.value: PromptValidatorHandler,
        TgModuleType.DATABASE.value: DatabaseHandler,
        TgModuleType.ERROR_LOGGING.value: ErrorHandler,
    }
    std_modules = [StdModuleType.VECTOR_DATABASE]
    module_manager = ModuleManager(tg_modules, std_modules, bot_config_manager.config)

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
