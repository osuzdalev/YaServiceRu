#!/usr/bin/env python3

from loguru import logger

from .common.logging_setup import setup_logging

from . import (
    BotConfigurationManager,
    BotLauncher,
    DatabaseHandler,
    ErrorHandler,
    GlobalFallbackHandler,
    ModuleManager,
    PromptValidatorHandler,
    RequestHandler,
    RestartHandler,
    VectorDatabase,
    StartHandler,
    WikiHandler,
)


def main(deployment: str = "local"):
    log_level = "INFO"
    setup_logging(log_level)

    if deployment == "local":
        core_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/core/{deployment}.yaml"
        database_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/database/{deployment}.yaml"
        vector_database_config = f"/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/config/vector_database/{deployment}.yaml"
        wiki_module_path = "/Users/osuz/PycharmProjects/YaServiceRu/docker/app/image_files/data/user/wiki/data.yaml"
    else:
        core_config = f"/var/lib/config/core/{deployment}.yaml"
        database_config = f"/var/lib/config/database/{deployment}.yaml"
        vector_database_config = f"/var/lib/config/vector_database/{deployment}.yaml"
        wiki_module_path = "/var/lib/data/user/wiki/data.yaml"

    file_paths = [
        core_config,
        database_config,
        vector_database_config,
        wiki_module_path,
    ]
    bot_config_manager = BotConfigurationManager(file_paths)

    tg_modules = [
        GlobalFallbackHandler,
        StartHandler,
        RestartHandler,
        WikiHandler,
        RequestHandler,
        PromptValidatorHandler,
        DatabaseHandler,
        ErrorHandler,
    ]
    std_modules = [VectorDatabase]
    module_manager = ModuleManager(tg_modules, std_modules, bot_config_manager.config)

    bot_launcher = BotLauncher(bot_config_manager, module_manager, log_level)
    bot_launcher.launch()
