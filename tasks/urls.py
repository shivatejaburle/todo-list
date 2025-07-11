from django.urls import path
from . import views as views

app_name = 'tasks'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]