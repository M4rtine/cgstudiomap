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

import mock
from openerp.tests import common
# required for mocking.
import openerp.addons.res_partner_moderator_supervision.res_partner  # noqa

_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Test suites interaction between the create and update and the slack logger."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    @mock.patch(
        'openerp.addons.res_partner_moderator_supervision.res_partner._slack_logger'
    )
    def test_create(self, mock_log):
        """Check the log info is hit."""
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        self.assertEqual(1, mock_log.info.call_count)

    @mock.patch(
        'openerp.addons.res_partner_moderator_supervision.res_partner._slack_logger'
    )
    def test_update(self, mock_log):
        """Check the log info is hit."""
        partner = self.partner_pool.create({'name': 'tname'})
        self.assertEqual('tname', partner.name)
        partner.write({'name': 'tupdate'})
        self.assertEqual('tupdate', partner.name)
        self.assertEqual(2, mock_log.info.call_count)
