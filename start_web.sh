#!/usr/bin/env sh

echo "WAITING 5 SEC FOR DB TO RUN..."
sleep 5
python3 manage.py makemigrations posts
echo "MIGRATION CREATED"
python3 manage.py migrate
echo "MIGRATION COMPLETED"
python3 manage.py parse_hackernews
echo "HACKERNEWS PARSED"
echo "LAUNCHING SERVER FOR TESTS"
screen -dmS django python3 manage.py runserver 0:8000
sleep 1
echo "SERVER FOR TESTS LAUNCHED"
echo "START INNER TESTS"
python3 manage.py test --noinput
echo "INNER TESTS COMPLETED"
pkill screen
echo "LAUNCHING SERVER"
python3 manage.py runserver 0:8000
