from configparser import ConfigParser


def load_constants():
    constants = ConfigParser()
    constants.read("resources/constants.ini")
    return constants
