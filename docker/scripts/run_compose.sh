#!/usr/bin/env bash

# Use the script like this:
# ./run_compose.sh ../telefix/config/core/dev.yaml

set -e

CONFIG_FILE=${1:-config.yaml}

# Autogenerate the environment variables and write them to a file
ENV_FILE=$(mktemp)
python3 generate_env_file.py --config $CONFIG_FILE --output $ENV_FILE
cat $ENV_FILE
source $ENV_FILE

docker-compose up -d

echo "Docker containers started successfully!"