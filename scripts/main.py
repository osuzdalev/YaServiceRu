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
    VectorDatabase,
)

if __name__ == "__main__":
    # TODO move the module names into enumerations
    # NOTE you could make the module name part of the class, and turn these
    # dictionaries into lists. Then, inside the module manage, you can do
    # if module.name == ModuleType.VECTOR_DATABASE
    tg_modules = {
        "global_fallback": GlobalFallbackHandler,
        "start": StartHandler,
        "restart": RestartHandler,
        "wiki": WikiHandler,
        "request": RequestHandler,
        "prompt_validator": PromptValidatorHandler,
        "database": DatabaseHandler,
        "error_logging": ErrorHandler,
    }
    std_modules = {"vector_database": VectorDatabase}
    wiki_module_path = "data/user/wiki/data.yaml"
    module_config = "config/module/test.yaml"
    module_manager = ModuleManager(
        tg_modules, std_modules, module_config, wiki_module_path
    )

    bot_config_manager = BotConfigurationManager("config/app/dev.yaml")

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
