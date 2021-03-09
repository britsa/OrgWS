from django.urls import re_path

from login.views import Authentication

urlpatterns = [
    re_path(r'^$', Authentication.as_view(), name = ''),
]
