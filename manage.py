# -*- coding: utf-8 -*-
import argparse
from utils import db_execute
from conf import db_name


def setup_store(db_name):
    db_execute(
        db_name,
        '''CREATE TABLE IF NOT EXISTS quota_check (
            id INTEGER PRIMARY KEY,
            account VARCHAR,
            quota INTEGER,
            created_at integer(4) not null default (strftime('%s','now'))
        )'''
    )


def drop_store(db_name):
    db_execute(db_name, 'DROP TABLE IF EXISTS quota_check')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', type=str, choices=['setup', 'drop'],
                        help='what to do with store of quota checks')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.command == 'setup':
        setup_store(db_name)
    elif args.command == 'drop':
        drop_store(db_name)
