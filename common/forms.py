from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .media_form import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    profile_image = forms.ImageField(required=False)  # 프로필 이미지를 업로드할 수 있는 필드 추가

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2" , "email", "first_name", "last_name")

class ModifyForm(UserChangeForm):
    email = forms.EmailField(label="이메일")

    class Meta :
        model = get_user_model()
        fields = ("email", "first_name", "last_name")
