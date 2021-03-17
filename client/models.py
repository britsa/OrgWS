from datetime import datetime

from orgws_common import constants


class ContactInformation(object):
    def __init__(self,body: dict):
        self.__name: str = body[u'Name']
        self.__mail_id: str = body[u'Mail-Id']
        self.__phone: str = body[u'Phone']
        self.__note: str = body[u'Note']
        self.__primary: bool = body[u'Primary']

    def db_info(self):
        info: dict={
            u'person_name':self.__name,
            u'email_address':self.__mail_id,
            u'mobile_number':self.__phone,
            u'description':self.__note,
            u'primary_contact':self.__primary
        }

class ClientInformation(object):
    def __init__(self, body: dict):
        self.__admin_id: str = body[u'AdminId']
        self.__company_name: str = body[u'CompanyName']
        self.__contact: list =body[u'Contact']

    def db_info(self):
        info: dict={
            u'active':False,
            u'approver_id' :{
                u'activated' :None,
                u'inactivated' :None,
                u'on_boarded' :self.__admin_id
            },
            u'company_name':self.__company_name,
            u'contact_info':[ContactInformation(each).db_info() for each in self.__contact],
            u'effective_dates':
                {
                    u'activation':None,
                    u'inactivation':None,
                    u'on_boarding':datetime.strftime(datetime.now(), constants.DATETIME_FORMAT)
                },
            u'updates':[

            ]


        }
        return info

        