from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('send_auth_code', views.send_auth_code, name='send_auth_code'),
    path('login', views.login, name="login"),
]