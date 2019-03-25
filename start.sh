#!/usr/bin/env bash

sleep 5
python3 manage.py makemigrations posts
echo "MIGRATION CREATED"
python3 manage.py migrate
echo "MIGRATION COMPLETED"
screen -dmS parsing  python3 loop_parsing.py
echo "HACKERNEWS PARSED"
sleep 4
echo "START INNER TESTS"
screen -dmS testing bash -c " sleep 10 && python3 manage.py test ; exec sh"
echo "INNER TESTS COMPLETED"
echo "LAUNCHING SERVER"
python3 manage.py runserver 0:8000
