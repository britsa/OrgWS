from datetime import datetime as dt, timedelta
from hashlib import sha1

from orgws_common import constants
from orgws_common.constants import TOKEN_SPAN_MINUTES


def generate_new_token(client_id: str) -> tuple:
    now = dt.now()
    hash_string: str = client_id + dt.strftime(now, constants.DATETIME_FORMAT)
    hash_string_encoded = str.encode(hash_string)
    db_object: dict = {
        u'owner_id': client_id,
        u'creation_date': dt.strftime(now, constants.DATETIME_FORMAT),
        u'span_time': str(TOKEN_SPAN_MINUTES),
        u'expiry_date': dt.strftime(now + timedelta(minutes=TOKEN_SPAN_MINUTES), constants.DATETIME_FORMAT)
    }
    return sha1(hash_string_encoded).hexdigest(), db_object


class TokenInformation(object):
    def __init__(self, db_source) -> None:
        if not type(db_source) == dict:
            db_source: dict = db_source.to_dict()

        self.__client_id: str = db_source[u'owner_id']
        self.__effective_date: str = db_source[u'creation_date']
        self.__expiration_date: str = db_source[u'expiry_date']
        self.__span: str = db_source[u'span_time']

    def show_info(self) -> dict:
        response: dict = {
            u'Client': {
                u'Id': self.__client_id
            }, u'Token': {
                u'EffectiveDate': self.__effective_date,
                u'Span': self.__span,
                u'ExpirationDate': self.__expiration_date
            }
        }
        return response

    def validity_info(self) -> tuple:
        expiry_date = dt.strptime(self.__expiration_date, constants.DATETIME_FORMAT)
        now = dt.strptime(dt.strftime(dt.now(), constants.DATETIME_FORMAT), constants.DATETIME_FORMAT)

        response: dict = {
            u'Validity': now < expiry_date
        }
        return response, now < expiry_date

    def new_token_info(self, token: str) -> dict:
        response: dict = {
            u'Token': token,
            u'EffectiveDate': self.__effective_date,
            u'Span': self.__span,
            u'ExpirationDate': self.__expiration_date
        }
        return response

    def all_info(self, all_details: dict):
        response, _ = self.validity_info()
        response[u'Information'] = all_details
        return response
