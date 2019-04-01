#coding:utf-8
from django import forms
from society.models import *
from django.utils.translation import ugettext_lazy as _


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['type', 'content']
        widgets = {
            'type': forms.TextInput(attrs={'class': 'input-text', 'id': 'type'}),
            'content': forms.Textarea(attrs={'class': 'textarea', 'onkeyup': '(this).Huitextarealength(this,200)', 'id': 'content'})
        }


# class StuForm(forms.Form):
#     class Meta:
#         model = Student
#         fields = ['username', 'password', 'phone']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'contact_name', 'placeholder': '你的用户名...'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control', 'id': 'contact_pass', 'placeholder': '你的密码...'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'id': 'contact_phone', 'placeholder': '你的手机号...'})
#         }

# 社团负责人资料修改
class PriForm(forms.ModelForm):
    class Meta:
        model = Principal
        fields = ('photo', 'info', 'phone')
        labels = {'photo': _('头像'), 'info': _('简介'), 'phone': _('手机号')}
        widgets = {
            'info': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '写点什么？'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入手机号'})
        }


#密码修改
# class PripassForm(forms.Form):
