# -*- coding: utf-8 -*-
accounts = {
    'OTA.TCH': {
        'user': 'ota_grs101',
        'password': 'secret',
    },
    'OTA.UT': {
        'user': 'ota_grs102',
        'password': 'newsecret',
    },
}
sender = ('Anton Yakovlev', 'anton.yakovlev@a.gentlemantravel.club')
recipient_info = 'airquota@ota.ru'
recipient_alert = 'airquota.alert@ota.ru'
db_name = 'db/quota.db'
smtp_gateway= 'email-smtp.eu-west-1.amazonaws.com'
smtp_port = 587
smtp_user = 'aws_ses_user'
smtp_password = 'aws_ses_user_password'
