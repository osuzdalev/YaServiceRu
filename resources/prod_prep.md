# 1) Delete unnecessary folders
```bash
git add .
git reset folder-to-exclude/
```


# 2) Hide the constant.ini file
```bash
git secret hide
```

# 3) Change the constants in files
* main.py -> line 36 
* background/telegram_database_utils.py -> line 10 
* clientcommands/request.py -> line 32 - 33

# 4) Push to git

# 5) Pull from server

# 6) Reveal Secret files
```bash
git secret reveal
```

# 7) Move files from repo to other folder for safety
```bash
mv /home/yaserviceru/Desktop/YaServiceRu/resources/yaserviceru_persistence \
/home/yaserviceru/Desktop/YaServiceRu/resources/yaserviceru_db.sqlite \
/home/yaserviceru/Desktop/
```

# 8) restart bot on server
```bash
ps aux | grep main.py
kill PID

ssh yaserviceru@77.239.235.39
pass: 1313
cd Desktop/YaServiceRu/
nohup python3 main.py &
```
