from rest_framework import generics
from rest_framework.response import Response
from stash_service import HttpStatusCode

from orgws_common.utils import requested_version


class TokenHandler(generics.RetrieveAPIView, generics.CreateAPIView):

    def retrieve(self, request, *args, **kwargs):
        try:
            version: str = requested_version(request, kwargs)
            if version == '1':
                pass
            return Response({'message': request.headers}, status=HttpStatusCode.OK.status_code())
        except:
            return Response({'message': 'Failed'}, status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code())

    def create(self, request, *args, **kwargs):
        try:
            pass
        except:
            pass
