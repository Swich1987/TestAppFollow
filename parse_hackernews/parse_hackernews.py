# -*- coding: utf-8 -*-
"""
Just parse hacker news and load them to Postgres
"""
import psycopg2
import requests
from bs4 import BeautifulSoup

DB_SETTINGS = {
    "dbname": "postgres",
    "user": "postgres",
    "host": "db",
    "port": 5432
}

HACKER_NEWS_URL = "https://news.ycombinator.com/"

TABLE_NAME = "posts_post"

INSERT_STR = ("INSERT INTO " + TABLE_NAME + "(created, title," +
              "url) " + "VALUES (current_timestamp, %(title)s," +
              "%(url)s) ON CONFLICT DO NOTHING")


def start_parsing():
    """Parse hackernews and load extracted data to db"""
    load_data_to_db(parse_hackernews())


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
    connection = psycopg2.connect(**DB_SETTINGS)
    title_url_list = remove_existed_data(title_url_raw_list, connection)
    for title, url in title_url_list:
        with connection.cursor() as cur:
            cur.execute(INSERT_STR, {'title': title, 'url': url})
            connection.commit()
            print('ADDED to database title="%s" with url="%s"' % (title, url))
    connection.close()


def remove_existed_data(title_url_list, connection):
    print('Start clearing data from already saved result.')
    new_title_url_list = []
    titles_list, urls_list = get_data_from_db(connection)
    for title, url in title_url_list:
        if title in titles_list:
            continue
        if url in urls_list:
            continue
        new_title_url_list.append((title, url))
    if new_title_url_list:
        print('Parsed raw data =', title_url_list)
        print('Cleared data from already saved result =', new_title_url_list)
    else:
        print("Nothing new.")
    return new_title_url_list


def get_data_from_db(connection):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM " + TABLE_NAME)
        db_posts = cur.fetchall()
        title_index, url_index = get_title_url_column_number(cur)
    if not db_posts:
        init_database(connection)
    titles_list = [db_post[title_index] for db_post in db_posts]
    urls_list = [db_post[url_index] for db_post in db_posts]
    return titles_list, urls_list


def get_title_url_column_number(cur):
    columns = cur.description
    i = 0
    title_index = 1
    url_index = 2
    for column in columns:
        if column.name == 'title':
            title_index = i
        if column.name == 'url':
            url_index = i
        i += 1
    return title_index, url_index


def init_database(connection):
    """Alter table to make correct ordering in PostgreSQL."""
    with connection.cursor() as cur:
        cur.execute('alter table %s alter url type text COLLATE ucs_basic;' % TABLE_NAME)
        cur.execute('alter table %s alter title type text COLLATE ucs_basic;' % TABLE_NAME)


if __name__ == "__main__":
    print('Start parsing...')
    start_parsing()
    print('Parsing completed.')
