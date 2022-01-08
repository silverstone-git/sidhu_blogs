from django.db import models

# Create your models here.


class article(models.Model):
    title = models.CharField(max_length=122)
    content = models.CharField(max_length=9_00_000)
    date_posted = models.DateField()


class reader(models.Model):
    username = models.CharField(max_length = 122)
    email_address = models.EmailField()
    description = models.CharField(max_length=300)
    level = models.CharField(default="novice", max_length=20)
    no_of_comments = models.IntegerField(default=0)


class comment(models.Model):
    content = models.CharField(max_length=2000)
    date_posted = models.DateField()