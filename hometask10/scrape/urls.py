from django.urls import path
from . import views

app_name = 'scrape'

urlpatterns = [
    path('', views.main, name='main'),
]
