import yaml
import os
from dotenv import load_dotenv

load_dotenv()


class BotConfigurationManager:
    """
    Manages the loading and processing of configuration files for a Telegram bot.

    This class is responsible for reading configuration files, processing environment
    variables, and organizing the resulting configuration settings for use within the bot.

    Attributes:
        config (dict): Stores the processed configuration settings.
        package_abs_path (str): Absolute path of the package.
        files_paths (list): Paths to the configuration files.

    Methods:
        _load_config_files(): Loads and processes configuration files.
        _merge_configs(config1, config2): Merges two configuration dictionaries.
        _process_config(config_dict): Processes individual configuration settings.
        _update_data_paths(data_dict): Updates paths in the configuration with absolute paths.
        _process_env_vars(config_dict): Replaces placeholders with environment variable values.
    """

    def __init__(self, base_path: str, files_paths: list):
        self.config = {}
        self.package_abs_path = base_path
        self.files_paths = files_paths
        self._load_config_files()

    def _load_config_files(self):
        for file_path in self.files_paths:
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

                if "bot_persistence" in value:
                    self._update_data_paths(value["bot_persistence"])

                # Recursive call to process nested dictionaries
                self._process_config(value)

    def _update_data_paths(self, data_dict):
        print("data_dict: ", data_dict)
        for key, file_path in data_dict.items():
            # Create absolute path
            abs_path = os.path.join(self.package_abs_path, file_path)
            # Update the file path in the configuration
            data_dict[key] = abs_path
            print("abs_path: ", abs_path)

    def _process_env_vars(self, config_dict):
        # Replace placeholders with environment variables
        for key, value in config_dict.items():
            if isinstance(value, str):
                config_dict[key] = os.getenv(value)
            elif isinstance(value, dict):
                self._process_env_vars(value)
