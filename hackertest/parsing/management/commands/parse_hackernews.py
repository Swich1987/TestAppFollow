# -*- coding: utf-8 -*-
"""Script command to parse hackernews and load them to Postgres."""
import datetime

import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

import hackertest.posts

HACKER_NEWS_URL = "https://news.ycombinator.com/"


class Command(BaseCommand):
    """Django command to parse hackernews."""
    help = "Parse hackernews"

    def handle(self, *args, **options):
        start_parsing()


def start_parsing():
    """Parse hackernews and load extracted data(title, url) to db."""
    print('==Parsing started at %s!==' % datetime.datetime.now())
    _load_data_to_db(_parse_hackernews())
    print('==Parsing finished!==')


def _parse_hackernews():
    """Parse hackernews and return parsed list of [(title, url), ...] tuples."""
    response = requests.get(HACKER_NEWS_URL)
    hacker_news_html = response.text
    news_soup = BeautifulSoup(hacker_news_html, 'html.parser')
    storylink_tags_list = news_soup.find_all('a', attrs={"class": "storylink"})
    title_url_raw_list = []
    for tag in storylink_tags_list:
        title = tag.text
        url = tag.get('href')
        title_url_raw_list.append((title, url))
    print('Hackernews parsed, start loading to db')
    return title_url_raw_list


def _load_data_to_db(title_url_raw_list):
    title_url_list = _remove_existed_data(title_url_raw_list)
    for title, url in title_url_list:
        post = hackertest.posts.models.Post(title=title, url=url)
        post.save()
        print('ADDED to database title="%s" with url="%s"' % (title, url))


def _remove_existed_data(title_url_list):
    print('Clearing data from already saved result...')
    new_title_url_list = []
    titles_list = hackertest.posts.models.Post.objects.values_list('title', flat=True)
    urls_list = hackertest.posts.models.Post.objects.values_list('url', flat=True)
    for title, url in title_url_list:
        if title in titles_list:
            continue
        if url in urls_list:
            continue
        new_title_url_list.append((title, url))
    if new_title_url_list:
        print('Cleared new data:\n', new_title_url_list)
    else:
        print("Nothing new.")
    print('Clearing completed.')
    return new_title_url_list


if __name__ == "__main__":
    start_parsing()
