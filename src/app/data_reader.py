from pprint import pprint

import yaml


class DataReader:
    def __init__(self, config: str, file_path: str):
        self.config = config
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, "r") as file:
                return yaml.safe_load(file)
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"Error loading data from {self.file_path}: {e}")
            return {}


class ChatGPTDataReader(DataReader):
    def __init__(self, config: str, file_path: str = "data/command/chatgpt/data.yaml"):
        super().__init__(config, file_path)

    def get_system_instructions(self):
        return self.data.get("system_instructions", {}).get(self.config, "").strip()

    def get_loading_gif(self):
        return self.data.get("loading_gif", {}).get(self.config, "").strip()


class StartReader(DataReader):
    def __init__(self, config: str, file_path: str = "data/command/start/data.yaml"):
        super().__init__(config, file_path)

    def get_introduction_video(self):
        # Fetch the video ID based on the config value
        return self.data.get("video", {}).get(self.config, "").strip()


class VectorDatabaseReader(DataReader):
    def __init__(
        self, config: str = None, file_path: str = "data/vector_database/data.yaml"
    ):
        super().__init__(config, file_path)

    def get_filters(self):
        return self.data.get("filters", {})

    def get_classes(self):
        return self.data.get("classes", {})
