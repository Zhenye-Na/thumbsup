# -*- coding: utf-8 -*-

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy

from thumbsup.helpers import ajax_required, AuthorRequiredMixin
from thumbsup.news.models import News


class NewsListView(LoginRequiredMixin, ListView):
    """首页动态"""
    model = News
    paginate_by = 20
    template_name = 'news/news_list.html'

    def get_queryset(self):
        return News.objects.filter(reply=False).select_related('user', 'parent').prefetch_related('liked')


class NewsDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    """删除动态"""
    model = News
    template_name = 'news/news_confirm_delete.html'
    # slug_url_kwarg = 'slug' 通过 url 传入想要删除的对象主键 id, 默认值是 slug
    # pk_url_kwarg = 'pk' 通过 url 传入想要删除的对象主键 id, 默认值是 pk
    success_url = reverse_lazy('news:list')  # 使用 reverse_lazy() 而不是 reverse() 的好处是可以在项目 URLConf 未加载前使用


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_news(request):
    """发送动态, Ajax POST 请求"""
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user, content=post)
        html = render_to_string('news/news_single.html', {'news': posted, 'request': request})
        return HttpResponse(html)
    else:
        return HttpResponseBadRequest('内容不能为空!')


@login_required
@ajax_required
@require_http_methods(['POST'])
def like(request):
    """点赞, Ajax POST 请求"""
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    # 取消或者添加赞
    news.switch_like(request.user)
    # 返回赞的数量
    return JsonResponse({'likes': news.like_count()})


@login_required
@ajax_required
@require_http_methods(['GET'])
def get_thread(request):
    """返回动态的评论, AJAX GET 请求"""
    news_id = request.GET['news']
    news = News.objects.select_related('user').get(pk=news_id)  # 不是 .get(pk=news_id).select_related('user')

    # render_to_string()表示加载模板, 填充数据, 返回字符串
    news_html = render_to_string('news/news_single.html', {'news': news})  # 没有评论, 返回单条动态
    thread_html = render_to_string('news/news_thread.html', {'thread': news.get_thread()}) # 有评论时, 返回动态所有评论

    return JsonResponse({
        'uuid': news_id,
        'news': news_html,
        'thread': thread_html
    })


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_comment(request):
    """给动态评论, Ajax POST 请求"""
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({
            'comments': parent.comment_count()
        })
    else:
        return HttpResponseBadRequest('内容不能为空!')


@login_required
@ajax_required
@require_http_methods(["POST"])
def update_interactions(request):
    """更新互动信息"""
    data_point = request.POST['id_value']
    news = News.objects.get(pk=data_point)
    return JsonResponse({'likes': news.like_count(), 'comments': news.comment_count()})
