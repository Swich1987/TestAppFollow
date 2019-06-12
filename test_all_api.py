# -*- coding: utf-8 -*-
""" Testing our API.

That test is used for external test of the API using requests.

URL - set URL for testing

REQUIRED_FIELDS - list of fields, that must be in response

WRONG_QUERY_PARAMETERS - list of checked wrong requests parameters

WRONG_JSON - start of response from server on wrong request
"""

import configparser
import os
import sys
import unittest
from http import HTTPStatus

import requests
from simplejson import JSONDecodeError

URL = 'http://ec2-18-218-151-219.us-east-2.compute.amazonaws.com:8000/posts'

WRONG_QUERY_PARAMETERS = ['order=url1',
                          'ordering=title',
                          'order',
                          'offset=10&limit=10&order=title&some=1']

WRONG_JSON = "{'error': 'wrong query parameter: "

REQUIRED_FIELDS = ['title', 'id', 'created', 'url']

_CHECKED_FIELD = REQUIRED_FIELDS[0]

_path_to_settings = os.path.join(sys.path[0], 'hackertest', 'settings.ini')
_config = configparser.ConfigParser()
_config.read(_path_to_settings)

_CHECKED_LIMIT = _config.getint('DJANGO', 'CHECKED_LIMIT')
_DEFAULT_LIMIT = _config.getint('DJANGO', 'DEFAULT_LIMIT')
_MAX_LIMIT = _config.getint('DJANGO', 'MAX_LIMIT')
_MIN_LIMIT = _config.getint('DJANGO', 'MIN_LIMIT')

_CHECKED_OFFSET = _config.getint('DJANGO', 'CHECKED_OFFSET')
_MIN_OFFSET = _config.getint('DJANGO', 'MIN_OFFSET')


def _get_ordered_list(url):
    """Request url and return ordered dict. Print error if there is exception."""
    response = requests.get(url)
    response_json = {}
    try:
        response_json = response.json()
    except JSONDecodeError as ecs:
        print('Error! %s' % ecs)
    return response_json


class TestGoodRequests(unittest.TestCase):
    """Test case for check good requests."""

    @staticmethod
    def _is_ordered_by(result_list, order_key, descending=False):
        """Check if result list of dict is ordered by order_key.

        Desceding check if ordered in descending order.
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
        """Check if every dict in result list have all required fields."""
        for post in result_list:
            if list(post.keys()) != REQUIRED_FIELDS:
                return False
        return True

    def test_posts(self):
        """Checking usual posts request for defalut limit and all fields."""
        result_list = _get_ordered_list(URL)
        self.assertEqual(len(result_list), _DEFAULT_LIMIT)
        self._validate_fields(result_list)

    def test_posts_ordering(self):
        """Testing ordering on all fields ascending and descending."""
        for field in REQUIRED_FIELDS:
            for descending in (False, True):
                minus = "-" if descending else ""
                with self.subTest(field=field, descending=descending):
                    result_list = _get_ordered_list(URL + '?order=' + minus + field)
                    self.assertTrue(self._is_ordered_by(result_list,
                                                        order_key=field,
                                                        descending=descending))

    def test_posts_offsets(self):
        """Testing different offsets."""
        etalon_list = _get_ordered_list(URL)
        offseted_list = _get_ordered_list(URL + '?offset=' + str(_CHECKED_OFFSET))
        self.assertEqual(etalon_list[_CHECKED_OFFSET], offseted_list[0])
        etalon_list = _get_ordered_list(URL + '?offset=-' + str(_MIN_OFFSET))
        offseted_list = _get_ordered_list(URL + '?offset=-' + str(_CHECKED_OFFSET))
        self.assertEqual(etalon_list, offseted_list)
        self.assertEqual(etalon_list[0], offseted_list[0])

    def test_posts_limits(self):
        """Testing different limits."""
        limited_list = _get_ordered_list(URL + '?limit=' + str(_CHECKED_LIMIT))
        self.assertEqual(len(limited_list), _CHECKED_LIMIT)
        limited_list = _get_ordered_list(URL + '?limit=-' + str(_CHECKED_LIMIT))
        self.assertEqual(len(limited_list), _DEFAULT_LIMIT)
        limited_list = _get_ordered_list(URL + '?limit=' + str(_MIN_LIMIT))
        self.assertEqual(len(limited_list), _MIN_LIMIT)
        limited_list = _get_ordered_list(URL + '?limit=100000')
        self.assertEqual(len(limited_list), _MAX_LIMIT)

    def test_posts_ordered_offseted_limited(self):
        """Testing use of all query parameters in 1 request (order, limit and offset)."""
        etalon_list = _get_ordered_list(URL + '?order=' + str(_CHECKED_FIELD))
        checked_list = _get_ordered_list(URL +
                                         '?order=' + str(_CHECKED_FIELD) +
                                         '&offset=' + str(_CHECKED_OFFSET) +
                                         '&limit=' + str(_CHECKED_LIMIT))
        self.assertEqual(etalon_list[_CHECKED_OFFSET], checked_list[0])
        self.assertEqual(len(checked_list), _CHECKED_LIMIT)
        self.assertTrue(self._is_ordered_by(checked_list,
                                            order_key=_CHECKED_FIELD))


class TestWrongRequests(unittest.TestCase):
    """Test case for check wrong requests."""

    def test_wrong_url(self):
        """Testing wrong url."""
        response = requests.get(URL[:-len('/posts')])
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_wrong_query_parameters(self):
        """Testing response for wrong query parameters."""
        for wrong_parameter in WRONG_QUERY_PARAMETERS:
            with self.subTest(wrong_parameter=wrong_parameter):
                response = requests.get(URL + '?' + wrong_parameter)
                self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
                response_json_str = str(response.json())
                self.assertTrue(response_json_str.startswith(WRONG_JSON))


if __name__ == '__main__':
    unittest.main()
