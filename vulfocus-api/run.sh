#!/bin/bash

service nginx start
wait
service redis-server restart
wait
nohup python3 manage.py runserver 0.0.0.0:8000 &
curl -X GET https://iast.huoxian.cn/api/v1/agent/download?url=https://iast.huoxian.cn -H 'Authorization: Token 9b2fc54785c5d8f53fc01ffb4c90b576b8a0e160' -o /tmp/agent.jar -k
nohup java -Dsqlite.path="/vulfocus-api/db.sqlite3" -Ddockerfile.path="/tmp/Dockerfile" -Drepository.name="webhubforiast/" -Dhost.ip="tcp://192.168.0.137:2375" -jar /vulfocus-api/app.jar &
celery -A vulfocus worker -l info -E --logfile=celery.log
