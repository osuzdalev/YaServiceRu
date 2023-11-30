#!/usr/bin/env python3

import argparse
import pathlib
from warnings import filterwarnings

from loguru import logger

from telegram.warnings import PTBUserWarning

from .common.logging import setup_logging

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--app_config_path",
        help="Application base configuration path",
        default="/app/telefix/config/dev",
    )
    parser.add_argument("-l", "--log_level", help="Logging level", default="INFO")
    args = parser.parse_args()

    setup_logging(args.log_level)

    app_config_path = pathlib.Path(args.app_config_path)
    logger.info(f"Application config path: {app_config_path}")

    core_config = app_config_path / "core.yaml"
    database_config = app_config_path / "database.yaml"
    vector_database_config = app_config_path / "vector_database.yaml"
    wiki_module_path = app_config_path / "wiki.yaml"

    bot_config_manager = BotConfigurationManager(
        core=core_config,
        database=database_config,
        vector_database=vector_database_config,
        wiki=wiki_module_path,
    )

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

    # Ignore "per_message=False" ConversationHandler warning message
    filterwarnings(
        action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
    )

    bot_launcher = BotLauncher(bot_config_manager, module_manager, args.log_level)
    bot_launcher.launch()
