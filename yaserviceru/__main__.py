#!/usr/bin/env python3
import os

from yaserviceru import (
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
from yaserviceru.common.types import TgModuleType, StdModuleType


def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    print("BASE PATH: ", base_path)
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
    wiki_module_path = os.path.join(base_path, "data/user/wiki/data.yaml")
    print("wiki_module_path PATH: ", wiki_module_path)
    module_config = os.path.join(base_path, "config/module/dev.yaml")
    module_manager = ModuleManager(
        tg_modules, std_modules, module_config, wiki_module_path
    )

    bot_config_path = os.path.join(base_path, "config/app/dev.yaml")
    bot_config_manager = BotConfigurationManager(base_path)

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()


if __name__ == "__main__":
    main()
