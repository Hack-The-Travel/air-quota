# -*- coding: utf-8 -*-
import pytest
from checkers import SirenaQuotaChecker

ticket_quota_rs = '''<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <ns2:getTicketQuotaResponse xmlns:ns2="http://service.swc.comtech/">
            <return>
                <quota>714</quota>
            </return>
        </ns2:getTicketQuotaResponse>
    </soap:Body>
</soap:Envelope>'''


class TestSirena:
    @pytest.mark.parametrize(
        'rs, expected', (
            ('<quota>958</quota>', 958),
            ('<quota>0958</quota>', 958),
            (ticket_quota_rs, 714),
        ))
    def test_extract_ticket_quota(self, rs, expected):
        tickets = SirenaQuotaChecker.extract_ticket_quota(rs)
        assert tickets == expected
