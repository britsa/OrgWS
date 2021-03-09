from django.urls import re_path

from client.views import client

urlpatterns = [
    re_path(r'^$', client.as_view(), name = ''),
]
