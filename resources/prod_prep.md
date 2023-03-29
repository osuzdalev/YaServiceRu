# 1) Delete unnecessary folders


# 2) Hide the constant.ini file
```bash
git secret hide
```

# 3) Change the constants in files
main.py -> line 36

background/
* telegram_database_utils.py -> line 10
* error_logging.py -> line 72
* helpers.py -> line 62

clientcommands/request.py -> line 32 - 33

# 4) Push to git

# 5) Pull from server

# 6) Reveal Secret files

```bash
git secret reveal
```

# 7) Move files from repo to other folder for safety

```bash
mv /home/yaserviceru/Desktop/YaServiceRu/yaserviceru_persistence \
/home/yaserviceru/Desktop/YaServiceRu/yaserviceru_db.sqlite \
/home/yaserviceru/Desktop/
```