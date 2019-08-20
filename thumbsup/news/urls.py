# -*- coding: utf-8 -*-

from django.urls import path
from thumbsup.news import views

app_name = "news"
urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
]
