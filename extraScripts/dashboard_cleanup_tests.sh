#!/bin/sh

docker container exec -it docker_dashboard-persistence-qa_1 bash -c "/usr/share/dev/dashboard/docker/setup-datastore.sh --environment .env.qa --reset"
docker container exec -it docker_mysql_db_1 bash -c "mysql -u root -proot < /usr/share/dev/dashboard/docker/keystone_clean.sql"
