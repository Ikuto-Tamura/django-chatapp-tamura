from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

"""
get_user_model()についてはvies.pyのところで解説しています
"""

# 会員登録フォーム
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "user_icon")

# プロフィール編集フォーム
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_icon']

