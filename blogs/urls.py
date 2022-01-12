from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name = 'index'),
    # more paths linked to view functions here

    path('blogs/', views.blog, name = 'blog'),
    path('login/', views.log_in, name = 'login'),
    path('create-account/', views.create_account, name = 'create_account'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('contact/', views.contact, name = 'contact'),
    path('log-out/', views.log_out, name = 'log_out')

]
