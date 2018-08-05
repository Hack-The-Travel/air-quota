# -*- coding: utf-8 -*-
import pytest
import base64
from checkers import AmadeusQuotaChecker
from checkers.amadeus import generate_password_digest, get_nonce

toqd_rs = '''<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:awsse="http://xml.amadeus.com/2010/06/Session_v3" xmlns:wsa="http://www.w3.org/2005/08/addressing"><soapenv:Header><wsa:To>http://www.w3.org/2005/08/addressing/anonymous</wsa:To><wsa:From><wsa:Address>https://noded1.production.webservices.amadeus.com/1ASIWASIAER</wsa:Address></wsa:From><wsa:Action>http://webservices.amadeus.com/HSFREQ_07_3_1A</wsa:Action><wsa:MessageID>urn:uuid:14b4b4e7-c60d-8d44-39d9-9078af4872b5</wsa:MessageID><wsa:RelatesTo RelationshipType="http://www.w3.org/2005/08/addressing/reply">f0a708f2-ec97-4e7b-9f97-b25655a8f783</wsa:RelatesTo><awsse:Session TransactionStatusCode="End"><awsse:SessionId>01ELYEAUF9</awsse:SessionId><awsse:SequenceNumber>1</awsse:SequenceNumber><awsse:SecurityToken>31F6H6JGQ1C2JZXVAC621NI07</awsse:SecurityToken></awsse:Session></soapenv:Header><soapenv:Body><Command_CrypticReply xmlns="http://xml.amadeus.com/HSFRES_07_3_1A"><longTextString><textStringDetails>/$TICKET QUOTA SYSTEM   CONSOLIDATOR  SIBERIA AIRLINE             

AGY NO - 42112125     QUOTA PERIOD                              
                      01AUG-15AUG                   05 AUG 2018 
----------------------------------------------------------------
AIRLINE             ITIN TC/DT    PERM   CURR  ISSUED REMAINING 
----------------------------------------------------------------
S7  SIBERIA AIRLINE       TKTT     500    700     481       219 
S7  SIBERIA AIRLINE       EMDS      50     50       8        42 
 </textStringDetails></longTextString></Command_CrypticReply></soapenv:Body></soapenv:Envelope>
        '''


class TestAmadeus:
    @pytest.mark.parametrize(
        'rs, tickets_expected, emds_expected', (
            (toqd_rs, 219, 42),
        ))
    def test_extract_quota(self, rs, tickets_expected, emds_expected):
        tickets, emds = AmadeusQuotaChecker.extract_quota(rs)
        assert tickets == tickets_expected
        assert emds == emds_expected


class TestAmadeusUtils:
    @pytest.mark.parametrize(
        'nonce, timestamp, password, password_digest_64', (
            ('secretnonce10111', '2015-09-30T14:12:15Z', 'AMADEUS', '+LzcaRc+ndGAcZIXmq/N7xGes+k='),
        ))
    def test_get_password_digest(self, nonce, timestamp, password, password_digest_64):
        nonce = nonce.encode('ascii')
        timestamp = timestamp.encode('ascii')
        password = password.encode('ascii')
        password_digest = generate_password_digest(nonce, timestamp, password)
        password_digest_64 = base64.b64encode(password_digest).decode('utf-8')
        assert password_digest_64 == password_digest_64

    def test_get_nonce_length(self):
        assert len(get_nonce(100)) == 100
