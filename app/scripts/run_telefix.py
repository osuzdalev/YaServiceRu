"""
Runs the library locally
Usage: python -m app.scripts.run_telefix
"""

import sys
from ..telefix import telefix


def run_telefix():
    predefined_args = [
        "--app_config_path",
        "/Users/osuz/PycharmProjects/YaServiceRu/app/config/local",
        "--log_level",
        "INFO",
    ]
    sys.argv.extend(predefined_args)
    telefix.main()


if __name__ == "__main__":
    run_telefix()
