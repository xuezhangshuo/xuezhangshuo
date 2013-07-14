#coding:utf8
from django import forms
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=38, label='')

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=20, label='真实姓名')
	email = forms.EmailField(label='电子邮箱')
	password = forms.CharField(max_length=32, widget=forms.PasswordInput, label="密码")
	password_again = forms.CharField(max_length=32, widget=forms.PasswordInput, label="重复密码")
	RRid = forms.CharField(max_length=15, required=False, label="人人主页")

class SettingForm(forms.Form):
	name = forms.CharField(max_length=20, label='真实姓名')
	# email = forms.EmailField(label='电子邮箱')
	GENDER_CHOICES = (('',' - '),('M', '男'),('F', '女'),)
	gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, label="性别")
	RRid = forms.CharField(required=False, label="人人主页")
