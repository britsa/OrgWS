from rest_framework import generics
from rest_framework.response import Response
from stash_service import HttpStatusCode, connect_firestore_with_key, AppException, Logger, logger

from access import models
from access.models import TokenInformation
from orgws_common import constants
from orgws_common.constants import HeaderKeys, Collections
from orgws_common.utils import requested_version, get_env, error_response, error_response_body, AppCodes
from orgws_common.validators import validate_information_header, validate_boolean_header, validate_security_header


def fetch_all_token_details(token: str) -> dict or None:
    # establishing connection to Firebase DB
    database_data = connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(
        token).get()

    # verifying the token existence in DB
    if database_data.exists:
        token_info: TokenInformation = TokenInformation(database_data)
        info_response = token_info.show_info()
        return info_response
    return None


def fetch_token_validity(token: str) -> tuple or None:
    # establishing connection to Firebase DB
    database_data = connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(
        token).get()

    # verifying the token existence in DB
    if database_data.exists:
        token_info: TokenInformation = TokenInformation(database_data)
        return token_info.validity_info(), token_info
    return None


def check_security(token: str) -> None or AppException:
    info_response: dict = fetch_all_token_details(token)
    if info_response:
        (_, valid), __ = fetch_token_validity(token)
        if valid:
            logger.info(f"{info_response[u'Client'][u'Id']} has the requested service")
            return None
    logger.info(f"'{token}' is either expired or unavailable")
    raise AppException(AppCodes.INVALID_TOKEN)


class TokenHandler(generics.RetrieveDestroyAPIView, generics.CreateAPIView):

    # GET method
    def retrieve(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)

            # version 1 code
            if version == '1':
                # extract the headers
                token_value: str = request.headers[HeaderKeys.TOKEN]

                security_header_available: bool = False
                if validate_security_header(request.headers):
                    security_header_available = validate_boolean_header(request.headers[HeaderKeys.SECURITY])

                info_response: dict = {}
                if validate_information_header(request.headers) or security_header_available:

                    information_required: bool = True
                    if validate_information_header(request.headers):
                        information_required = validate_boolean_header(request.headers[HeaderKeys.INFORMATION])

                    # information_required = True -> Sends the information of the token
                    if information_required or security_header_available:
                        info_response = fetch_all_token_details(token_value)
                        if info_response:
                            # token is found. Information is collected. Sending to the consumer
                            if not security_header_available:
                                return Response(info_response, status=HttpStatusCode.OK.status_code())
                        else:
                            # token is not found. Forbidden message will send to the consumer
                            return Response(error_response_body(HttpStatusCode.FORBIDDEN),
                                            status=HttpStatusCode.FORBIDDEN.status_code())

                # information_required = False or Not found -> Validates the token
                validity_info: tuple = fetch_token_validity(token_value)
                if validity_info:
                    # token is found. Validity information is collected.
                    (response, still_valid), token_info = validity_info

                    if not still_valid:
                        # If the token is expired, then the token is deleted.
                        connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(
                            token_value).delete()

                    # Response is send to the consumer
                    if not security_header_available:
                        return Response(response, status=HttpStatusCode.OK.status_code())
                    else:
                        return Response(token_info.all_info(info_response), status=HttpStatusCode.OK.status_code())
                else:
                    # token is not found. Forbidden message will send to the consumer
                    return Response(error_response_body(HttpStatusCode.FORBIDDEN),
                                    status=HttpStatusCode.FORBIDDEN.status_code())

        except Exception as e:
            return error_response(e)

    # POST method
    def create(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)

            # version 1 code
            if version == '1':
                # extract the headers
                client_id: str = request.headers[HeaderKeys.CLIENT_ID]

                # check whether the client ID is valid and active
                db_info = connect_firestore_with_key(Collections.CUSTOMER, get_env(constants.FIREBASE_CERT)).document(
                    client_id).get()
                if not db_info.exists:
                    return Response(error_response_body(HttpStatusCode.FORBIDDEN),
                                    status=HttpStatusCode.FORBIDDEN.status_code())
                elif not db_info.to_dict()[u'active']:
                    return Response(error_response_body(HttpStatusCode.NOT_ACCEPTABLE),
                                    status=HttpStatusCode.NOT_ACCEPTABLE.status_code())

                # generating the SHA 1 token for the client-ID
                sha1_token, db_source = models.generate_new_token(client_id)

                # establishing connection to Firebase DB and the data is sent to DB
                connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(
                    sha1_token).set(db_source)
                # New information is updated to the DB. Success message will send to the consumer
                return Response(TokenInformation(db_source).new_token_info(sha1_token),
                                status=HttpStatusCode.OK.status_code())

        except Exception as e:
            return error_response(e)

    # DELETE method
    def destroy(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)

            # version 1 code
            if version == '1':
                # extract the headers
                client_id: str = request.headers[HeaderKeys.CLIENT_ID]

                # retrieving all the token documents which were generated by the requested Client-ID
                all_documents = connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).where(
                    u'owner_id', u'==', client_id).stream()

                for document in all_documents:
                    token_info: TokenInformation = TokenInformation(document)
                    # token is found. Validity information is collected.
                    _, still_valid = token_info.validity_info()

                    # deleting the document if it is not valid
                    if not still_valid:
                        connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(
                            document.id).delete()

                # Success response is sent to the consumer
                return Response(status=HttpStatusCode.NO_CONTENT.status_code())

        except Exception as e:
            return error_response(e)
