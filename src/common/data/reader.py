class ChatGPTDataReader:
    def __init__(self):
        self.path_system_instructions: str = "data/chatgpt/system_instructions.txt"
        self.path_loading_gif: str = "data/chatgpt/loading_gif/file_id.txt"

    def get_system_instructions(self):
        with open(self.path_system_instructions, 'r') as file:
            return file.read()

    def get_loading_gif(self):
        with open(self.path_loading_gif, 'r') as file:
            return file.read()


class StartReader:
    def __init__(self):
        self.path_introduction_video: str = "data/start/file_id.txt"

    def get_introduction_video(self):
        with open(self.path_introduction_video, 'r') as file:
            return file.readline().strip()


class DataReader:
    def __init__(self):
        self.chatgpt = ChatGPTDataReader()
        self.start = StartReader()

