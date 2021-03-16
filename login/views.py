from rest_framework import generics
from rest_framework.response import Response
from stash_service import HttpStatusCode, AppException

from access.views import check_security
from orgws_common.constants import HeaderKeys
from orgws_common.utils import error_response, requested_version


class Authentication(generics.CreateAPIView, generics.UpdateAPIView):

    # Sign Up
    def create(self, request, *args, **kwargs):
        pass

    # Log In
    def update(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)
            token: str = request.headers[HeaderKeys.TOKEN]
            check_security(token)

            # version 1 code
            if version == '1':
                # your code
                return Response({'message': 'it is working'}, status=HttpStatusCode.OK.status_code())

        except Exception as e:
            return error_response(e)

    # Forgot password
    def partial_update(self, request, *args, **kwargs):
        pass
