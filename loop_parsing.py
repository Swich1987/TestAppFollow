# -*- coding: utf-8 -*-
"""
Just parse hacker news and load them to Postgres
"""

from time import sleep

from parse_hackernews.parse_hackernews import start_parsing

UPDATE_SEC = 60

if __name__ == "__main__":
    print('Start parsing')
    while True:
        start_parsing()
        print('Wait %s seconds and repeat parsing' % UPDATE_SEC)
        sleep(UPDATE_SEC)
