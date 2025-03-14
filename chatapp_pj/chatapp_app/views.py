import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import OuterRef, Q, Subquery
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from .forms import ProfileEditForm, SignUpForm
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
    
    #すでにログインしている場合にこのページを訪れようとしたらhomeにリダイレクトされる処理
    def dispatch(self, request, *args, **kwargs):
        # ログインしている場合、他のページにリダイレクト
        if request.user.is_authenticated:
            return redirect('home')  # リダイレクト先のURLを指定
        return super().dispatch(request, *args, **kwargs)

"""
htmlを描写するだけであれば、TemplateViewを継承し、template_nameを指定するだけでとてもシンプルに書くことができます。
"""


"""
(発展)
ここで、dispatchメソッドというものをオーバーライドしています。
dispatchメソッドの本来の役割はここでは解説しません。
しかし、大事なこととしてdispatchメソッドは、Viewが呼び出されたときに最初に発動するメソッドです。
そのため、dispatchメソッドを改良してリダイレクトの処理を加えることで一貫とした処理を効率的に加えることができます。
もし、ログインしている状態であればdispatchメソッドはhomeという名前のURLにリダイレクトするメソッドに変化し、
そうでなければ本来の親クラス(TemplateView)のdispatchメソッドの機能を果たすように条件分岐しています。
"""

"""
(発展)
dispatchメソッドの改良で、条件分岐が加わっていることを解説しました。
条件分岐は、本来であればif節とelse節、場合によってはelif節を書くと勉強したのではないでしょうか。
しかし、returnがif節の処理に入っている場合、このようにelse節を省略して書くことができます。
この知識はよく使うので覚えておくと良いです。
"""

class SignUpView(CreateView):
    model = User
    template_name = "chatapp_app/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        # ログインしている場合、他のページにリダイレクト
        if request.user.is_authenticated:
            return redirect('home')  # リダイレクト先のURLを指定
        return super().dispatch(request, *args, **kwargs)


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
    paginate_by = 5

    def get_queryset(self):
        # ログインユーザー以外のUserを取得
        return User.objects.exclude(id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logged_in_user'] = self.request.user

        # 各ユーザーの最新メッセージを取得するために、annotateを使用
        users = context['users']

        # 最新メッセージを取得するサブクエリ
        latest_message_subquery = Chat.objects.filter(
            Q(sender=self.request.user, receiver=OuterRef('pk')) |
            Q(sender=OuterRef('pk'), receiver=self.request.user)
        ).order_by('-created_at')

        # 各ユーザーに対して最新メッセージを追加する
        users = users.annotate(
            latest_message=Subquery(latest_message_subquery.values('chat')[:1]),
            latest_message_time=Subquery(latest_message_subquery.values('created_at')[:1]),
        )

        # コンテキストに追加するリストを準備
        user_and_latest_messages = []
        for user in users:
            user_and_latest_messages.append({
                'user': user,
                'message': user.latest_message,
                'time': user.latest_message_time,
            })

        # 時間順にソート
        user_and_latest_messages.sort(
            key=lambda x: x['time'] if x['time'] is not None else timezone.make_aware(datetime.datetime.min),
            reverse=True
        )

        context['user_and_latest_messages'] = user_and_latest_messages

        return context



    
"""
context_object_nameやpagenate_byを設定すると何ができるようになるか調べてみましょう。
get_queryset(self)とget_context_data(self,**kwargs)は頻出のメソッドです。それぞれどのようなメソッドかを調べてみましょう。
今回は、オーラバーライドしてget_querysetやget_context_dataが独自の処理を施すようにカスタマイズしています。
(モデル).objects.excludeや(モデル).objects.filterといった記述が出てきますが、これはORMという概念を理解することでコードの
意味を理解できるようになると思います。
次の記事が分かりやすいです。
https://qiita.com/sotaheavymetal21/items/34cf15d0b5f4ac0a2d0f
QオブジェクトやSubquery,OuterRefやannotateなどは大事なのでこれも意味を理解するようにしましょう。
これらの意味がわかれば、このViewの意味も理解できるはずです。
ソートの処理はそこまで頻出ではないと思います。Noneを含むソートがあるので、複雑な処理となっています。
私も初めて知りました。
"""


class TalkRoomView(LoginRequiredMixin, TemplateView):
    model = User
    template_name = 'chatapp_app/talk_room.html'

    def get_queryset(self):
        # 自分と相手のメッセージをすべて取得（時系列順に並び替え）
        other_user = get_object_or_404(User, id=self.kwargs['pk'])

        # メッセージが存在しなくてもアクセス可能
        messages = Chat.objects.filter(
                Q(sender=self.request.user, receiver=other_user) | Q(sender=other_user, receiver=self.request.user)
            ).select_related('sender', 'receiver').order_by('created_at')
        return messages

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
    
"""
HomeViewでオーバーライドしたget_querysetやget_context_dataに加え、postというメソッドをオーバーライドしています。
talk_roomでは、単にページにアクセスするだけでなく、メッセージを送信するという機能があり、POSTの処理が必要になるからですね。
get_object_or_404も大事なので覚えましょう。
message = request.POST.get('message')はhtmlのフォームを復習すれば意味がつかめると思います。
今度は(モデル).obejcts.createというORMが登場しています。新しいインスタンスを作成するORMがこれに該当し、
この処理を楽にかけるようにしたのが実はCreateViewです。今回はすこし複雑なので、自分でこのロジックを実装しています。
"""

"""(発展)
.select_related('sender', 'receiver')という記述があります。
これはN+1問題を解消するもので、基本的に必須の処理になります。
今すぐでなくていいですが、いずれ覚えるようにしましょう。
"""


class SettingView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'chatapp_app/settings.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
    """
    UpdateViewは本来複数個作成されるインスタンスを編集対象としています。例えば、ブログアプリであれば記事などです。
    だから、get_objectはpkやslugなどそのインスタンスのidにあたるものをurlとして要求するのですが、自分のプロフィール
    編集のURLに自分のidを含めるなどをしない場合は、編集対象を自分に書き換えることでこの問題を解決できます。
    """
    
class MyPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'chatapp_app/password_change.html'
    success_url = reverse_lazy('home')
