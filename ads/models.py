from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Ad(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    description = models.TextField(max_length=1200, null=True)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
