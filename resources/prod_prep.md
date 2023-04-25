# 1) Merge from Dev
```bash
git merge dev
```

# 2) Change the constants in files
* main.py -> line 38 **(Persistence)**
* main.py -> line 25 **(LOGS)**
* main.py -> line 40 **(TOKEN)**
* background/telegram_database_utils.py -> line 10 **(Database)**
* clientcommands/request.py -> line 32 - 33 **(Phone)**
* clientcommands/chatgpt_module/Weaviate/data -> line 17 **(Volumes)**

# 3) Hide the constant.ini file
```bash
git secret hide
```

# 3) Delete unnecessary folders
```bash
git add .
git reset folder-to-exclude/
```

# 4) Push to git

# 5) Pull from server
```bash
ssh yaserviceru@77.239.235.39
pass: ********

ps aux | grep main.py
kill PID

cd Desktop/YaServiceRu/
git pull
```

# 6) Reveal Secret files
```bash
git secret reveal
```

# Reset persistence if needed
```bash
cd resources
python3 reset_persistence.py
```

# 7) Move files from repo to other folder for safety
```bash
mv /home/yaserviceru/Desktop/YaServiceRu/resources/yaserviceru_persistence \
/home/yaserviceru/Desktop/YaServiceRu/resources/yaserviceru_db.sqlite \
/home/yaserviceru/Desktop/
```

# 8) restart bot on server
```bash
cd Desktop/YaServiceRu/
nohup python3 main.py &
```
