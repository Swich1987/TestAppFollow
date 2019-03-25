# -*- coding: utf-8 -*-
from django.http import HttpResponseBadRequest
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Post


def error_response(error_str):
    response = HttpResponseBadRequest('{"error": "%s"}' % error_str)
    return response


class LimitOffsetSettings(LimitOffsetPagination):
    default_limit = 5
    max_limit = 25
    min_limit = 1
    min_offset = 1

    def get_paginated_response(self, data):
        return Response(data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows posts to be viewed
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetSettings

    def list(self, request, *args, **kwargs):
        self.queryset = self.filter_queryset(self.get_queryset())

        allowed_params = ['order', 'offset', 'limit']
        params = request.query_params
        for param in params:
            if param not in allowed_params:
                return error_response("wrong query parameter: " + param)

        allowed_order = ['title', 'id', 'created', 'url']
        if 'order' in params:
            order = params['order']
            if order.startswith('-') and len(order) > 1:
                order = order[1:]
            if order not in allowed_order:
                return error_response("wrong query parameter: " + order)
            self.queryset = self.queryset.order_by(params['order'])

        return super().list(self, request, *args, **kwargs)
