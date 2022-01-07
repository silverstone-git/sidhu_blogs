from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name = 'index'),
    # more paths linked to view functions here

    path('blogs/', views.blog, name = 'blog')

]
