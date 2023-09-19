from src import (
    BotLauncher,
    BotConfigurationManager,
    ModuleManager,
    StartHandler,
    WikiHandler,
    RequestHandler,
    DatabaseHandler,
    ErrorHandler,
    GlobalFallbackHandler,
    PromptValidator,
    VectorDatabase
)

if __name__ == "__main__":
    tg_modules = {"start": StartHandler,
                  "wiki": WikiHandler,
                  "request": RequestHandler,
                  "database": DatabaseHandler,
                  "error_logging": ErrorHandler,
                  "global_fallback": GlobalFallbackHandler}
    std_modules = [PromptValidator, VectorDatabase]
    wiki_module_path = "data/command/wiki/data.yaml"
    module_manager = ModuleManager(tg_modules, std_modules, wiki_module_path)

    bot_config_manager = BotConfigurationManager("config/app/dev.yaml")

    bot_launcher = BotLauncher(bot_config_manager, module_manager)
    bot_launcher.launch()
