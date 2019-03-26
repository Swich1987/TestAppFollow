#!/usr/bin/env bash

sleep 5
python3 manage.py makemigrations posts
echo "MIGRATION CREATED"
python3 manage.py migrate
echo "MIGRATION COMPLETED"
screen -dmS parsing  python3 loop_parsing.py
echo "HACKERNEWS PARSED"
echo "LAUNCHING SERVER FOR TESTS"
screen -dmS django python3 manage.py runserver 0:8000
sleep 1
echo "SERVER FOR TESTS LAUNCHED"
echo "START INNER TESTS"
python3 manage.py test
echo "INNER TESTS COMPLETED"
pkill screen
screen -dmS parsing  python3 loop_parsing.py
echo "LAUNCHING SERVER"
python3 manage.py runserver 0:8000
