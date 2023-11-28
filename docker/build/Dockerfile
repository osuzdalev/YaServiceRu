FROM python:3.9-slim

EXPOSE 80

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        postgresql-common \
    && rm -rf /var/lib/apt/lists/*

COPY ./docker/app/image_filers/config/* /var/lib/config/
COPY ./docker/app/image_filters/data/* /var/lib/data/

COPY ./app/dist/telefix-*.tar.gz /tmp/
RUN python3 -m pip install /tmp/telefix-*.tar.gz

COPY ./docker/app/image_files/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
