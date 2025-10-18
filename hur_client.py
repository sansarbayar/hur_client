import zeep
import time
import urllib3
import base64

from zeep import helpers
from requests import Session
from base64 import b64encode

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

HUR_PKEY_PATH = '# PRIVATE KEY FILE PATH #'
HUR_ACCESS_TOKEN = '# ACCESS TOKEN #'

HUR_SERVICES = {
    'WS100101_getCitizenIDCardInfo': 'https://xyp.gov.mn/citizen-1.3.0/ws?WSDL',
    'WS100103_getCitizenAddressInfo': 'https://xyp.gov.mn/citizen-1.3.0/ws?WSDL',
    'WS100126_getCitizenNonPaymentInfo': 'https://xyp.gov.mn/citizen-1.3.0/ws?WSDL',
    'WS100501_getCitizenSalaryInfo': 'https://xyp.gov.mn/insurance-1.3.0/ws?WSDL',
    'WS100202_getPropertyList': 'https://xyp.gov.mn/property-1.3.0/ws?WSDL',
    'WS100406_getCitizenVehicleList': 'https://xyp.gov.mn/transport-1.3.0/ws?WSDL',
}


def sign_hur():
    sign_data = {
        'accessToken': HUR_ACCESS_TOKEN,
        'timeStamp': str(int(time.time())),
    }
    param = '%s.%s' % (sign_data['accessToken'], sign_data['timeStamp'])

    with open(HUR_PKEY_PATH, 'rb') as keyfile:
        private_key = RSA.importKey(keyfile.read())

    digest = SHA256.new()
    digest.update(param.encode('utf-8'))
    signature = b64encode(PKCS1_v1_5.new(private_key).sign(digest))

    return sign_data, signature


def call_hur_service(service_name, params=None):
    try:
        if service_name not in HUR_SERVICES:
            raise Exception('%s service not found.' % service_name)

        sign_data, signature = sign_hur()

        urllib3.disable_warnings()
        session = Session()
        session.verify = False

        transport = zeep.Transport(session=session, timeout=15)
        client = zeep.Client(wsdl=HUR_SERVICES[service_name], transport=transport)

        client.transport.session.headers.update({
            'accessToken': sign_data['accessToken'],
            'timeStamp': sign_data['timeStamp'],
            'signature': signature,
        })

        if params:
            response = client.service[service_name](params)
        else:
            response = client.service[service_name]()

        result = helpers.serialize_object(response, target_cls=dict)

        # Иргэний үнэмлэх лавлагаа үед цээж зургийг byte array-с base64 руу хөрвуулж байна.
        if service_name == 'WS100101_getCitizenIDCardInfo' and result.get('resultCode', None) == 0 and result['response']['image']:
            result['response']['image'] = base64.b64encode(result['response']['image']).decode('utf-8')

        return result

    except Exception as ex:
        raise Exception('ХУР лавлагаа татахад алдаа гарлаа, service: %s, error: %s' % (service_name, ex))
