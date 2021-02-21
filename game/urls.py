from django.contrib import admin
from django.urls import path
from . import views

# This is the urls.py where you can change the url patterns and provide an URL to views.
urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('<int:pk>', views.game, name='detail'),
]
