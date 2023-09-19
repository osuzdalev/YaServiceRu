from src import (
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
    wiki_module_path = "data/command/wiki/data.yaml"
    module_manager = ModuleManager(tg_modules, std_modules, wiki_module_path)

    bot_config_manager = BotConfigurationManager("config/app/dev.yaml")

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
