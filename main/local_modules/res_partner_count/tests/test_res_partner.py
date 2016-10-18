# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging
import datetime
from openerp.tests import common

_logger = logging.getLogger(__name__)


class NewDatetime(datetime.datetime):
    """Cannot mock datetime.datetime easy
    source:
        http://stackoverflow.com/questions/4481954/python-trying-to-mock-datetime-date-today-but-not-working  # noqa

    """

    @classmethod
    def now(cls):
        return cls(1980, 4, 5, 12, 0, 0)


class TestResPartner(common.TransactionCase):
    """Test suites interaction between partner and res.partner.count.*"""

    def setUp(self):
        super(TestResPartner, self).setUp()
        # pseudo mock of datetime
        # self.__datetime will be used to restore the real datetime.datetime
        self.__datetime = datetime.datetime
        datetime.datetime = NewDatetime
        self.partner_pool = self.env['res.partner']
        self.partner1 = self.partner_pool.create({'name': 'partner1'})
        self.partner2 = self.partner_pool.create({'name': 'partner2'})

    def tearDown(self):
        """Restore datetime class to avoid any wrong interaction with other tests.

        tearDownClass should not be used here, to avoid issue if the tests are ran
        in multi-process.
        """
        datetime.datetime = self.__datetime

    def test_add_count_view(self):
        """Test the entry res.partner.count.view is created."""
        res = self.partner1.add_count_view(self.partner2)
        self.assertEqual(self.partner1, res.active_partner_id)
        self.assertEqual(self.partner2, res.passive_partner_id)

    def test_add_count_view_datetimeToNow(self):
        """Check when a count view is created, the datetime of the count is
        equal to now()"""
        count = self.partner1.add_count_view(self.partner2)
        self.assertEqual('1980-04-05 12:00:00', count.datetime)
