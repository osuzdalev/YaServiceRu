import yaml
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigurationManager:
    def __init__(self, config_file_path):
        self.config = None
        self.config_file_path = config_file_path
        self._load_config_file()

    def _load_config_file(self):
        with open(self.config_file_path, 'r') as config_file:
            self.config = yaml.safe_load(config_file)
            self._process_env_vars(self.config['secret'])  # Process only 'secret' section

    def _process_env_vars(self, config_dict):
        # Replace placeholders with environment variables
        for key, value in config_dict.items():
            if isinstance(value, str):
                config_dict[key] = os.getenv(value)
            elif isinstance(value, dict):
                self._process_env_vars(value)
