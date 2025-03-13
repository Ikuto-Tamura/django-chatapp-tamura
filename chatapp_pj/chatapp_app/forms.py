from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "user_icon")


"""
get_user_model()についてはvies.pyのところで解説しています
"""