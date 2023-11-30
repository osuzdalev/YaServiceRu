import yaml
import os
from dotenv import load_dotenv

from loguru import logger

from ..common.yaml_loader import YamlLoader

load_dotenv()


class BotConfigurationManager:
    """
    Manages the loading and processing of configuration files for a Telegram bot.

    Responsible for reading configuration files, processing environment variables,
    and organizing the resulting configuration settings for use within the bot.

    Attributes:
        config (dict): Stores the processed configuration settings.

    Methods:
        _merge_configs(config1, config2): Merges two configuration dictionaries.
        _process_config(config_dict): Processes individual configuration settings.
        _process_env_vars(config_dict): Replaces placeholders with environment variable values.
    """

    def __init__(self, **kwargs):
        """
        Expects keyword arguments where each key is a configuration type
        (e.g., 'core', 'database', 'vector_database', 'wiki') and each value
        is the path to the respective configuration file. The configuration
        files are read and their contents are merged into the internal config
        dictionary.

        Parameters:
        **kwargs: Keyword arguments where keys are configuration types and
                  values are file paths to the respective YAML configuration files.
        """
        self.config = {}

        for config_type, file_path in kwargs.items():
            if config_type == "wiki":
                logger.info("Loading wiki configs")
                with open(file_path, mode="rb") as fp:
                    config = yaml.load(fp, Loader=YamlLoader)
                    config = {"wiki": config}
                    self._merge_configs(self.config, config)
            else:
                with open(file_path, "r") as config_file:
                    config = yaml.safe_load(config_file)
                    self._process_config(config)
                    self._merge_configs(self.config, config)

    def _merge_configs(self, config1, config2):
        for key in config2:
            if (
                key in config1
                and isinstance(config1[key], dict)
                and isinstance(config2[key], dict)
            ):
                self._merge_configs(config1[key], config2[key])
            else:
                config1[key] = config2[key]

    def _process_config(self, config_dict):
        for key, value in config_dict.items():
            if isinstance(value, dict):
                if "secret" in value:
                    self._process_env_vars(value["secret"])

                # Recursive call to process nested dictionaries
                self._process_config(value)

    def _process_env_vars(self, config_dict):
        # Replace placeholders with environment variables
        for key, value in config_dict.items():
            if isinstance(value, str):
                config_dict[key] = os.getenv(value)
            elif isinstance(value, dict):
                self._process_env_vars(value)
