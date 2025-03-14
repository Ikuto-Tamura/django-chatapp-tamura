from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',views.SignIn.as_view(),name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/',views.HomeView.as_view(),name='home'),
    path('talk_room/<int:pk>/', views.TalkRoomView.as_view(), name='talk_room'),
    path('settings/',views.SettingView.as_view(),name='settings'),
    path('settings/password_change/',views.MyPasswordChangeView.as_view(),name='password_change'),
]

"""
クラスベースビュー(CBV)を用いるときは.as_view()を忘れないようにしましょう
"""