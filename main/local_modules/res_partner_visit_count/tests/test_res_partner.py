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

from openerp.tests import common

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites to make sure the model is set has wanted."""

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    def test_field_visit_count(self):
        """Double check the field is here and accepts integers."""
        partner = self.partner_pool.create({'name': 'tname', 'visit_count': 1})
        self.assertEqual(1, partner.visit_count)
        partner.write({'visit_count': 666})
        self.assertEqual(666, partner.visit_count)
