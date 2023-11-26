image_files directory contains files that are copied to the image either directly or by using volumes.
This also includes the database files and the actual data.

TODO
Where in the image those files should be placed to be accessible from the package?

# Deployment:
```bash
./docker/build/run_compose.sh ./docker/build/admin_config.ini
```
can be dev, main, local