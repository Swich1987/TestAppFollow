"""
Just parse hacker news and load them to Postgres
"""
import requests
import psycopg2
from bs4 import BeautifulSoup

DB_SETTINGS = {
    "dbname": "postgres",
    "user": "postgres",
    "host": "db",
    "port": 5432
}

HACKER_NEWS_URL = "https://news.ycombinator.com/"
TABLE_NAME = "posts_post"

INSERT_STR = ("INSERT INTO " + TABLE_NAME + "(created, title, url) " +
              "VALUES (current_timestamp, %(title)s, %(url)s) " +
              "ON CONFLICT DO NOTHING")


def get_title_url_column_number(cur):
    columns = cur.description
    i = 0
    for column in columns:
        print(i, column.name)
        if column.name == 'title':
            title_index = i
            print(title_index)
        if column.name == 'url':
            url_index = i
            print(url_index)
        i += 1
    return (title_index, url_index)


def get_data_from_db(connection):
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM " + TABLE_NAME)
        db_posts = cur.fetchall()
        title_index, url_index = get_title_url_column_number(cur)
    titles_list = [db_post[title_index] for db_post in db_posts]
    urls_list = [db_post[url_index] for db_post in db_posts]
    return titles_list, urls_list


def remove_excisted_data(title_url_list, connection):
    print('Start clearing data from already saved result')
    print('RAW DATA =', title_url_list)
    new_title_url_list = []
    titles_list, urls_list = get_data_from_db(connection)
    for title, url in title_url_list:
        if title in titles_list:
            continue
        if url in urls_list:
            continue
        new_title_url_list.append((title, url))
    print('CLEARED DATA =', new_title_url_list)
    return new_title_url_list


def load_data_to_db(title_url_raw_list):
    connection = psycopg2.connect(**DB_SETTINGS)
    title_url_list = remove_excisted_data(title_url_raw_list, connection)
    for title, url in title_url_list:
        with connection.cursor() as cur:
            cur.execute(INSERT_STR, {'title': title, 'url': url})
            connection.commit()
            print('ADDED to database title="%s" with url="%s"' % (title, url))
    connection.close()


def parse_hackernews():
    """Parse Hacker news and return parsed list of (title, url) tuples."""
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


def start_parsing():
    """Parse hackernews and load extracted data to db"""
    load_data_to_db(parse_hackernews())
