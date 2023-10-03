* add pg_config
* add pg_data
* launch docker-compose

pg_config - file with connection protocols and general config to the db
pg_data is the actual data, spread across several folders. Can be copied/archived and placed in other machine.

init_database.sql is used once before the launch of the docker to create the schema of the database

Reinit empty DB
Pycharm
Database (right panel)
right click -> New -> Query console -> copy paste init -> run

One file data to export
Pycharm
Database (right panel)
right click -> import/export -> 'pg_dump'