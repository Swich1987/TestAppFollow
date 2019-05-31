"""
Celery settings.
"""
import os
import sys
import configparser

from celery import Celery


current_directory = sys.path[0]
path_to_settings = os.path.join(current_directory, 'hackertest', 'settings.ini')

config = configparser.ConfigParser()
config.read(path_to_settings)

app = Celery(broker=config['CELERY']['BROKER_URL'])
app.conf.timezone = config['CELERY']['TIMEZONE']
UPDATE_PARSING_SEC = float(config['CELERY']['UPDATE_PARSING_SEC'])
