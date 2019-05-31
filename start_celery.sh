#!/usr/bin/env sh

echo "Clear celery files."
rm -f ./celerybeat.pid
rm -f ./celerybeat-schedule
rm -f ./celeryd.pid
echo "Start periodic parsing..."
screen -dmS worker celery -A hackertest.celery_tasks.tasks worker --loglevel INFO
celery -A hackertest.celery_tasks.tasks beat --loglevel INFO