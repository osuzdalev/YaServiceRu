#!/bin/bash

# Source the .env file to set environment variables
source .env

CONFIG_FILE=${1:-config.yaml}

# Read values from $CONFIG_FILE using Python and set them as environment variables
DATABASE_PORT=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['port'])")
DATABASE_DATA=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['data'])")
DATABASE_CONFIG=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['database']['config'])")

WEAVIATE_PORT=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['port'])")
WEAVIATE_DATA=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['data'])")
WEAVIATE_PERSISTENCE=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['weaviate']['persistence'])")

APP_PORT=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['port'])")
APP_LOGS=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['logs'])")
APP_PERSISTENCE=$(python -c "import yaml; print(yaml.safe_load(open('$CONFIG_FILE'))['yaserviceru']['network']['persistence'])")

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
