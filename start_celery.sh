#!/usr/bin/env sh

echo "Clear celery files."
rm -f ./celerybeat.pid
rm -f ./celerybeat-schedule
rm -f ./celeryd.pid
echo "Start periodic parsing..."
cat ./hackertest/settings.ini | grep "UPDATE_PARSING_SEC"
screen -dmS worker celery -A hackertest.celery_tasks.tasks worker --loglevel INFO
celery -A hackertest.celery_tasks.tasks beat --loglevel INFO