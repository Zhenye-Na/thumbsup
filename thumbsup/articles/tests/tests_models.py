# -*- coding: utf-8 -*-

from test_plus.test import TestCase

from thumbsup.articles.models import Article


class ArticleModelTest(TestCase):
    def setUp(self):
        """初始化操作"""
        self.user = self.make_user("test_user")
        self.other_user = self.make_user("other_test_user")
        self.article = Article.objects.create(
            title="第一篇文章",
            content="程序员梦工厂",
            status="P",
            user=self.user,
        )
        self.not_p_article = Article.objects.create(
            title="第二篇文章",
            content="""慕课网-程序员的梦工厂""",
            user=self.user,
        )

    def test_object_instance(self):
        """判断实例对象是否为 Article 类型"""
        assert isinstance(self.article, Article)
        assert isinstance(self.not_p_article, Article)
        assert isinstance(Article.objects.get_published()[0], Article)

    def test_return_values(self):
        """测试返回值"""
        assert self.article.status == "P"
        assert self.article.status != "p"
        assert self.not_p_article.status == "D"
        assert str(self.article) == "第一篇文章"  # 因为 __str__ 方法返回的是title.
        assert self.article in Article.objects.get_published()
        assert Article.objects.get_published()[0].title == "第一篇文章"
        assert self.not_p_article in Article.objects.get_drafts()
