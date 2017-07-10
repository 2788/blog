from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import ugettext, ugettext_lazy as _

import re


def lowercase_email(email):
        """
        Normalize the address by lowercasing the domain part of the email
        address.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

class SignupForm(forms.ModelForm):
    username = forms.CharField(
        label='用户名',required=True,error_messages={'required':'请填入用户名啊!','max_length':'最多只能输入15个字符','min_length':'至少输入3个字符'},max_length=15,min_length=6,widget=forms.TextInput(attrs={'placeholder':'6~20位字母/数字/汉字'}))
    password = forms.CharField(
        label='密码', required=True,error_messages={'required': '请填写你的密码','max_length':'最多输入20个字符','min_length':'最少6个字符'},widget=forms.TextInput(attrs={'placeholder':'6~20位字母/数字'}))
    confirm_password = forms.CharField(
        label='确认密码', required=True,error_messages={'required': '请填写你的密码','max_length':'最多输入20个字符','min_length':'最少6个字符'},widget=forms.TextInput(attrs={'placeholder':'6~20位字母/数字'}))

    class Meta:
        model = get_user_model()
        fields = ("username", "password",)


    def clean_confirm_password(self):
        UserModel = get_user_model()
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data["confirm_password"]
        if password == confirm_password:
            return password
        raise forms.ValidationError("确认密码和密码不一致")

    def clean_username(self):
        UserModel = get_user_model()
        username = self.cleaned_data['username']
        n = re.sub('[^\u4e00-\u9fa5a-zA-Z]', '', username)

        mgc = ['admin','fanhuaxiu','繁花社长']

        if n in mgc:
            raise forms.ValidationError("这么好的名字当然被人提前预定啦，换一个试试^-^")
        try:
            UserModel._default_manager.get(username = username)
        except UserModel.DoesNotExist:
            return username
        raise forms.ValidationError("有人已经注册了这个用户名")

class SigninForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':'请填入用户名啊!','max_length':'最多只能输入15个字符','min_length':'至少输入3个字符'})
    password = forms.CharField(required=True,error_messages={'required': '请填写你的密码','max_length':'最多输入20个字符','min_length':'最少6个字符'})

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_password(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        User = authenticate(username=username,password=password)
        if User:
            return password
        else:
            raise forms.ValidationError("用户名或者密码错误!")

class BlogForm(forms.Form):
    title = forms.CharField(required=True,max_length=20,min_length=1,widget=forms.TextInput(attrs={'placeholder':'标题'}))
    summary = forms.CharField(required=True, max_length=150,min_length=1,widget=forms.TextInput(attrs={'placeholder':'摘要'}))
    content = forms.CharField(required=True,min_length=1,widget=forms.Textarea(attrs={'placeholder':'正文'}))

class CommentForm(forms.Form):
    content = forms.CharField(required=True,min_length=1,widget=forms.Textarea(attrs={'placeholder':'正文'}))
