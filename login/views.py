from rest_framework import generics
from rest_framework.response import Response


class Authentication(generics.CreateAPIView, generics.UpdateAPIView):

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass
