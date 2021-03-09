from django.urls import re_path

from contact.views import ContactForm

urlpatterns = [
    re_path(r'^$', ContactForm.as_view(), name=''),
]
