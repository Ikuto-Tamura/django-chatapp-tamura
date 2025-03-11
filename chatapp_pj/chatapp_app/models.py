from django.db import models

from django.contrib.auth.models import AbstractUser
 
class User(AbstractUser):
    user_icon = models.ImageField('画像',upload_to='user_icons',default="sori_snow_boy.png")