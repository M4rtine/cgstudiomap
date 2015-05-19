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
        self.valid_email = 'cgstudiomap@gmail.com'
        self.invalid_email = 'not_valid_email'

    def test_validate_during_create_valid_email(self):
        partner = self.partner_pool.create(
            {'name': 't_name', 'email': self.valid_email}
        )
        self.assertEqual(partner.email, self.valid_email)

    def test_validate_during_create_invalid_email(self):
        self.assertRaises(
            ValidationError,
            self.partner_pool.create,
            {'name': 't_name', 'email': self.invalid_email}
        )

    def test_validate_during_write_valid_email(self):
        partner = self.partner_pool.create(
            {'name': 't_name'}
        )
        partner.write({'email': self.valid_email})
        self.assertEqual(partner.email, self.valid_email)

    def test_validate_during_write_invalid_email(self):
        partner = self.partner_pool.create({'name': 't_name'})
        self.assertRaises(
            ValidationError,
            partner.write,
            {'email': self.invalid_email}
        )

