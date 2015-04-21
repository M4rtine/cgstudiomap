# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp.tests.common import TransactionCase


class TestResPartner(TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.res_partner_pool = self.env['res.partner']
        self.res_country_pool = self.env['res.country']

        self._valid_address = [
            {
                'street': 'Chemin de la palombiere',
                'zip': '64150',
                'city': 'Mourenx',
                'country_id': self.res_country_pool.search(
                    [('name', 'ilike', 'France')]
                )[0].id
            },
            {
                'street': '7345 Boulevard Saint Laurent',
                'zip': 'H2R',
                'city': 'Montreal',
                'country_id': self.res_country_pool.search(
                    [('name', 'ilike', 'Canada')]
                )[0].id
            },
            {
                'street': 'Chaussée de Namur 40',
                'zip': '1367',
                'city': 'Grand-Rosière',
                'country_id': self.res_country_pool.search(
                    [('name', 'ilike', 'Belgium')]
                )[0].id
            },
        ]

    def test_unvalid_location(self):
        with self.assertRaises(ValidationError):
            self.res_partner_pool.create({
                'name': 't_name',
                'street': 'somewhere',
                'city': 'somecity',
                'zip': '123H2R',
                'country_id': 3
            })
