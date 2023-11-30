#!/usr/bin/env bash

# ./docker/build/run_compose.sh ./docker/build/admin_config.ini

set -e

# Check if file exists
CONFIG_FILE=${1:-"$(dirname $0)/admin_config.ini"}
if ! test -f "$CONFIG_FILE"; then
    echo "$CONFIG_FILE does not exist"
    exit 1
fi

# Autogenerate the environment variables and write them to a file
ENV_FILE=$(mktemp)
python3 docker/build/generate_env_file.py --config $CONFIG_FILE --output $ENV_FILE --dotenv .env
cat $ENV_FILE
source $ENV_FILE

docker-compose -f ./docker/build/docker-compose.yml up -d

echo "Docker containers started successfully!"