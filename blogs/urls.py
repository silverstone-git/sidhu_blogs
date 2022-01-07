from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.homepage, name = 'homepage'),
    # more paths linked to view functions here

    path('blogs/', views.index, name = 'blogs')

]
