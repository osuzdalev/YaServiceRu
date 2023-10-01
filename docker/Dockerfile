FROM python:3.9

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt update && apt upgrade -y \
    && apt install -q -y --no-install-recommends \
        postgresql-common python3-venv \
    && rm -rf /var/lib/apt/lists/*

COPY .. /usr/src/yaserviceru

RUN python3 -m venv /yaserviceru_venv \
    && . /yaserviceru_venv/bin/activate \
    && pip3 install --upgrade --no-cache-dir -r /usr/yaserviceru/yaserviceru/requirements.txt

# NOTE Workaround until the package is properly installed
# TODO Configure a setup.py and update the dockerfile to install the package
# See https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/
ENV PYTHONPATH="/usr/src/yaserviceru:$PYTHONPATH"
RUN ln -s /usr/yaserviceru/yaserviceru/scripts/main.py /usr/bin/yaserviceru

EXPOSE 80

ENTRYPOINT ["/usr/src/yaserviceru/docker/entrypoint.sh"]
CMD ["yaserviceru"]