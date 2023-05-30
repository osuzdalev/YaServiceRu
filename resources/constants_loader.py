from configparser import ConfigParser
import os


def load_constants():
    constants = ConfigParser()
    constants_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "constants.ini"
    )
    constants.read(constants_path)
    return constants
