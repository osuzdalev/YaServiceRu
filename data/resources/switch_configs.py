import argparse


def replace_in_file(file_path: str, search: str, replace: str):
    with open(file_path, "r") as file:
        content = file.read()

    content = content.replace(search, replace)

    with open(file_path, "w") as file:
        file.write(content)


def apply_changes(use_local: bool):
    main_py = "main.py"
    telegram_website_py = "client/wiki_module/telegram_website.py"
    telegram_database_utils_py = "common/telegram_database_utils.py"
    docker_compose_yml = "client/chatgpt_module/Weaviate/docker-compose.yml"

    if use_local:
        replace_in_file(
            main_py,
            'constants.get("FILEPATH", "SERVER_PERSISTENCE")',
            'constants.get("FILEPATH", "LOCAL_PERSISTENCE")',
        )
        replace_in_file(
            main_py,
            'constants.get("FILEPATH", "SERVER_LOGGER")',
            'constants.get("FILEPATH", "LOCAL_LOGGER")',
        )
        replace_in_file(
            main_py,
            'constants.get("TOKEN", "MAIN_BOT")',
            'constants.get("TOKEN", "DEV_BOT")',
        )
        replace_in_file(
            telegram_website_py,
            'constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA")',
            'constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA_TEST")',
        )
        replace_in_file(
            telegram_database_utils_py,
            'constants.get("FILEPATH", "SERVER_DATABASE")',
            'constants.get("FILEPATH", "LOCAL_DATABASE")',
        )
        replace_in_file(
            docker_compose_yml,
            "/Users/osuz/PycharmProjects/YaServiceRu/client/chatgpt_module/Weaviate/data:/data",
            "/home/yaserviceru/Desktop/YaServiceRu/client/chatgpt_module/Weaviate/data:/data",
        )
    else:
        replace_in_file(
            main_py,
            'constants.get("FILEPATH", "LOCAL_PERSISTENCE")',
            'constants.get("FILEPATH", "SERVER_PERSISTENCE")',
        )
        replace_in_file(
            main_py,
            'constants.get("FILEPATH", "LOCAL_LOGGER")',
            'constants.get("FILEPATH", "SERVER_LOGGER")',
        )
        replace_in_file(
            main_py,
            'constants.get("TOKEN", "DEV_BOT")',
            'constants.get("TOKEN", "MAIN_BOT")',
        )
        replace_in_file(
            telegram_website_py,
            'constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA_TEST")',
            'constants.get("TOKEN", "PAYMENT_PROVIDER_YOOKASSA")',
        )
        replace_in_file(
            telegram_database_utils_py,
            'constants.get("FILEPATH", "LOCAL_DATABASE")',
            'constants.get("FILEPATH", "SERVER_DATABASE")',
        )
        replace_in_file(
            docker_compose_yml,
            "/home/yaserviceru/Desktop/YaServiceRu/client/chatgpt_module/Weaviate/data:/data",
            "/Users/osuz/PycharmProjects/YaServiceRu/client/chatgpt_module/Weaviate/data:/data",
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Switch between local and server configurations."
    )
    parser.add_argument(
        "--local", help="Use local configurations.", action="store_true"
    )
    args = parser.parse_args()

    apply_changes(args.local)
