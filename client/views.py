from rest_framework import generics
from rest_framework.response import Response
from stash_service import connect_firestore_with_key, HttpStatusCode

from access.views import check_security
from client.models import ClientInformation, give_new_client_id
from orgws_common import constants
from orgws_common.constants import HeaderKeys, Collections
from orgws_common.utils import requested_version, error_response, get_env


class Client(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView, generics.ListAPIView):

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
                info: ClientInformation = ClientInformation(body)
                client_id: str = give_new_client_id(info)
                connect_firestore_with_key(Collections.CUSTOMER, get_env(constants.FIREBASE_CERT)).document(
                    client_id).set(info.db_info())

                return Response({
                    u'ClientId': client_id
                }, status=HttpStatusCode.OK.status_code())
        except Exception as e:
            return error_response(e)

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        pass
