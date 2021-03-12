from rest_framework import generics
from rest_framework.response import Response
from stash_service import HttpStatusCode, AppException

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

            # version 1 code
            if version == '1':
                # your code
                return Response({'message': 'it is working'}, status=HttpStatusCode.OK.status_code())

        except KeyError:
            # Expected header is not found
            return Response(error_response(HttpStatusCode.BAD_REQUEST), status=HttpStatusCode.BAD_REQUEST.status_code())
        except AppException as e:
            # Validation Exception captured
            return Response(error_response(HttpStatusCode.PRECONDITION_FAILED), status=HttpStatusCode.PRECONDITION_FAILED.status_code())
        except:
            # Unknown exception handled
            return Response(error_response(HttpStatusCode.INTERNAL_SERVER_ERROR), status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code())

    # Forgot password
    def partial_update(self, request, *args, **kwargs):
        pass
