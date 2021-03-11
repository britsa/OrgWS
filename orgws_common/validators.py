from stash_service import AppException

# /token
from orgws_common.constants import HeaderKeys
from orgws_common.utils import AppCodes


def validate_information_header(headers: dict) -> bool or AppException:
    return HeaderKeys.INFORMATION in headers.keys()


def validate_boolean_header(value: str) -> bool:
    if value == 'true' or value == 'True':
        return True
    elif value == 'false' or value == 'False':
        return False
    raise AppException(AppCodes.INVALID_BOOLEAN_HEADER_VALUE, 'Invalid Header value Found', True)
