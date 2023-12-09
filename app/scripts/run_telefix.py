"""
Runs the library locally
Usage: python -m app.scripts.run_telefix
"""

import sys
from ..telefix import telefix


def run_telefix():
    telefix.main(
        [
            "--app_config_path",
            "/Users/osuz/PycharmProjects/YaServiceRu/app/config/local",
            "--log_level",
            "INFO",
        ]
    )


if __name__ == "__main__":
    run_telefix()
