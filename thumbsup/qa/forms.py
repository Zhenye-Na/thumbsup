# -*- coding:utf-8 -*-

from django import forms
from markdownx.fields import MarkdownxFormField

from thumbsup.qa.models import Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())  # 隐藏
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]
