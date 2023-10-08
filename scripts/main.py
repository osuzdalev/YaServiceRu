#!/usr/bin/env python3

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

if __name__ == "__main__":
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
    wiki_module_path = "data/user/wiki/data.yaml"
    module_config = "config/module/test.yaml"
    module_manager = ModuleManager(
        tg_modules, std_modules, module_config, wiki_module_path
    )

    bot_config_manager = BotConfigurationManager("local", "config/app/dev.yaml")

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
