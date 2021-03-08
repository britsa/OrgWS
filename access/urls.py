from django.urls import re_path

from access.views import TokenHandler

urlpatterns = [
    re_path(r'^$', TokenHandler.as_view(), name=''),
]
