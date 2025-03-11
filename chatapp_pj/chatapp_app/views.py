from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import SignUpForm
from django.urls import reverse_lazy

User = get_user_model()

"""
ここでは、get_user_model()という関数を使用しています。
この関数は、AUTH_USER_MODELで設定した、現在使用しているカスタムUserモデルを取得します。
個々のビューにそれぞれカスタムUserモデルの名前を書くよりも、get_user_model()を代入したUserという変数を使う方が、
Userモデルを変更したときに、個々のビューを書き直さなくて良いという利点があります。
"""

def index(request):
    return render(request,'chatapp_app/index.html') 

class SignUpView(CreateView):
    model = User
    template_name = "chatapp_app/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')


"""
CreateViewを継承して会員登録機能をシンプルに実装しています。
いくつか設定している項目があると思うのですが、これをattributeといいます。
以下では、attributeについて解説します。

model:このビューによってどのモデルのインスタンスを作成するかを指定する
templae_name:使用するhtmlテンプレートを指定
form_class:使用するフォームクラスを指定
success_url:会員登録成功後にリダイレクトするURLを指定
"""

"""
reverse_lazy()という関数を使っています。
これを使うと、URLを名前で取得できます。
urls.pyのpath関数を見てください。nameがpath関数の第三引数になっているのがわかると思います。
これを参照して、遷移先を指定できます。
細かいことを言うと、reverse関数というものがあり、reverse_lazyはこれの遅延評価版
なのですが、今はまだ覚えなくて大丈夫です。
"""