"""Python script defining dedicated functions to interact with the wiki JSON file"""
import logging
import json
from typing import Union

logger_wiki_json_utils = logging.getLogger(__name__)


def backup(current_file: dict, backup_file: str = 'wiki_data_backup.json') -> None:
    """Saves the current JSON File with which the bot interacts to a backup file.
    Used before any twicking as a precaution"""
    logger_wiki_json_utils.info("backup()")
    with open(backup_file, "w") as back_file_handle:
        json.dump(current_file, back_file_handle, indent=4, sort_keys=True, ensure_ascii=False)


# TODO figure out how to not use the absolute path
#  yet make this file available to both those in this directory and main.py
def get_wiki_json_dict(dict_path: str = '/Users/osuz/PycharmProjects/YaServiceRu/clientcommands/wiki_module/wiki_data.json') -> dict:
    """Get a copy of the current JSON file to access data"""
    logger_wiki_json_utils.info("get_wiki_json_dict()")
    with open(dict_path, "r") as json_file:
        # Load the data from the file into a Python dictionary
        data_dict = json.loads(json_file.read())
    
    return data_dict


WIKI_DATA_DICT = get_wiki_json_dict()


def get_answer_path(value: str, data_dict: dict = None, path: str = "") -> Union[str, None]:
    """Returns the path inside the JSON to a particular key as a string.
    The string is formatted to look good when sent in Telegram
    :rtype: object"""
    logger_wiki_json_utils.info("get_answer_path()")
    # Loop through the items (key-value pairs) in the dictionary
    if data_dict is None:
        data_dict = get_wiki_json_dict()
    for dict_key, dict_value in data_dict.items():
        items = data_dict.items()
        items_list = list(items)
        location_RU = items_list[1][1]
        # If the current value is the value we're looking for, return the path to the value
        if dict_value == value:
            path = path[6:]
            return "`/wiki` " "_" + path + "\n➡ " + location_RU + "_\n\n"

        # If the current value is a dictionary, call the get_DICT_PATH function recursively to search the nested
        # dictionary
        elif isinstance(dict_value, dict):
            result = get_answer_path(value, dict_value, path + " ➡ " + location_RU)
            if result:
                return result

    # If the value is not found, return None
    return None


def test():
    # Just to be sure
    backup(data)

    # Modify and Write the modified dictionary back to the JSON file
    name_EN = "Security_Password"
    name_RU = "Security_Password"
    text = "Security_Password"
    data["Windows"]["Computer"]["System_Settings"]["Security_Password"] = {
        "0_EN": name_EN,
        "0_RU": name_RU,
        "Text": text
    }
    with open('wiki_data.json', "w") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)

    # Check if it was properly inserted
    with open('wiki_data.json', "r") as json_file:
        # Load the data from the file into a Python dictionary
        data_dict = json.loads(json_file.read())
    # Get the path to the "Windows" value
    print(get_answer_path(name_RU, data_dict))


if __name__ == "__main__":
    # Open the JSON file
    data = get_wiki_json_dict()

    print(get_answer_path(data["Windows"]["Computer"]["Slowing_Bugging"]["Hard_Disk_SSD"]["0_EN"]))


