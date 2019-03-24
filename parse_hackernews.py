"""
Just parse hacker news and load them to Postgres
"""

from time import sleep

import requests

import psycopg2

from bs4 import BeautifulSoup

HACKER_NEWS_URL = "https://news.ycombinator.com/"
TABLE_NAME = "posts_post"

INSERT_STR = ("INSERT INTO " + TABLE_NAME + "(created, title, url) " +
              "VALUES (current_timestamp, %(title)s, %(url)s) " +
              "ON CONFLICT DO NOTHING")

TITLE_POSITION = 2
URL_POSITION = 3

UPDATE_SEC = 60


def load_data_to_db(title_url_list):
    conn = psycopg2.connect(dbname="postgres", user="postgres",
                            host='db', port=5432)
    insert_dict = {}
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM " + TABLE_NAME)
        db_posts = cur.fetchall()
    db_titles_list = [db_post[TITLE_POSITION] for db_post in db_posts]
    db_urls_list = [db_post[URL_POSITION] for db_post in db_posts]
    for title, url in title_url_list:
        if title not in db_titles_list and url not in db_urls_list:
            insert_dict["title"] = title
            insert_dict["url"] = url
            with conn.cursor() as cur:
                cur.execute(INSERT_STR, insert_dict)
                conn.commit()
                print('Added to database title="%s" with url="%s"' % (title, url))
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM " + TABLE_NAME)
            db_posts = cur.fetchall()
        db_titles_list = [db_post[TITLE_POSITION] for db_post in db_posts]
        db_urls_list = [db_post[URL_POSITION] for db_post in db_posts]
    conn.close()

def parse_and_load():
    """Parse Hacker news and load them to Postgres"""
    response = requests.get(HACKER_NEWS_URL)
    hacker_news_html = response.text
    news_soup = BeautifulSoup(hacker_news_html, 'html.parser')
    storylink_tags_list = news_soup.find_all('a', attrs={"class": "storylink"})
    title_url_list = []
    for tag in storylink_tags_list:
        title = tag.text
        url = tag.get('href')
        title_url_list.append((title, url))
    load_data_to_db(title_url_list)


if __name__ == "__main__":
    while True:
        parse_and_load()
        sleep(UPDATE_SEC)
