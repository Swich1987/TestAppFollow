from django.db import models

class Post(models.Model):
    title = models.TextField()
    url = models.TextField()
    created = models.DateTimeField('date created')
