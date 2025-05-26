from django.urls import path
from . import views


urlpatterns = [
    path('', views.warehouse_list, name='warehouse-list'),
    path('create/', views.warehouse_create, name='warehouse-create'),
]
