import sys
from pprint import pformat
import yaml
import os
from dotenv import load_dotenv

from loguru import logger

from pydantic import ValidationError

from .config_template import AppConfig
from ..common.yaml_loader import YamlLoader

load_dotenv()


def load_config(**kwargs) -> AppConfig:
    """
    Loads and processes configuration files for a Telegram bot.

    Reads configuration files, processes environment variables, and organizes the resulting
    configuration settings for use within the bot.

    Methods:
        _merge_configs(config1, config2): Merges two configuration dictionaries.
        _process_config(config_dict): Processes individual configuration settings.
        _process_env_vars(config_dict): Replaces placeholders with environment variable values.

    Expects keyword arguments where each key is a configuration type
    (e.g., 'core', 'database', 'vector_database', 'wiki') and each value
    is the path to the respective configuration file. The configuration
    files are read and their contents are merged into the internal config
    dictionary.

    Parameters:
    **kwargs: Keyword arguments where keys are configuration types and
              values are file paths to the respective YAML configuration files.
    """
    config = {}
    for config_type, file_path in kwargs.items():
        if config_type == "wiki":
            logger.info("Loading wiki configs")
            with open(file_path, mode="rb") as fp:
                new_config = {"wiki": yaml.load(fp, Loader=YamlLoader)}
                _merge_configs(config, new_config)
        else:
            with open(file_path, "r") as config_file:
                new_config = yaml.safe_load(config_file)
                _process_config(new_config)
                _merge_configs(config, new_config)
    try:
        return AppConfig(**config)
    except ValidationError as e:
        logger.error(f"Configuration validation error: {e}")
        sys.exit(1)


def _process_env_vars(config_dict):
    # Replace placeholders with environment variables
    for key, value in config_dict.items():
        if isinstance(value, str):
            config_dict[key] = os.getenv(value)
        elif isinstance(value, dict):
            _process_env_vars(value)


def _merge_configs(config1, config2):
    for key in config2:
        if (
                key in config1
                and isinstance(config1[key], dict)
                and isinstance(config2[key], dict)
        ):
            _merge_configs(config1[key], config2[key])
        else:
            config1[key] = config2[key]


def _process_config(config_dict):
    for key, value in config_dict.items():
        if isinstance(value, dict):
            if "secret" in value:
                _process_env_vars(value["secret"])

            # Recursive call to process nested dictionaries
            _process_config(value)
