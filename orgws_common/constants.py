"""
This orgws_common.constants will have all the necessary key constants that can be used in the application.
"""

# .env keys
CURRENT_ENV: str = 'APP_ENV'
FIREBASE_CERT: str = 'FIREBASE_KEY'

# Path Params
API_VERSION: str = 'version'

# other constants
DATETIME_FORMAT: str = '%d-%m-%Y %H:%M:%S'
TOKEN_SPAN_MINUTES: int = 60


class Collections(object):
    TOKEN = 'token'
    CUSTOMER = 'customer'


# header keys
class HeaderKeys(object):
    INFORMATION = 'information'
    TOKEN = 'token'
    CLIENT_ID = 'client-ID'
    SECURITY = 'security'
