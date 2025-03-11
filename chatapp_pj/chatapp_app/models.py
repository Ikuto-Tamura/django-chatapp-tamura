from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_icon = models.ImageField('プロフィール画像',upload_to='user_icons',default="sori_snow_boy.png")


"""
ImageFieldは画像を扱えるモデルフィールドです。これを使うには、Pillowをpip install Pillowでinstallする必要があります。
第一引数は、verbose_nameと呼ばれるもので、このフィールドが何なのかを人間にわかりやすく説明するためものです。
本来ならverbose_name='プロフィール画像'と書くところを、第一引数に持ってくることで特別にこのような省略形でかけます。(豆知識)
他のフィールドオプションについては、自分で調べてみましょう。分からなかったら質問して良いです
"""