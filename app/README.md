# YaServiceRu

Handling of repair service orders on the Telegram platform.

The idea is to dispatch orders of electronic goods reparations to the
appropriate and available contractor within a large group/community.

# Run on local machine
First launch the other docker services, then run

```bash
python -m app.scripts.local
```

## System Dependencies

```bash
sudo apt install postgresql-common
```

---

You may use sphinx to create documentation
https://towardsdatascience.com/documenting-python-code-with-sphinx-554e1d6c4f6d

It will create an html website which you can optionally host with a web server
https://tecadmin.net/tutorial/docker-run-static-website

---

# Install package locally

```bash
python -m build
python -m pip install ./dist/telefix-0.{x}.{x}.tar.gz
```
