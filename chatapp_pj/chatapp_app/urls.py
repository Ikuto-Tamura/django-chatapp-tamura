from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/',views.SignUpView.as_view(),name='signup'),
]

"""
クラスベースビュー(CBV)を用いるときは.as_view()を忘れないようにしましょう
"""