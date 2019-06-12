""" Celery settings module.

Most of settings are extracted from settings.ini

app - celery app, which can me imported to create celery's task

UPDATE_PARSING_SEC - extracted from file. Time between parsing site.
SOFT_TIME_LIMIT - celery setting for max limit per task.
"""
import configparser
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from celery import Celery
from celery.signals import after_setup_logger

logger = logging.getLogger(__name__)

_path_to_settings = os.path.join(sys.path[0], 'hackertest', 'settings.ini')

_config = configparser.ConfigParser()
_config.read(_path_to_settings)

app = Celery(broker=_config['CELERY']['BROKER_URL'])
app.conf.timezone = _config['CELERY']['TIMEZONE']

UPDATE_PARSING_SEC = _config.getfloat('CELERY', 'UPDATE_PARSING_SEC')
SOFT_TIME_LIMIT = _config.getint('CELERY', 'SOFT_TIME_LIMIT')


@after_setup_logger.connect
def _setup_loggers(logger, *args, **kwargs):
    """Setup logger for celery tasks."""
    max_bytes = 1024 * _config.getint('CELERY', 'LOG_FILE_SIZE_KBYTES')
    backup_count = _config.getint('CELERY', 'LOG_FILE_BACKUP_COUNT')

    fh = RotatingFileHandler(filename=_config['CELERY']['LOG_FILE_NAME'],
                             maxBytes=max_bytes, backupCount=backup_count)

    format_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(format_str)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
