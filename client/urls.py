from django.urls import re_path

from client.views import Client

urlpatterns = [
    re_path(r'^$', Client.as_view(), name = ''),
]
