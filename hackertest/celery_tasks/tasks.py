"""Just describe her celery's task.

here is two self-described modules:
setup_periodic_tasks and parse_hackenews_task.
"""
import logging

from hackertest.parsing.management.commands.parse_hackernews import start_parsing
from .settings import app, UPDATE_PARSING_SEC, SOFT_TIME_LIMIT

logger = logging.getLogger(__name__)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Used to setup launching of any periodic tasks."""
    logger.info('Setup periodic task.')
    sender.add_periodic_task(UPDATE_PARSING_SEC, parse_hackernews_task.s(),
                             name='Celery parse hackernews task')


@app.task(soft_time_limit=SOFT_TIME_LIMIT)
def parse_hackernews_task():
    """"Load and launch parsing task from Django's script."""
    logger.debug("Launch start_parsing.")
    start_parsing()
