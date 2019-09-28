from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    """验证是否是 AJAX 请求"""

    @wraps(f)
    def wrap(request, *args, **kwargs):
        """判断 request 是否是 AJAX 请求"""
        if not request.is_ajax():
            return HttpResponseBadRequest('不是 AJAX 请求!')
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):
    """验证是否为作者, 用于状态删除, 文章编辑"""

    def dispatch(self, request, *args, **kwargs):
        # 状态实例, 文章实例有 user 属性
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
