import re
from django import forms

from Mxonline.settings import REGEX_MOBILE
from user.models import UserProfile
from course.models import Course
from .models import UserAsk

class UserAskForm(forms.ModelForm):

	def clean_name(self):
		name = self.cleaned_data.get('name','')

		if not UserProfile.objects.filter(username=name).exists():
			raise forms.ValidationError('用户名不存在')

		return name

	def clean_mobile(self):
		moblie = self.cleaned_data.get('moblie','')

		if not re.match(REGEX_MOBILE,moblie):
			raise forms.ValidationError('手机号码非法')

		return moblie

	def clean_course_name(self):
		course_name = self.cleaned_data.get('course_name','')

		if not Course.objects.filter(name=course_name).exists():
			raise forms.ValidationError('课程不存在')

		return course_name

	class Meta:
		model = UserAsk
		fields = ['name','mobile','course_name']