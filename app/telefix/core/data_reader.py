import inspect
import os
import logging
from pprint import pprint
from typing import Dict
import yaml

logger_data_reader = logging.getLogger(__name__)


class DataReader:
    """
    The DataReader class is designed for loading and handling data from YAML files.

    This class serves as a base class for various specialized data reader classes that
    are tailored for specific data handling needs in different contexts (like ChatGPTDataReader,
    StartReader, VectorDatabaseReader, etc.). It encapsulates the common functionality
    needed for reading data from YAML files, handling errors, and providing access to
    the data contents.

    Attributes:
        config (str): A configuration identifier used to specify different modes or
                      setups for reading data.
        file_path (str): The path to the YAML file that contains the data.
        data (dict): A dictionary holding the data loaded from the YAML file.

    Methods:
        _load_data: A private method to load data from the specified YAML file. It handles
                    file not found and YAML parsing errors gracefully.

    The class is intended to be extended by subclasses that can utilize the loaded data
    for specific purposes, such as fetching system instructions, loading GIFs, or
    retrieving specific information relevant to the application's functionality.

    Each config (dev, main, ect ...) has its own specific data (video ID, ect ...).
    """

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
    """
    The ChatGPTDataReader class extends the DataReader class, specifically
    tailored for handling ChatGPT-related configurations and data.

    This class is designed to read from a YAML file that contains specific
    configurations for the ChatGPT system, such as system instructions and
    URLs for loading GIFs.
    """

    def __init__(
        self, config: str, file_path: str = "telefix/data/user/chatbot/data.yaml"
    ):
        super().__init__(config, file_path)

    def get_system_instructions(self):
        return self.data.get("system_instructions", {}).get(self.config, "").strip()

    def get_loading_gif(self):
        return self.data.get("loading_gif", {}).get(self.config, "").strip()


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

    def __init__(
        self, config: str, file_path: str = "telefix/data/user/start/data.yaml"
    ):
        super().__init__(config, file_path)

    def get_introduction_video(self):
        # Fetch the video ID based on the config value
        return self.data.get("video", {}).get(self.config, "").strip()


class VectorDatabaseReader(DataReader):
    """
    The VectorDatabaseReader class extends DataReader to handle data related to
    vector databases, specifically for managing classes and filters.

    This class is specialized for reading YAML files that define classes and filters
    used in a vector database context. It processes data for different types of filters
    (like EnglishFilters, RussianFilters, SpecialSubjectFilters), each with its
    specific configurations, descriptions, properties, and vectorization strategies.

    Attributes:
        Inherits all attributes from the DataReader class.

    Methods:
        get_filters: Returns a dictionary of filter data, with keys as filter names
                     and values as lists of filter strings.
        get_classes: Returns a dictionary of class data, where each key is a class
                     name, and the value is a dictionary containing class details
                     like descriptions, properties, vectorizers, and module configurations.

    This class is crucial for initializing and configuring components that handle
    vectorized data processing in various language and domain-specific contexts.
    """

    def __init__(
        self,
        config: str = None,
        file_path: str = "telefix/data/vector_database/data.yaml",
    ):
        super().__init__(config, file_path)

    def get_filters(self) -> Dict[str, Dict]:
        logger_data_reader.info(f"{inspect.currentframe().f_code.co_name}")
        return self.data.get("filters", {})

    def get_classes(self) -> Dict[str, Dict]:
        logger_data_reader.info(f"{inspect.currentframe().f_code.co_name}")
        return self.data.get("classes", {})
