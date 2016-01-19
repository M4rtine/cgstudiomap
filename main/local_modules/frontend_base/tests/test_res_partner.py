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
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    def test_small_image_url_exists(self):
        """Check if the field exist on res.partner."""
        partner = self.partner_pool.create({
            'name': 'tpartner',
            'small_image_url': 'tsmall_image_url',
        })
        self.assertFalse(partner.small_image_url)

    def test_write_resetSmallImageUrl(self):
        """Check if the field small_image_url is reset when image is set."""
        partner = self.partner_pool.create({
            'name': 'tpartner',
            'small_image_url': 'tsmall_image_url',
        })
        self.assertEqual(
            partner.small_image_url, 'tsmall_image_url'
        )
        partner.write({'image': False})
        self.assertFalse(partner.small_image_url)
