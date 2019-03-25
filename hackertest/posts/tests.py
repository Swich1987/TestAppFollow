# -*- coding: utf-8 -*-
from rest_framework.response import Response

from django.test import TestCase

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
    def setUp(self):
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
