# -*- coding: utf-8 -*-
import random
import uuid
import base64
import re
from hashlib import sha1
from datetime import datetime
from typing import Tuple

from .quotachecker import QuotaChecker, QuotaResponse


def get_nonce(n: int=8) -> bytes:
    """Return random byte string of length n.

    :param n: length of the returned string.
    :return: random string.
    """
    chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    random_string = ''.join(random.SystemRandom().choice(chars) for _ in range(n))
    return random_string.encode('ascii')


def generate_password_digest(nonce: bytes, timestamp: bytes, password: bytes) -> bytes:
    """Generate password digest.

    :param nonce: random string.
    :param timestamp: current UTC timestamp in ISO format, e.g. '2018-08-04T17:13:14.105Z'.
    :param password: raw password obtained from Amadeus.
    :return: password digest.
    """
    return sha1(nonce + timestamp + sha1(password).digest()).digest()


class AmadeusQuotaChecker(QuotaChecker):
    def __init__(self, user: str, password: str, office_id: str, duty_code: str, airline: str, endpoint: str):
        QuotaChecker.__init__(self, template_dir='templates')
        self.user = user
        self.password = password
        self.office_id = office_id
        self.duty_code = duty_code
        self.airline = airline
        self.endpoint = endpoint

    @staticmethod
    def extract_quota(ticket_quota_response: str) -> Tuple[int, int]:
        """Extract number of remaining tickets and EMDs.

        Extract or die trying.

        :param ticket_quota_response: response of CommandCryptic service for toqd/t-YY request.
        :return: number of remaining tickets and EMDs.
        """
        matches = re.findall(r'<textStringDetails>([\S\s]+)<\/textStringDetails>', ticket_quota_response)
        output_strings = str(matches[0]).split('\n')
        tickets_matches = re.findall(r'TKTT\ +\d+\ +\d+\ +\d+\ +(\d+)', output_strings[-3])
        tickets = int(tickets_matches[0])
        emds_matches = re.findall(r'EMDS\ +\d+\ +\d+\ +\d+\ +(\d+)', output_strings[-2])
        emds = int(emds_matches[0])
        return tickets, emds

    def get_quota(self):
        soap_action = 'http://webservices.amadeus.com/HSFREQ_07_3_1A'
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.105Z')
        nonce = get_nonce()
        password_digest = generate_password_digest(nonce, timestamp.encode('ascii'), self.password.encode('ascii'))
        headers = {
            'Content-Type': 'text/xml;charset=UTF-8',
            'SOAPAction': soap_action,
        }
        rq = self.render_template('amadeus_command_cryptic.xml', context={
            'message_id': str(uuid.uuid4()),
            'soap_action': soap_action,
            'endpoint': self.endpoint,
            'username': self.user,
            'password': base64.b64encode(password_digest).decode('utf-8'),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'created': timestamp,
            'duty_code': self.duty_code,
            'pseudo_city_code': self.office_id,
            'airline': self.airline,
        })
        rs = self.request(self.endpoint, headers=headers, data=rq)
        quota = QuotaResponse()
        quota.tickets, quota.emds = self.extract_quota(rs)
        return quota
