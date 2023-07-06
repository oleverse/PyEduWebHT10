from django.urls import path, re_path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    re_path('^page/(?P<page_number>[0-9]+)?', views.main, name='main-paged'),
    re_path(r'^tag/(?P<tag_slug>[0-9a-zA-Z-]+)(?:/page/(?P<page_number>[0-9]+))?', views.tag, name='tag'),
    path('author/<str:author_slug>', views.author, name='author'),
    path('add-author', views.add_author, name='add-author'),
    path('add-quote', views.add_quote, name='add-quote'),
]
