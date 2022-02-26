from django.db import models
from time import time

# Create your models here.


class article(models.Model):
    name = models.CharField(max_length=300, default="origin_13_jan_2022")
    title = models.CharField(max_length=122)
    content = models.CharField(max_length=9_00_000)
    date_posted = models.DateField()


class reader(models.Model):
    username = models.CharField(max_length = 122)
    email_address = models.EmailField()
    description = models.CharField(max_length=300)
    level = models.CharField(default="novice", max_length=20)
    no_of_comments = models.IntegerField(default=0)
    saved_articles = models.CharField(max_length=1_00_000, default="[]")


class comment(models.Model):
    comment_id = models.CharField(default = str(time()), max_length=300)
    content = models.CharField(default = "Bruh", max_length=2000)
    author = models.CharField(default = "Anonymous", max_length=122)
    blogname = models.CharField(default = "origin_13_jan_22", max_length=300)
    no_of_upvotes = models.IntegerField(default = 0)
