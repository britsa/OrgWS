class ContactInformation(object):
    def __init__(self,body: dict):
        self.__name: str = body[u'Name']
        self.__mail_id: str = body[u'Mail-Id']
        self.__phone: str = body[u'Phone']
        self.__note: str = body[u'Note']
        self.__primary: bool = body[u'Primary']

class ClientInformation(object):
    def __init__(self, body: dict):
        self.__admin_id: str = body[u'AdminId']
        self.__company_name: str = body[u'CompanyName']
        self.__contact: list =body[u'Contact']
        