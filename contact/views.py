from rest_framework import generics
from rest_framework.response import Response


class ContactForm(generics.RetrieveAPIView, generics.CreateAPIView):

    def retrieve(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass
