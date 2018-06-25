# -*- coding: utf-8 -*-
import re
import requests
from utils import db_execute
import conf


def extract_ticket_quota(ticket_quota_response):
    matches = re.findall(r'<quota>(\d+)<\/quota>', ticket_quota_response)
    return int(matches[0])


def get_ticket_quota(user, password, gateway='https://ws.sirena-travel.ru/swc-main/bookingService'):
    """Returns ticket quota for PoS (ППр).

    This method calls `getTicketQuota` method of Sirena WS.

    :param user: Sirena WS user with supervisor permission in the PoS.
    :param password: user password.
    :param gateway: (optional) Sirena WS gateway to call getTicketQuota method.
    :return: ticket quota.
    :rtype: int
    """
    rq = '''<soapenv:Envelope
       xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
       xmlns:ser="http://service.swc.comtech/">
       <soapenv:Header/>
       <soapenv:Body>
          <ser:getTicketQuota>
             <dynamicId>0</dynamicId>
          </ser:getTicketQuota>
       </soapenv:Body>
    </soapenv:Envelope>'''
    r = requests.post(gateway, auth=(user, password), data=rq)
    r.raise_for_status()
    return extract_ticket_quota(r.text)


def save_check(db_name, account_code, ticket_quota):
    db_execute(
        db_name,
        '''INSERT INTO quota_check (account, quota)
           VALUES ('{account}', {quota})
        '''.format(account=account_code, quota=ticket_quota)
    )


if __name__ == '__main__':
    for code, account in conf.accounts.items():
        try:
            save_check(
                conf.db_name,
                code,
                get_ticket_quota(account['user'], account['password'])
            )
            print('{:20} - ok'.format(code))
        except Exception:
            print('{:20} - error'.format(code))
