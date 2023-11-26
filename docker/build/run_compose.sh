#!/usr/bin/env bash

# ./docker/build/run_compose.sh ./docker/build/admin_config.ini

set -e

# Check if config file argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <path_to_config_file>"
    exit 1
fi

CONFIG_FILE=$1

# Autogenerate the environment variables and write them to a file
ENV_FILE=$(mktemp)
python3 docker/build/generate_env_file.py --config $CONFIG_FILE --output $ENV_FILE --dotenv .env
cat $ENV_FILE
source $ENV_FILE
echo "$ENV_FILE sourced"

docker-compose -f docker/build/docker-compose.yml up -d

echo "Docker containers started successfully!"

