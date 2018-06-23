# -*- coding: utf-8 -*-
import pytest
from checker import extract_ticket_quota


class TestChecker:
    @pytest.mark.parametrize('rs', [
        '<quota>958</quota>',
        '<quota>0958</quota>'
    ])
    def test_extract_quota(self, rs):
        assert extract_ticket_quota(rs) == 958
