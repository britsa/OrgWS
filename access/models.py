from datetime import datetime as dt, timedelta
from hashlib import sha1

from orgws_common import constants


def generate_new_token(client_id: str) -> tuple:
    span: int = 60  # minutes
    now = dt.now()
    hash_string: str = client_id + dt.strftime(now, constants.DATETIME_FORMAT)
    hash_string_encoded = str.encode(hash_string)
    db_object: dict = {
        u'owner_id': client_id,
        u'creation_date': dt.strftime(now, constants.DATETIME_FORMAT),
        u'span_time': str(span),
        u'expiry_date': dt.strftime(now + timedelta(minutes=span), constants.DATETIME_FORMAT)
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
        print(expiry_date, now, type(expiry_date), type(now))

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
