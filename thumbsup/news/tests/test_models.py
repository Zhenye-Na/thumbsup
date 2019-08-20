# -*- coding: utf-8 -*-

from test_plus.test import TestCase
from thumbsup.news.models import News


class NewsModelsTest(TestCase):

    def setUp(self) -> None:
        self.user = self.make_user('user01')
        self.other_user = self.make_user('user02')
        self.first_news = News.objects.create(
            user=self.user,
            content='content no. 1'
        )
        self.second_news = News.objects.create(
            user=self.other_user,
            content='content no. 2'
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content='comment first news',
            reply=True,
            parent=self.first_news
        )

    def test__str__(self):
        self.assertEqual(self.first_news.__str__(), 'content no. 1')

    def test_switch_like(self):
        """测试用户点赞与取消点赞"""
        self.first_news.switch_like(self.user)
        assert self.first_news.like_count() == 1
        assert self.user in self.first_news.get_likers()

    def test_reply_this(self):
        """测试回复功能"""
        initial_comment_count = News.objects.count()
        self.first_news.reply_this(self.other_user, 'comment on first updates')
        assert News.objects.count() == initial_comment_count + 1
        assert self.first_news.comment_count() == 2
        assert self.third_news in self.first_news.get_thread()
