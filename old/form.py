#coding:utf8
from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(max_length=20, label='大名')
    comment = forms.CharField(widget=forms.Textarea,label='评论')
    rate = forms.IntegerField()
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=38, label='')

