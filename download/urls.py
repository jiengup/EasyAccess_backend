from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_resource_list/', views.get_resource_list, name='get_resource_list'),
]