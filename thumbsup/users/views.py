# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    """用户详情"""
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "users/user_detail.html"


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """用户只能更改自己的信息"""
    model = User
    fields = ['nickname', 'email', 'picture', 'introduction', 'job_title', 'location', 'personal_url', 'weibo', 'zhihu',
              'github', 'linkedin']
    template_name = 'users/user_form.html'

    def get_success_url(self):
        """更新成功后跳转的页面"""
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user
        # return User.objects.get(username=self.request.user.username)
