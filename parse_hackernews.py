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


def load_data_to_db(title_url_list):
    conn = psycopg2.connect(dbname="postgres", user="postgres",
                            host='db', port=5432)
    insert_dict = {}
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM " + TABLE_NAME)
        db_posts = cur.fetchall()
    db_title = [db_post[2] for db_post in db_posts]
    db_url = [db_post[3] for db_post in db_posts]
    for title, url in title_url_list:
        if title not in db_title and url not in db_url:
            insert_dict["title"] = title
            insert_dict["url"] = url
            with conn.cursor() as cur:
                cur.execute(INSERT_STR, insert_dict)
                conn.commit()
                print('Added to database title="%s" with url="%s"' % (title, url))
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
        # print(title, url)
    load_data_to_db(title_url_list)


if __name__ == "__main__":
    while True:
        parse_and_load()
        sleep(60)
