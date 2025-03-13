import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import SignUpForm
from .models import Chat

User = get_user_model()

"""
ここでは、get_user_model()という関数を使用しています。
この関数は、AUTH_USER_MODELで設定した、現在使用しているカスタムUserモデルを取得します。
個々のビューにそれぞれカスタムUserモデルの名前を書くよりも、get_user_model()を代入したUserという変数を使う方が、
Userモデルを変更したときに、個々のビューを書き直さなくて良いという利点があります。
"""



class IndexView(TemplateView):
    template_name = 'chatapp_app/index.html'
    
    def dispatch(self, request, *args, **kwargs):
        # ログインしている場合、他のページにリダイレクト
        if request.user.is_authenticated:
            return redirect('home')  # リダイレクト先のURLを指定
        return super().dispatch(request, *args, **kwargs)

"""
htmlを描写するだけであれば、TemplateViewを継承することでとてもシンプルに書くことができます。
"""

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

class SignIn(LoginView):
    template_name = 'chatapp_app/login.html'
    redirect_authenticated_user = True

"""
Login機能はLoginViewを継承することで簡単に実装することができます。
redirect_authenticated_userというattributeをTrueに設定していますが、これが何なのか調べてみましょう。
Falseにしてみて、挙動の変化を確かめてみるのもいい実験だと思います。
ちなみに、管理画面adminにログインしていると、ログインしている扱いになってしまいます。
これは、ログインの情報をrequest.sessionで管理しているからです。
ログイン機能の挙動を確認したいときは、一旦adminからログアウトすることが必要になったりします。
"""





class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'chatapp_app/home.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ログインしているユーザーを 'logged_in_user' というコンテキストに追加
        context['logged_in_user'] = self.request.user
        
        # 各ユーザーとの最新のトークを格納するリストを初期化
        users = context['users']
        latest_messages = []

        for user in users:
            # ログインユーザーとその友達との間のメッセージを取得
            message = Chat.objects.filter(
                Q(sender=self.request.user, receiver=user) | Q(sender=user, receiver=self.request.user)
            ).order_by('-created_at').first()  # 最新のメッセージを取得

            if message:
                latest_messages.append({'user': user, 'message': message.chat, 'time':message.created_at})  # ユーザーとメッセージをタプルとして格納
            else:
                latest_messages.append({'user': user, 'message': None,'time':None})  # メッセージがない場合はNoneを格納
                
        latest_messages.sort(
            key=lambda x: x['time'] if x['time'] is not None else timezone.make_aware(datetime.datetime.min),
            reverse=True
        )

        context['latest_messages'] = latest_messages  # コンテキストに追加

        return context

    
"""
context_object_nameを設定すると何ができるようになるか調べてみましょう。
get_queryset(self)とget_context_data(self,**kwargs)は頻出のメソッドです。それぞれどのようなメソッドかを調べてみましょう。
今回は、オーラバーライドしてget_querysetが独自の処理を施すようにカスタマイズしています。
ここでは、ORM(Object-Relational Mapping)という概念が登場します。
次の記事が分かりやすいです。
https://qiita.com/sotaheavymetal21/items/34cf15d0b5f4ac0a2d0f
"""


class TalkRoomView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'chatapp_app/talk_room.html'

    def get_queryset(self):
        # 自分と相手のメッセージをすべて取得（時系列順に並び替え）
        other_user = get_object_or_404(User, id=self.kwargs['pk'])

        # メッセージが存在しなくてもアクセス可能
        messages = Chat.objects.filter(
            sender=self.request.user, receiver=other_user
        ) | Chat.objects.filter(
            sender=other_user, receiver=self.request.user
        )
        return messages.order_by('created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messages'] = self.get_queryset()
        context['other_user'] = get_object_or_404(User, id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        other_user = get_object_or_404(User, id=self.kwargs['pk'])
        message = request.POST.get('message')

        if message:
            Chat.objects.create(
                sender=request.user,
                receiver=other_user,
                chat=message
            )
            return HttpResponseRedirect(reverse('talk_room', kwargs={'pk': other_user.pk}))

        return self.get(request, *args, **kwargs)
