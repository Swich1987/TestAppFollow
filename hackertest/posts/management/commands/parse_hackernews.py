# -*- coding: utf-8 -*-
"""
Command to parse hacker news and load them to Postgres.
"""
from django.core.management.base import BaseCommand

from hackertest.celery_tasks.parse_hackernews import start_parsing


class Command(BaseCommand):
    """
    Django command to parse hackernews.
    """
    help = "Parse hackernews"

    def handle(self, *args, **options):
        start_parsing()
