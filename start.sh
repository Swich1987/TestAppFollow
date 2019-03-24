#!/bin/bash
sleep 5
python3 manage.py makemigrations posts
echo "MIGRATION CREATED"
sleep 2
python3 manage.py migrate
echo "MIGRATION COMPLETED"
sleep 2
screen -d -m python3 parse_hackernews.py
echo "HACKERNEWS PARSED"
sleep 2
echo "START SERVER"
python3 manage.py runserver 0:8000
