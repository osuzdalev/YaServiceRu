In order to view metrics on the dashboards, you need to create some usage. Ideally you will use Weaviate as you would normally use it in this step.

# Bash commands

```bash
curl http://localhost:8080/v1/schema
curl http://localhost:8080/v1/objects
```

```bash
curl -X DELETE http://localhost:8080/v1/schema/Name_of_class
```

```bash
curl \
-X POST \
-H "Content-Type: application/json" \
-d '{
     "id": "test_1"
    }' \
http://localhost:8080/v1/backups/filesystem
```

```bash
# Syntax: /v1/backups/{backend}/{backup_id}
curl http://localhost:8080/v1/backups/filesystem/my-very-first-backup
```

```bash
curl \
-X POST \
-H "Content-Type: application/json" \
-d '{
     "id": "my-very-first-backup"
    }' \
http://localhost:8090/v1/backups/filesystem/my-very-first-backup/restore
```

```bash
# Syntax: /v1/backups/{backend}/{backup_id}/restore
curl http://localhost:8090/v1/backups/filesystem/my-very-first-backup/restore
```

# Sentence Transformer MPS usage

If running on Macs M# chips, edit the following code in the "SentenceTransformers" class
```python
if device is None:
    if torch.cuda.is_available():
        device = "cuda"
    elif torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"
    logger.info("Use pytorch device: {}".format(device))
```

### Open Grafana in the browser

* Open your Browser at `localhost:3000`
* Log into the Grafana instance using weaviate/weaviate. 
* Select one of the sample dashboards, such as "Importing Data Into Weaviate".
