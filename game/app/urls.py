from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name='app'),
    path('reset/', views.reset, name='reset'),
]
