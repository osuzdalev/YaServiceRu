FROM python:3.9-slim

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        postgresql-common python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY ../app/dist/telefix-*.tar.gz /tmp/
RUN python3 -m pip install /tmp/telefix-*.tar.gz

COPY ./docker/entrypoint.sh /usr/src/yaserviceru/docker/entrypoint.sh
RUN chmod +x /usr/src/telefix/docker/core.sh

EXPOSE 80
ENTRYPOINT ["/usr/src/telefix/docker/entrypoint.sh"]
