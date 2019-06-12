# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.TextField()
    url = models.TextField()
    created = models.DateTimeField('date created', default=timezone.now)
