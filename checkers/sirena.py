# -*- coding: utf-8 -*-
import re
from .quotachecker import QuotaChecker, QuotaResponse


class SirenaQuotaChecker(QuotaChecker):
    def __init__(self, user: str, password: str, endpoint: str):
        QuotaChecker.__init__(self, template_dir='templates')
        self.user = user
        self.password = password
        self.endpoint = endpoint

    @staticmethod
    def extract_ticket_quota(ticket_quota_response: str) -> int:
        """Extract number of remaining tickets.

        Extract or die trying.

        :param ticket_quota_response: text of getTicketQuota method response.
        :return: number of remaining tickets.
        """
        matches = re.findall(r'<quota>(\d+)<\/quota>', ticket_quota_response)
        return int(matches[0])

    def get_quota(self):
        rq = self.render_template('sirena_get_ticket_quota.xml', context=None)
        rs = self.request(self.endpoint, auth=(self.user, self.password), data=rq)
        quota = QuotaResponse()
        quota.tickets = self.extract_ticket_quota(rs)
        return quota
