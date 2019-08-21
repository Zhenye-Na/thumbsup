# -*- coding: utf-8 -*-

from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from thumbsup.articles.models import Article
from thumbsup.articles.forms import ArticleForm
from thumbsup.helpers import AuthorRequiredMixin

class ArticleListView(LoginRequiredMixin, ListView):
    """已发布的文章列表"""

    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['popular_tags'] = Article.objects.get_counted_tags()
        return context

    def get_queryset(self):
        return Article.objects.get_published()


class DraftListView(ArticleListView):
    """草稿箱文章列表"""
    def get_queryset(self):
        return Article.objects.filter(user=self.request.user).get_drafts()


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """发表文章"""
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = '您的文章已经创建成功!'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """创建成功后跳转"""
        messages.success(self.request, self.message)  # 消息传递给下一次请求
        return reverse_lazy('articles:list')


class ArticleDetailView(LoginRequiredMixin, DetailView):
    """文章详情"""
    model = Article
    template_name = 'articles/article_detail.html'

    # def get_queryset(self):
    #     return Article.objects.select_related('user').filter(slug=self.kwargs['slug'])


class ArticleEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):  # 注意类的继承顺序
    """编辑文章"""
    model = Article
    message = "您的文章编辑成功!"
    form_class = ArticleForm
    template_name = 'articles/article_update.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleEditView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy('articles:article', kwargs={'slug': self.get_object().slug})
