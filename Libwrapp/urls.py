from django.conf.urls import url
from . import views, downloader

urlpatterns = [
    url(r'^$', views.main, name='main'),
    url(r'^load', downloader.load, name='main'),
]