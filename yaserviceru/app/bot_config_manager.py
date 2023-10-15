import yaml
import os
from dotenv import load_dotenv

load_dotenv()


class BotConfigurationManager:
    def __init__(self, base_path: str):
        self.config = None
        self.package_abs_path = base_path
        self.config_file_path = os.path.join(base_path, "config/app/dev.yaml")
        self._load_config_file()

    def _load_config_file(self):
        with open(self.config_file_path, "r") as config_file:
            self.config = yaml.safe_load(config_file)
            self._process_config(self.config)

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
