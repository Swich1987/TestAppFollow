from .settings import app, UPDATE_PARSING_SEC
from .parse_hackernews import start_parsing


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(UPDATE_PARSING_SEC, parse_hackernews_task.s(),
                             name='Celery parse hackernews task')


@app.task
def parse_hackernews_task():
    start_parsing()
