from django.db import models

from django.contrib.auth.models import AbstractUser
 
class User(AbstractUser):
    user_icon = models.ImageField(upload_to='user_icons')