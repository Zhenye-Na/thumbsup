# -*- coding: utf-8 -*-

from django import forms
from thumbsup.articles.models import Article
from markdownx.fields import MarkdownxFormField


class ArticleForm(forms.ModelForm):
    content = MarkdownxFormField()
    status = forms.CharField(widget=forms.HiddenInput())
    edited = forms.BooleanField(widget=forms.HiddenInput(), initial=False, required=False)

    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'tags']
