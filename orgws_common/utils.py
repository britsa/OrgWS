"""
This orgws_common.utils will have all the support methods and classes that can be utilised in the application.
"""
import logging
import os

from orgws_common import constants
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


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
    # TODO: Raise exception here


# slices the version number from the input of format 'v[0-9]+'
def requested_version(request, kwargs: dict) -> str:
    version: str = kwargs[constants.API_VERSION][1:]  # slices to a string by leaving the first character
    logger.info(
        f"OrgWS v{version} ({get_env(constants.CURRENT_ENV)}) | {request.method} '{request.get_full_path()}'")
    return version
