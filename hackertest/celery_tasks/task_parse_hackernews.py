# -*- coding: utf-8 -*-
"""
Just parse hacker news and load them to Postgres
"""
import datetime
import requests
from bs4 import BeautifulSoup

import hackertest.posts

HACKER_NEWS_URL = "https://news.ycombinator.com/"

def start_parsing():
    """Parse hackernews and load extracted data to db"""
    print('==Parsing started at %s!==' % datetime.datetime.now())
    load_data_to_db(parse_hackernews())
    print('==Parsing finished!==')


def parse_hackernews():
    """Parse Hacker news and return parsed list of [(title, url), ...] tuples."""
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


def load_data_to_db(title_url_raw_list):
     title_url_list = remove_existed_data(title_url_raw_list)
     for title, url in title_url_list:
         post = hackertest.posts.models.Post(title=title, url=url)
         post.save()
         print('ADDED to database title="%s" with url="%s"' % (title, url))


def remove_existed_data(title_url_list):
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
