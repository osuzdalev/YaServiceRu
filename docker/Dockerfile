# Use the specified image as the base
FROM python:3.9

# Set a non-interactive frontend
RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        postgresql-common python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /yaserviceru_venv \
    && . /yaserviceru_venv/bin/activate \
    # Install the project package from TestPyPI and the dependencies from PyPI
    && pip3 install --upgrade --no-cache-dir \
        -i https://test.pypi.org/simple/ \
        --extra-index-url https://pypi.org/simple \
        yaserviceru==0.2.18

EXPOSE 80

COPY ./docker/entrypoint.sh /usr/src/yaserviceru/docker/entrypoint.sh
RUN chmod +x /usr/src/yaserviceru/docker/entrypoint.sh
ENTRYPOINT ["/usr/src/yaserviceru/docker/entrypoint.sh"]
