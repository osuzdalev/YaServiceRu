FROM python:3.9 as builder

# Set a non-interactive frontend
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        postgresql-common python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment, activate it and install package
COPY ../app/dist/yaserviceru-*.tar.gz /tmp/
RUN python3 -m venv /yaserviceru_venv \
    && . /yaserviceru_venv/bin/activate \
    && python3 -m pip install /tmp/telefix-*.tar.gz

FROM python:3.9-slim
COPY --from=builder /yaserviceru_venv /yaserviceru_venv
ENV PATH="/yaserviceru_venv/bin:$PATH"

COPY ./docker/entrypoint.sh /usr/src/yaserviceru/docker/entrypoint.sh
RUN chmod +x /usr/src/telefix/docker/core.sh

EXPOSE 80
ENTRYPOINT ["/usr/src/yaserviceru/docker/entrypoint.sh"]
