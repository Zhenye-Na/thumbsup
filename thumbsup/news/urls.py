# -*- coding: utf-8 -*-

from django.urls import path
from thumbsup.news import views

app_name = "news"
urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
    path("post-news/", views.post_news, name="post_news"),
    path("delete/<str:pk>",  views.NewsDeleteView.as_view(), name="delete_news"),
    path("like/", views.like, name="like_post"),
    path("get-thread/", views.get_thread, name="get_thread"),
    path("post-comment/", views.post_comment, name="post_comment"),
    path('update-interactions/', views.update_interactions, name='update_interactions'),
]
