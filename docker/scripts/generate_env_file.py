#!/usr/bin/env python3

import yaml
import argparse
import os
from dotenv import load_dotenv

load_dotenv()


def generate_env_file(config_file, output_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    with open(output_file, "w") as env_file:
        database = config["database"]
        weaviate = config["weaviate"]
        params = dict(
            database_postgres_password=os.getenv("DATABASE_POSTGRES_PASSWORD"),
            database_port=database["port"],
            database_data=database["data"],
            database_config=database["config"],
            weaviate_port=weaviate["port"],
            weaviate_data=weaviate["data"],
            weaviate_persistence=weaviate["persistence"],
            app_logs=config["telefix"]["docker"]["logs"],
            app_port=config["telefix"]["docker"]["port"]
        )

        FILE = """
        export DATABASE_POSTGRES_PASSWORD={database_postgres_password}
        export DATABASE_PORT={database_port}
        export DATABASE_DATA={database_data}
        export DATABASE_CONFIG={database_config}
        export WEAVIATE_PORT={weaviate_port}
        export WEAVIATE_DATA_VOLUME_PATH={weaviate_data}
        export WEAVIATE_PERSISTENCE_PATH={weaviate_persistence}
        export APP_LOGS={app_logs}
        export APP_PORT={app_port}
        """

        env_file.write(FILE.format(**params))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate environment variables from a YAML configuration file."
    )
    parser.add_argument(
        "--config", required=True, help="Path to the configuration YAML file."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output file to write environment variables.",
    )
    args = parser.parse_args()

    generate_env_file(args.config, args.output)
