# -*- coding: utf-8 -*-
"""Django test for posts API."""
from django.test import TestCase
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

RESPONSES = [
    {
        'title': "Some test case with '",
        'url': 'http://example2.com/url.html',
        'created': '2019-03-23T19:43:49.194383Z'
    },
    {
        'title': "Some test case with '",
        'url': 'http://example2.com/url.html',
        'created': '2019-03-23T19:44:53.955272Z'
    }
]


class PostsTestCase(TestCase):
    """Django TestCase class to test all endpoint for posts application.

    Create Post and PostSerializer objects using response from RESPONSES.
    """

    def setUp(self):
        """Setup the responses which are necessary to RESPONSES and save them
        in self.responses for test in test_response.
        """
        posts = []
        serializers = []
        self.responses = []
        for response in RESPONSES:
            with self.subTest():
                title = response['title']
                url = response['url']
                created = response['created']
                post = Post.objects.create(title=title,
                                           url=url,
                                           created=created)
                posts.append(post)
        for post in posts:
            with self.subTest(current_post=post):
                ser = PostSerializer(post)
                serializers.append(ser)
        for ser in serializers:
            with self.subTest(current_serializer=ser):
                response = Response(ser.data)
                self.responses.append(response)

    def test_response(self):
        """Creating responses for serializers."""
        for i, response in enumerate(RESPONSES):
            with self.subTest(i=i):
                self.assertDictContainsSubset(response, dict(self.responses[i].data))
