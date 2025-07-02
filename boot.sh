#!/bin/bash

while true;do 
    flask db upgrade 
    if [[ "$?" == "0" ]]; then 
        break 
    fi 
    echo Upgrade command failed, retrying in 5 secs... 
    sleep 5 
done 
exec gunicorn -b :5000 --access-logfile - --error-logfile - microblog:app

# 1. 数据库迁移
while ! flask db upgrade; do
  echo "DB upgrade failed, retry in 5s..."
  sleep 5
done

# 2. 等待 ES 健康
until curl -s http://elasticsearch:9200 >/dev/null; do
  echo "Waiting for Elasticsearch..."
  sleep 5
done

# 3. 启动应用
exec gunicorn -b :5000 --access-logfile - \
     --error-logfile - microblog:app
