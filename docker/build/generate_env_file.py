#!/usr/bin/env python3

import configparser
import argparse
from dotenv import load_dotenv
import os


def generate_env_file(config_file, output_file, dotenv_file):
    load_dotenv(dotenv_file)

    config = configparser.ConfigParser()
    config.read(config_file)

    params = {}
    for section in config.sections():
        section_formatted = section.replace(".", "_").upper()
        for key, value in config[section].items():
            env_name = f"{section_formatted}_{key.upper()}"
            params[env_name] = value

    # FIXME how to avoid leaking the secrets?
    params["DATABASE_POSTGRES_PASSWORD"] = os.getenv("DATABASE_POSTGRES_PASSWORD")
    params["API_OPENAI"] = os.getenv("API_OPENAI")
    params["TOKEN_TG_DEV_BOT"] = os.getenv("TOKEN_TG_DEV_BOT")
    params["TOKEN_PAYMENT_PROVIDER_YOOKASSA"] = os.getenv(
        "TOKEN_PAYMENT_PROVIDER_YOOKASSA"
    )
    params["PASSWORD_YANDEX_YASERVICERU_APP"] = os.getenv(
        "PASSWORD_YANDEX_YASERVICERU_APP"
    )

    env_content = f"""
    export API_OPENAI={params['API_OPENAI']}
    export TOKEN_TG_DEV_BOT={params['TOKEN_TG_DEV_BOT']}
    export TOKEN_PAYMENT_PROVIDER_YOOKASSA={params['TOKEN_PAYMENT_PROVIDER_YOOKASSA']}
    export PASSWORD_YANDEX_YASERVICERU_APP={params['PASSWORD_YANDEX_YASERVICERU_APP']}
    export TELEFIX_LOCAL_PERSISTENCE={params['TELEFIX_LOCAL_PERSISTENCE']}
    export TELEFIX_IMAGE_PERSISTENCE={params['TELEFIX_IMAGE_PERSISTENCE']}
    export TELEFIX_LOCAL_LOGS={params['TELEFIX_LOCAL_LOGS']}
    export TELEFIX_IMAGE_LOGS={params['TELEFIX_IMAGE_LOGS']}
    export TELEFIX_LOCAL_DOCKERFILE={params['TELEFIX_LOCAL_DOCKERFILE']}
    export TELEFIX_IMAGE_PORT={params['TELEFIX_IMAGE_PORT']}
    export TELEFIX_IMAGE_COMMAND={params['TELEFIX_IMAGE_COMMAND']}
    export DATABASE_LOCAL_DATA={params['DATABASE_LOCAL_DATA']}
    export DATABASE_IMAGE_DATA={params['DATABASE_IMAGE_DATA']}
    export DATABASE_LOCAL_CONFIG={params['DATABASE_LOCAL_CONFIG']}
    export DATABASE_IMAGE_CONFIG={params['DATABASE_IMAGE_CONFIG']}
    export DATABASE_IMAGE_PORT={params['DATABASE_IMAGE_PORT']}
    export DATABASE_POSTGRES_PASSWORD={params['DATABASE_POSTGRES_PASSWORD']}
    export VECTOR_DATABASE_LOCAL_PERSISTENCE={params['VECTOR_DATABASE_LOCAL_PERSISTENCE']}
    export VECTOR_DATABASE_IMAGE_PERSISTENCE={params['VECTOR_DATABASE_IMAGE_PERSISTENCE']}
    export VECTOR_DATABASE_LOCAL_BACKUPS={params['VECTOR_DATABASE_LOCAL_BACKUPS']}
    export VECTOR_DATABASE_IMAGE_BACKUPS={params['VECTOR_DATABASE_IMAGE_BACKUPS']}
    export VECTOR_DATABASE_IMAGE_PORT={params['VECTOR_DATABASE_IMAGE_PORT']}
    export PROMETHEUS_LOCAL_CONFIGS={params['PROMETHEUS_LOCAL_CONFIGS']}
    export PROMETHEUS_IMAGE_CONFIGS={params['PROMETHEUS_IMAGE_CONFIGS']}
    export PROMETHEUS_LOCAL_DATA={params['PROMETHEUS_LOCAL_DATA']}
    export PROMETHEUS_IMAGE_DATA={params['PROMETHEUS_IMAGE_DATA']}
    export PROMETHEUS_IMAGE_PORT={params['PROMETHEUS_IMAGE_PORT']}
    export GRAFANA_LOCAL_CONFIGS={params['GRAFANA_LOCAL_CONFIGS']}
    export GRAFANA_IMAGE_CONFIGS={params['GRAFANA_IMAGE_CONFIGS']}
    export GRAFANA_LOCAL_DATASOURCE={params['GRAFANA_LOCAL_DATASOURCE']}
    export GRAFANA_IMAGE_DATASOURCE={params['GRAFANA_IMAGE_DATASOURCE']}
    export GRAFANA_LOCAL_DASHBOARD_PROVIDER={params['GRAFANA_LOCAL_DASHBOARD_PROVIDER']}
    export GRAFANA_IMAGE_DASHBOARD_PROVIDER={params['GRAFANA_IMAGE_DASHBOARD_PROVIDER']}
    export GRAFANA_LOCAL_DASHBOARDS={params['GRAFANA_LOCAL_DASHBOARDS']}
    export GRAFANA_IMAGE_DASHBOARDS={params['GRAFANA_IMAGE_DASHBOARDS']}
    export GRAFANA_IMAGE_PORT={params['GRAFANA_IMAGE_PORT']}
    """.strip()

    with open(output_file, "w") as env_file:
        env_file.write(env_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate environment variables from an INI configuration file."
    )
    parser.add_argument(
        "--config", required=True, help="Path to the INI configuration file."
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the output file to write environment variables.",
    )
    parser.add_argument("--dotenv", required=True, help="Path to the .env file.")
    args = parser.parse_args()

    generate_env_file(args.config, args.output, args.dotenv)
