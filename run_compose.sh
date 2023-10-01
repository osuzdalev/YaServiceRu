#!/bin/bash

# Use the script like this:
# ./run_compose.sh ./config/app/dev.yaml

set -e

source .env

CONFIG_FILE=${1:-config.yaml}

# TODO Write a python script to autogenerate the environment variables
# and write them to a file, which you will then source to export them.
# This script should then look like this:
#
# ENV_FILE=$(mktemp)
# generate_env_file.py --config $CONFIG_FILE --output $ENV_FILE
# source $ENV_FILE
# docker-compose up -d
# echo "Docker containers started successfully!"

# Read values from $CONFIG_FILE using Python and set them as environment variables
DATABASE_PORT=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['port'])")
DATABASE_DATA=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['data'])")
DATABASE_CONFIG=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['config'])")

WEAVIATE_PORT=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['port'])")
WEAVIATE_DATA=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['data'])")
WEAVIATE_PERSISTENCE=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['persistence'])")

APP_PORT=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['port'])")
APP_LOGS=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['logs'])")
APP_PERSISTENCE=$(python3 -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['persistence'])")

export DATABASE_POSTGRES_PASSWORD
export DATABASE_PORT
export DATABASE_DATA
export DATABASE_CONFIG
export WEAVIATE_PORT
export WEAVIATE_DATA
export WEAVIATE_PERSISTENCE
export APP_PORT
export APP_LOGS
export APP_PERSISTENCE

# Launch docker-compose
docker-compose up -d

echo "Docker containers started successfully!"