from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
    path('login/',views.SignIn.as_view(),name='login'),
    path('home/',views.HomeView.as_view(),name='home'),
]

"""
クラスベースビュー(CBV)を用いるときは.as_view()を忘れないようにしましょう
"""