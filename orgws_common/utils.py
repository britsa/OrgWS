"""
This orgws_common.utils will have all the support methods and classes that can be utilised in the application.
"""
import logging
import os

from rest_framework.response import Response

from orgws_common import constants
from dotenv import load_dotenv
from stash_service import AppResponseCodes, AppException, HttpStatusCode

logger = logging.getLogger(__name__)


class AppCodes(AppResponseCodes):
    INVALID_BOOLEAN_HEADER_VALUE = (2001, 'Invalid boolean value passed in header')
    ENVIRONMENT_NOT_FOUND = (2002, 'Requested Key not found on the .env file')
    INVALID_TOKEN = (2003, 'Requested token either expired or unavailable in the database')


# get_env() returns the value for the matched key in .env file
def get_env(key: str) -> str:
    response_value: str or None = os.environ.get(key)
    if response_value:
        response_value = str(response_value)
        return response_value
    else:
        logger.warning('Application loading .env file')
        load_dotenv()
        logger.info('.env loaded successfully.')
        response_value = os.environ.get(key)
        if response_value:
            response_value = str(response_value)
            return response_value
    raise AppException(AppCodes.ENVIRONMENT_NOT_FOUND, key, False)


# slices the version number from the input of format 'v[0-9]+'
def requested_version(request, kwargs: dict) -> str:
    version: str = kwargs[constants.API_VERSION][1:]  # slices to a string by leaving the first character
    logger.info(
        f"OrgWS v{version} ({get_env(constants.CURRENT_ENV)}) | {request.method} '{request.get_full_path()}'")
    return version


def error_response_body(httpStatusCode: HttpStatusCode) -> dict:
    response: dict = {u'Error': {
        'Code': httpStatusCode.status_code(),
        'Message': httpStatusCode.status_message()
        }
    }
    return response


def error_response(exception: Exception) -> Response:
    if type(exception) == KeyError:
        # Expected key not found in the request or dictionary
        return Response(error_response_body(HttpStatusCode.BAD_REQUEST), status=HttpStatusCode.BAD_REQUEST.status_code())

    elif type(exception) == AppException:
        # Validation exception found
        return Response(error_response_body(HttpStatusCode.PRECONDITION_FAILED), status=HttpStatusCode.PRECONDITION_FAILED.status_code())

    else:
        # Other exceptions found
        return Response(error_response_body(HttpStatusCode.INTERNAL_SERVER_ERROR), status=HttpStatusCode.INTERNAL_SERVER_ERROR.status_code())
