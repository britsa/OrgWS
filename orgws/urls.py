from django.contrib import admin
from django.urls import path, re_path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/(?P<version>(v1))/token', include('access.urls')),
    re_path(r'^api/(?P<version>(v1))/contact', include('contact.urls')),
    re_path(r'^api/(?P<version>(v1))/client', include('client.urls')),

]
