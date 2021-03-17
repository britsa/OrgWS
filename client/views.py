from rest_framework import generics
from rest_framework.response import Response
from stash_service import connect_firestore_with_key

from access.views import check_security
from client.models import ClientInformation
from orgws_common import constants
from orgws_common.constants import HeaderKeys, Collections
from orgws_common.utils import requested_version, error_response, get_env


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
                check_security(token)
                body: dict = request.data
                info:ClientInformation =ClientInformation(body)
                clientid: str = 'KA2910'
                connect_firestore_with_key(Collections.CUSTOMER, get_env(constants.FIREBASE_CERT)).document(clientid).set(info.db_info())

                return Response (body)
        except Exception as e:
            return error_response(e)

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass