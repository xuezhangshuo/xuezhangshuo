#coding:utf8
from django import forms
from account.models import *
    
class SearchForm(forms.Form):
    query = forms.CharField(max_length=38, label='')

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=20, label='姓名')
	email = forms.EmailField(label='电子邮箱')
	password = forms.CharField(max_length=32, min_length=6, widget=forms.PasswordInput, label="密码")
	password_again = forms.CharField(max_length=32, min_length=6, widget=forms.PasswordInput, label="重复密码")
	RRid = forms.CharField(max_length=30, required=False, label="人人主页", help_text="可选，未来打算用作获取头像")

	def clean_email(self):
		data = self.cleaned_data['email']
		try:
			user = xzsUser.objects.get(email=data)
		except xzsUser.DoesNotExist:
			return data
		else:
			raise forms.ValidationError("该邮箱已存在")

	def clean_password_again(self):
		password = self.cleaned_data['password']
		password_again = self.cleaned_data['password_again']
		if password != password_again:
			raise forms.ValidationError("两次密码输入不一致")
		else:
			return password

class SettingForm(forms.Form):
	name = forms.CharField(max_length=20, label='真实姓名')
	# email = forms.EmailField(label='电子邮箱')
	GENDER_CHOICES = (('',' - '),('M', '男'),('F', '女'),)
	gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False, label="性别")
	RRid = forms.CharField(required=False, label="人人主页")
