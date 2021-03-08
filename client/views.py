from rest_framework import generics
from rest_framework.response import Response

class Client(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView,generics.ListAPIView):

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass