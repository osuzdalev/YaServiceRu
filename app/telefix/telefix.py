#!/usr/bin/env python3

import argparse
import pathlib
import sys
from warnings import filterwarnings

from loguru import logger

from telegram.warnings import PTBUserWarning

from .common.logging import setup_logging

from . import (
    BotLauncher,
    DatabaseHandler,
    ErrorHandler,
    GlobalFallbackHandler,
    load_config,
    ModuleManager,
    PromptValidatorHandler,
    RequestHandler,
    RestartHandler,
    VectorDatabase,
    StartHandler,
    WikiHandler,
)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--app_config_path",
        help="Application base configuration path",
        default="/app/config/dev",
    )
    parser.add_argument("-l", "--log_level", help="Logging level", default="INFO")
    args = parser.parse_args(argv or sys.argv)

    setup_logging(args.log_level)

    app_config_path = pathlib.Path(args.app_config_path)
    logger.info(f"Application config path: {app_config_path}")

    core_config = app_config_path / "core.yaml"
    database_config = app_config_path / "database.yaml"
    vector_database_config = app_config_path / "vector_database.yaml"
    wiki_module_path = app_config_path / "wiki.yaml"

    bot_config = load_config(
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
    module_manager = ModuleManager(
        tg_modules, std_modules, bot_config, args.log_level
    )

    # Ignore "per_message=False" ConversationHandler warning message
    filterwarnings(
        action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning
    )

    bot_launcher = BotLauncher(bot_config, module_manager, args.log_level)
    bot_launcher.launch()
