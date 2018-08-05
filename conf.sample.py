# -*- coding: utf-8 -*-
import os

here = os.path.dirname(os.path.abspath(__file__))
sirena_endpoint = 'https://ws.sirena-travel.ru/swc-main/bookingService'


accounts = {
    'OTA.TCH': {
        'gds': '1H',
        'user': 'ota_grs101',
        'password': 'secret',
        'endpoint': sirena_endpoint,
        'alert': 200,
    },
    'OTA.UT': {
        'gds': '1H',
        'user': 'ota_grs102',
        'password': 'newsecret',
        'endpoint': sirena_endpoint,
        'alert': 200,
    },
    'OTA.S7': {
        'gds': '1A',
        'user': 'WSXXXYYY',
        'password': 'AMADEUS',
        'office_id': 'CITYY28XX',
        'duty_code': 'SU',
        'airline': 'S7',
        'endpoint': 'https://noded1.production.webservices.amadeus.com/OTAWSAP',
        'alert': 200,
    },
}
sender = ('Anton Yakovlev', 'anton.yakovlev@a.gentlemantravel.club')
recipient_info = 'airquota@ota.ru'
recipient_alert = 'airquota.alert@ota.ru'
db_name = os.path.join(here, 'db/quota.db')
smtp_gateway= 'email-smtp.eu-west-1.amazonaws.com'
smtp_port = 587
smtp_user = 'aws_ses_user'
smtp_password = 'aws_ses_user_password'
