from rest_framework import generics
from rest_framework.response import Response

from orgws_common.constants import HeaderKeys
from orgws_common.utils import requested_version, error_response


class Client(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView,generics.ListAPIView):

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def create(self, request, *args, **kwargs):
        try:
            version: str = requested_version(request, kwargs)
            if version == '1':
                token: str = request.headers[HeaderKeys.TOKEN]
                body: dict = request.data
                return Response (body)
        except Exception as e:
            return error_response(e)

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass