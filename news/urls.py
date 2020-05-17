from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_news_list/', views.get_news_list, name='get_news_list'),
    path('get_news_detail/', views.get_news_detail, name='get_news_detail'),
    path('modify_news_stars/', views.modify_news_stars, name='modify_news_stars'),
    path('get_comment_list/', views.get_comment_list, name='get_comment_list'),
    path('add_comment/', views.add_comment, name='add_comment'),
]