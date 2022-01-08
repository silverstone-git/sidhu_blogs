from django.contrib import admin
from blogs.models import comment
from blogs.models import reader
from blogs.models import article


# Register your models here.

admin.site.register(comment)
admin.site.register(reader)
admin.site.register(article)