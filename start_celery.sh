#!/usr/bin/env sh

echo "Clear celery files."
rm -f ./celerybeat.pid
rm -f ./celerybeat-schedule
rm -f ./celeryd.pid

CELERY_LOG_LEVEL=`cat ./hackertest/settings.ini | grep "LOG_LEVEL = " |
                 cut -d ' ' -f 3 | sed "s/\\r//g"`
echo "CELERY LOG LEVEL = $CELERY_LOG_LEVEL"
cat ./hackertest/settings.ini | grep "UPDATE_PARSING_SEC"
echo "You can change settings in hackertest/settings.ini"

echo "Start periodic parsing..."
screen -dmS worker celery -A hackertest.celery_tasks.tasks worker \
       --loglevel $CELERY_LOG_LEVEL
celery -A hackertest.celery_tasks.tasks beat --loglevel $CELERY_LOG_LEVEL