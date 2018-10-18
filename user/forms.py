from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate

from .models import UserProfile
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
	username = forms.CharField(required=True,error_messages={'required':'用户名不能为空'})
	password = forms.CharField(required=True,error_messages={'required':'密码不能为空'})

	def clean(self):
		username = self.cleaned_data.get('username','')
		password = self.cleaned_data.get('password','')

		if not UserProfile.objects.filter(username=username).exists():
			raise forms.ValidationError('用户名不存在')

		user = authenticate(username=username,password=password)

		if not user.is_active:
			raise forms.ValidationError('用户账号未激活')

		if user is None:
			raise forms.ValidationError('账号或者密码错误')
		else:
			self.cleaned_data['user'] = user

		return self.cleaned_data

class RegisterForm(forms.Form):
	email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空'})
	password = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空'})
	password_again = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空'})
	captcha = CaptchaField(required=True,error_messages={'required':'验证码不能为空','invalid':'验证码错误'})

	def clean_email(self):
		email = self.cleaned_data.get('email','')
		if UserProfile.objects.filter(Q(username=email)|Q(email=email)).exists():
			raise forms.ValidationError('此邮箱已被注册')

		return email

	def clean_password_again(self):
		password = self.cleaned_data.get('password','')
		password_again = self.cleaned_data.get('password_again','')

		if password_again != password:
			raise forms.ValidationError('两次输入的密码不一致')

		return password_again

class ForgetPasswordForm(forms.Form):
	email = forms.EmailField(required=True,error_messages={'required':'邮箱不能为空'})
	captcha = CaptchaField(required=True,error_messages={'required':'验证码不能为空','invalid':'验证码错误'})

	def clean_email(self):
		email = self.cleaned_data.get('email','')

		if not UserProfile.objects.filter(email=email).exists():
			raise forms.ValidationError('用户邮箱不存在')

		return email

class ModifyPasswordForm(forms.Form):
	password1 = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空','min_length':'密码长度过短'})
	password2 = forms.CharField(required=True,min_length=6,error_messages={'required':'密码不能为空','min_length':'密码长度过短'})

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1','')
		password2 = self.cleaned_data.get('password2','')

		if password1 != password2:
			raise forms.ValidationError('两次输入的密码不一致')

		return password2

class ModifyUserAvaterForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ['avater']

class UserInfoForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = ['nickname','birthday','gender','address','mobile']






