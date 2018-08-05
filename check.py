# -*- coding: utf-8 -*-
import logging
from utils import db_execute

import conf
from checkers import QuotaResponse, QuotaChecker, AmadeusQuotaChecker, SirenaQuotaChecker


def save_check(db_name, account_code, quota: QuotaResponse):
    tickets = 'NULL' if quota.tickets is None else quota.tickets
    emds = 'NULL' if quota.emds is None else quota.emds
    db_execute(
        db_name,
        '''INSERT INTO quota_check (account, remaining_tickets, remaining_emds)
           VALUES ('{account}', {tickets}, {emds})
        '''.format(account=account_code, tickets=tickets, emds=emds)
    )


def get_checker(account: dict) -> QuotaChecker:
    gds = account['gds']
    if gds == '1H':
        return SirenaQuotaChecker(account['user'], account['password'], account['endpoint'])
    if gds == '1A':
        return AmadeusQuotaChecker(account['user'], account['password'], account['office_id'],
                                   account['duty_code'], account['airline'], account['endpoint'])
    return QuotaChecker()


if __name__ == '__main__':
    for code, account in conf.accounts.items():
        try:
            save_check(
                conf.db_name,
                code,
                get_checker(account).get_quota()
            )
            print('{:20} - ok'.format(code))
        except Exception as e:
            print('{:20} - error'.format(code))
            logging.critical(e, exc_info=True)
