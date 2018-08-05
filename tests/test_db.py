# -*- coding: utf-8 -*-
import sqlite3
import os
import pytest
from manage import setup_store

here = os.path.dirname(os.path.abspath(__file__))


class TestDB():
    db_name = os.path.join(here, '../db/test.db')

    def test_init_db(self):
        try:
            if os.path.isfile(self.db_name):
                os.remove(self.db_name)
        except OSError:
            pytest.fail('Unexpected error trying to delete {}'.format(self.db_name), pytrace=True)
        conn = sqlite3.connect(self.db_name)
        conn.close()
        assert os.path.isfile(self.db_name)

    def test_setup_store(self):
        try:
            setup_store(self.db_name)
        except sqlite3.Error:
            pytest.fail('Unexpected error trying to setup store', pytrace=True)
