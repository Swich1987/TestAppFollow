"""
Testing our API.
"""
import sys
import random
import string

import csv
import unittest

import requests
import json


URL = 'http://ec2-18-218-151-219.us-east-2.compute.amazonaws.com:8000/posts'
# URL = 'http://127.0.0.1:8000/posts'
SUCCESS_CODE = 200
BAD_REQUEST_CODE = 400
MISSING_PAGE_CODE = 404

CHECKED_LIMIT = 10
DEFAULT_LIMIT = 5
MAX_LIMIT = 25
MIN_LIMIT = 1

CHECKED_OFFSET = 3
MIN_OFFSET = 1

REQUIRED_FIELDS = ['title', 'id', 'created', 'url']
CHECKED_FIELD = REQUIRED_FIELDS[0]

WRONG_QUERY_PARAMETERS = ['order=url1',
                          'ordering=title',
                          'order',
                          'offset=10&limit=10&order=title&some=1']
WRONG_JSON = "{'error': 'wrong query parameter: "

def get_ordered_list(url):
    """Request url and return ordered dict."""
    response = requests.get(url)
    response_json = {}
    try:
        response_json = response.json()
    except Exception:
        pass
    return response_json

class TestGoodRequests(unittest.TestCase):
    """Test case for check good requests."""

    @staticmethod
    def _is_ordered_by(result_list, order_key, descending=False):
        """
        Check if result list of dict is ordered by order_key.
        desceding check if ordered in descending order.
        """
        result_list_of_order_key = [elem[order_key] for elem in result_list]
        copy_result_list_of_order_key = result_list_of_order_key.copy()
        copy_result_list_of_order_key.sort(reverse=descending)
        if not result_list_of_order_key == copy_result_list_of_order_key:
            print('Error checking order! descending =', descending)
            print('NOT equal:')
            print(result_list_of_order_key)
            print(copy_result_list_of_order_key)
        return result_list_of_order_key == copy_result_list_of_order_key

    @staticmethod
    def _validate_fields(result_list):
        """
        Check if every dict in result list have all required fields.
        """
        for post in result_list:
            if list(post.keys()) != REQUIRED_FIELDS:
                return False
        return True

    def test_posts(self):
        """Checking usual posts request for defalut limit and all fields."""
        result_list = get_ordered_list(URL)
        self.assertEqual(len(result_list), DEFAULT_LIMIT)
        self._validate_fields(result_list)

    def test_posts_ordering(self):
        """Testing ordering on all fields ascending and descending."""
        for field in REQUIRED_FIELDS:
            for descending in (False, True):
                minus = "-" if descending else ""
                with self.subTest(field=field, descending=descending):
                    result_list = get_ordered_list(URL + '?order=' + minus + field)
                    self.assertTrue(self._is_ordered_by(result_list,
                                    order_key=field,
                                    descending=descending))

    def test_posts_offsets(self):
        """Testing different offsets."""
        etalon_list = get_ordered_list(URL)
        offseted_list = get_ordered_list(URL + '?offset=' + str(CHECKED_OFFSET))
        self.assertEqual(etalon_list[CHECKED_OFFSET], offseted_list[0])
        etalon_list = get_ordered_list(URL + '?offset=-' + str(MIN_OFFSET))
        offseted_list = get_ordered_list(URL + '?offset=-' + str(CHECKED_OFFSET))
        self.assertEqual(etalon_list, offseted_list)
        self.assertEqual(etalon_list[0], offseted_list[0])

    def test_posts_limits(self):
        """Testing different limits."""
        limited_list = get_ordered_list(URL + '?limit=' + str(CHECKED_LIMIT))
        self.assertEqual(len(limited_list), CHECKED_LIMIT)
        limited_list = get_ordered_list(URL + '?limit=-' + str(CHECKED_LIMIT))
        self.assertEqual(len(limited_list), DEFAULT_LIMIT)
        limited_list = get_ordered_list(URL + '?limit=' + str(MIN_LIMIT))
        self.assertEqual(len(limited_list), MIN_LIMIT)
        limited_list = get_ordered_list(URL + '?limit=100000')
        self.assertEqual(len(limited_list), MAX_LIMIT)

    def test_posts_ordered_offseted_limited(self):
        """
        Testing use of all query parameters in 1 request:
        order, limit and offset.
        """
        etalon_list = get_ordered_list(URL + '?order=' + str(CHECKED_FIELD))
        checked_list = get_ordered_list(URL +
                                        '?order=' + str(CHECKED_FIELD) +
                                        '&offset=' + str(CHECKED_OFFSET) +
                                        '&limit=' + str(CHECKED_LIMIT))
        self.assertEqual(etalon_list[CHECKED_OFFSET], checked_list[0])
        self.assertEqual(len(checked_list), CHECKED_LIMIT)
        self.assertTrue(self._is_ordered_by(checked_list,
                                            order_key=CHECKED_FIELD))

class TestWrongRequests(unittest.TestCase):
    """Test case for check wrong requests."""

    def test_wrong_url(self):
        """Testing wrong url."""
        response = requests.get(URL[:-len('/posts')])
        self.assertEqual(response.status_code, MISSING_PAGE_CODE)

    def test_wrong_query_parameters(self):
        """Testing response for wrong query parameters."""
        for wrong_parameter in WRONG_QUERY_PARAMETERS:
            with self.subTest(wrong_parameter=wrong_parameter):
                response = requests.get(URL + '?' + wrong_parameter)
                self.assertEqual(response.status_code, BAD_REQUEST_CODE)
                response_json_str = str(response.json())
                self.assertTrue(response_json_str.startswith(WRONG_JSON))


if __name__ == '__main__':
    unittest.main()
