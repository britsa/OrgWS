from rest_framework import generics
from rest_framework.response import Response
from stash_service import HttpStatusCode, connect_firestore_with_key, AppException

from access import models
from access.models import TokenInformation
from orgws_common import constants
from orgws_common.constants import HeaderKeys, Collections
from orgws_common.utils import requested_version, get_env, error_response
from orgws_common.validators import validate_information_header, validate_boolean_header


class TokenHandler(generics.RetrieveAPIView, generics.CreateAPIView):

    # GET method
    def retrieve(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)

            # version 1 code
            if version == '1':
                # extract the headers
                token_value: str = request.headers[HeaderKeys.TOKEN]
                if validate_information_header(request.headers):
                    information_required: bool = validate_boolean_header(request.headers[HeaderKeys.INFORMATION])

                    # information_required = True -> Sends the information of the token
                    if information_required:
                        # establishing connection to Firebase DB
                        database_data = connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(token_value).get()

                        # verifying the token existence in DB
                        if database_data.exists:
                            token_info: TokenInformation = TokenInformation(database_data)
                            # token is found. Information is collected. Sending to the consumer
                            return Response(token_info.show_info(), status=HttpStatusCode.OK.status_code())
                        else:
                            # token is not found. Forbidden message will send to the consumer
                            return Response(error_response(HttpStatusCode.FORBIDDEN), status=HttpStatusCode.FORBIDDEN.status_code())

                # information_required = False or Not found -> Validates the token
                # establishing connection to Firebase DB
                database_data = connect_firestore_with_key(Collections.TOKEN,get_env(constants.FIREBASE_CERT)).document(token_value).get()

                # verifying the token existence in DB
                if database_data.exists:
                    token_info: TokenInformation = TokenInformation(database_data)
                    # token is found. Validity information is collected.
                    response, still_valid = token_info.validity_info()

                    if not still_valid:
                        # If the token is expired, then the token is deleted.
                        connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(token_value).delete()

                    # Response is send to the consumer
                    return Response(response, status=HttpStatusCode.OK.status_code())
                else:
                    # token is not found. Forbidden message will send to the consumer
                    return Response(error_response(HttpStatusCode.FORBIDDEN), status=HttpStatusCode.FORBIDDEN.status_code())
        except KeyError:
            # Expected header is not found
            return Response(error_response(HttpStatusCode.BAD_REQUEST), status=HttpStatusCode.BAD_REQUEST.status_code())
        except AppException as e:
            # Validation Exception captured
            return Response(error_response(HttpStatusCode.PRECONDITION_FAILED), status=HttpStatusCode.PRECONDITION_FAILED.status_code())
        except:
            # Unknown exception handled
            return Response(error_response(HttpStatusCode.INTERNAL_SERVER_ERROR), status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code())

    # POST method
    def create(self, request, *args, **kwargs):
        try:
            # find the version from the URL
            version: str = requested_version(request, kwargs)

            # version 1 code
            if version == '1':
                # extract the headers
                client_id: str = request.headers[HeaderKeys.CLIENT_ID]

                # generating the SHA 1 token for the client-ID
                sha1_token, db_source = models.generate_new_token(client_id)

                # establishing connection to Firebase DB and the data is sent to DB
                connect_firestore_with_key(Collections.TOKEN, get_env(constants.FIREBASE_CERT)).document(sha1_token).set(db_source)
                # New information is updated to the DB. Success message will send to the consumer
                return Response(TokenInformation(db_source).new_token_info(sha1_token), status=HttpStatusCode.OK.status_code())
        except KeyError:
            # Expected header is not found
            return Response(error_response(HttpStatusCode.BAD_REQUEST), status=HttpStatusCode.BAD_REQUEST.status_code())
        except AppException as e:
            # Validation Exception captured
            return Response(error_response(HttpStatusCode.PRECONDITION_FAILED), status=HttpStatusCode.PRECONDITION_FAILED.status_code())
        except:
            # Unknown exception handled
            return Response(error_response(HttpStatusCode.INTERNAL_SERVER_ERROR), status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code())
