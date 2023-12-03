import os
import pathlib
from pprint import pprint
from typing import Dict
import yaml

from loguru import logger


class DataReader:
    """
    The DataReader class is designed for loading and handling data from YAML files.

    This class serves as a base class for various specialized data reader classes that
    are tailored for specific data handling needs in different contexts (like ChatGPTDataReader,
    StartReader, VectorDatabaseReader, etc.). It encapsulates the common functionality
    needed for reading data from YAML files, handling errors, and providing access to
    the data contents.

    The class is intended to be extended by subclasses that can utilize the loaded data
    for specific purposes, such as fetching system instructions, loading GIFs, or
    retrieving specific information relevant to the application's functionality.

    Each config (dev, main, ect ...) has its own specific data (video ID, ect ...).
    """

    def __init__(self, config: str, file_path: str):
        """
        Loads data from the specified YAML file.
        Handles file not found and YAML parsing errors gracefully.
        The `data` dict holds the data that are loaded from the YAML file.
        Params:
            - config (str): A configuration identifier used to specify different modes or
                            setups for reading data.
            - file_path (str): The path to the YAML file that contains the data.
        """
        self.config = config

        try:
            with open(file_path, "r") as file:
                self.data = yaml.safe_load(file)
        except (FileNotFoundError, IsADirectoryError, yaml.YAMLError) as e:
            logger.error(f"Error loading data from {file_path}: {e}")
            self.data = {}


class ChatGPTDataReader(DataReader):
    """
    The ChatGPTDataReader class extends the DataReader class, specifically
    tailored for handling ChatGPT-related configurations and data.

    This class is designed to read from a YAML file that contains specific
    configurations for the ChatGPT system, such as system instructions and
    URLs for loading GIFs.
    """

    def __init__(self, config: str, dir_path: pathlib):
        file_path = dir_path / "user/chatbot/data.yaml"
        super().__init__(config, file_path)

    def get_system_instructions(self):
        return self.data.get("system_instructions", {}).strip()

    def get_loading_gif(self):
        return self.data.get("loading_gif", {}).strip()


class StartReader(DataReader):
    """
    The StartReader class extends the DataReader class for handling specific data
    related to start-up processes, particularly fetching introduction video IDs.

    This class is tailored to read and process data from a specific YAML structure
    related to introduction videos. It is designed to work with YAML files that
    contain video IDs under different configurations (like 'dev' and 'main').

    Attributes:
    Inherits all attributes from the DataReader class.

    Methods:
    get_introduction_video: Retrieves the introduction video ID based on the
    current configuration value. The method looks up
    the 'video' key in the loaded data and returns the
    corresponding video ID for the given config.

    The YAML file structure expected by this class is as follows:
        video:
            dev: <video_id_for_dev_environment>
            main: <video_id_for_production_environment>

    where each environment (dev, main) has its own specific video ID.
    """

    def __init__(self, config: str, dir_path: pathlib):
        file_path = dir_path / "user/start/data.yaml"
        super().__init__(config, file_path)

    def get_introduction_video(self):
        # Fetch the video ID based on the config value
        return self.data.get("video", {}).get(self.config, "").strip()
