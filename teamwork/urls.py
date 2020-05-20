from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_tag_list', views.get_tag_list, name='get_tag_list'),
    path('get_teacher_list', views.get_teacher_list, name='get_teacher_list'),
    path('get_wanted_list', views.get_wanted_list, name='get_wanted_list'),
    path('get_wanted_detail/', views.get_wanted_detail, name='get_wanted_detail'),
    path('publish', views.publish, name='publish'),
]