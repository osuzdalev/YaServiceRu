import yaml


class DataReader:
    def __init__(self, config: str):
        self.config = config
        self.chatgpt = ChatGPTDataReader(self.config)
        self.start = StartReader(self.config)


class ChatGPTDataReader:
    def __init__(self, config: str):
        self.config = config
        self.file_path: str = "data/command/chatgpt/data.yaml"
        with open(self.file_path, "r") as file:
            self.data = yaml.safe_load(file)

    def get_system_instructions(self):
        return self.data.get("system_instructions", {}).get(self.config, "").strip()

    def get_loading_gif(self):
        return self.data.get("loading_gif", {}).get(self.config, "").strip()


class StartReader:
    def __init__(self, config: str):
        self.config = config
        self.file_path: str = "data/command/start/data.yaml"
        with open(self.file_path, "r") as file:
            self.data = yaml.safe_load(file)

    def get_introduction_video(self):
        # Fetch the video ID based on the config value
        return self.data.get("video", {}).get(self.config, "").strip()
