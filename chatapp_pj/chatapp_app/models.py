from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user_icon = models.ImageField('プロフィール画像',upload_to='user_icons',default="sori_snow_boy.png")

    def __str__(self):
        return f"{self.username},{self.id}"

"""
ImageFieldは画像を扱えるモデルフィールドです。これを使うには、Pillowをpip install Pillowでinstallする必要があります。
第一引数は、verbose_nameと呼ばれるもので、このフィールドが何なのかを人間にわかりやすく説明するためものです。
本来ならverbose_name='プロフィール画像'と書くところを、第一引数に持ってくることで特別にこのような省略形でかけます。(豆知識)
他のフィールドオプションについては、自分で調べてみましょう。分からなかったら質問して良いです
"""

"""
画像を扱えるFieldには、ImageFieldやFileFiledがあります。なぜ、FileFieldではなく、ImageFiledを用いるのかなども考えてみると良いと思います。
現状では、優先度はそこまで高くないので、djangoの実装に慣れてきたら考えてみてください。
"""

class Chat(models.Model):
    chat = models.CharField('メッセージ',max_length=500)
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages',verbose_name='送信者')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages',verbose_name='受信者')
    created_at = models.DateTimeField('送信日時',auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.chat[:30]}"