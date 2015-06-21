# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
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
from pygeolib import GeocoderResult
from openerp.tests import common
from ..models import res_partner


class TestResPartner(common.TransactionCase):
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.res_partner_pool = self.env['res.partner']
        self.res_country_pool = self.env['res.country']
        self.res_state_pool = self.env['res.country.state']
        self.ir_model_data_pool = self.env['ir.model.data']

        self.france = self.ir_model_data_pool.get_object('base', 'fr')
        self.canada = self.ir_model_data_pool.get_object('base', 'ca')
        self.usa = self.ir_model_data_pool.get_object('base', 'us')
        self.turkey = self.ir_model_data_pool.get_object('base', 'tr')

    def test_codec(self):
        self.assertEqual(res_partner.__codec__, 'utf-8')

    def test_address_update(self):
        partner = self.res_partner_pool.create({
            'name': 't_name',
            'street': 'Chemin de la palombiere',
            'zip': '64150',
            'country_id': self.france.id,
            'city': 'mourenx'
        })

        self.assertEqual(partner.city, 'Mourenx')
        self.assertEqual(partner.street, u'Rue de la Palombi\xe8re')

    def test_create_state(self):
        """Even if the given address does not have a state, the process
        creates the appropriate one.
        """
        partner = self.res_partner_pool.create({
            'name': 't_name',
            'street': 'Chemin de la palombiere',
            'zip': '64150',
            'country_id': self.france.id,
            'city': 'mourenx'
        })

        self.assertEqual(partner.state_id.name, 'Aquitaine')

    def test_street2_does_not_change(self):
        partner = self.res_partner_pool.create({
            'name': 't_name',
            'street': 'Chemin de la palombiere',
            'street2': 'appt 207',
            'zip': '64150',
            'country_id': self.france.id,
            'city': 'mourenx'
        })

        self.assertEqual(partner.street2, 'appt 207')

    def test_tricky_addresses(self):
        """These addresses should not fail."""
        partner = self.res_partner_pool.create({
            'name': u't_street_and_city_with_é',
            'street': u'5455 Av. de Gaspé',
            'street2': u'suite 900',
            'zip': u'H2T 3B3',
            'country_id': self.canada.id,
            'city': u'montreal'
        })

        self.assertEqual(partner.street, u'5455 Avenue de Gasp\xe9')
        self.assertEqual(partner.city, u'Montr\xe9al')
        self.assertEqual(partner.state_id.name, u'Qu\xe9bec')

    def test_build_geocode_return_geocode_instance(self):
        vals = {
            'street': u'5455 Av. de Gaspé',
            'street2': u'suite 900',
            'zip': u'H2T 3B3',
            'country_id': self.canada.id,
            'city': u'montreal'
        }
        self.assertIsInstance(
            self.res_partner_pool._build_geocode(vals), GeocoderResult
        )

    def test_clean_location_data_return_cleaned_data(self):
        vals = {
            'street': u'5455 Av. de Gaspé',
            'street2': u'suite 900',
            'zip': u'H2T 3B3',
            'country_id': self.canada.id,
            'city': u'montreal'
        }
        ret = self.res_partner_pool._clean_location_data(vals)
        self.assertIsInstance(ret, dict)

        self.assertEqual(ret['street'], u'5455 Avenue de Gasp\xe9')
        self.assertEqual(ret['city'], 'Montr\xc3\xa9al')

    def test_bug_139(self):
        """https://github.com/cgstudiomap/cgstudiomap/issues/139

        Keep this test to check the bug does not come back somehow.
        """
        vals = {
            'street': u'231 front street',
            'zip': '11201',
            'city': 'New York',
            'country_id': self.usa.id
        }

        ret = self.res_partner_pool._clean_location_data(vals)
        self.assertIsInstance(ret, dict)

    def test_bug_145(self):
        """https://github.com/cgstudiomap/cgstudiomap/issues/145"""
        vals = {
            'street': u'6 Ortanca Sokak',
            'zip': '34379',
            'city': u'İstanbul',
            'country_id': self.turkey.id
        }

        ret = self.res_partner_pool._clean_location_data(vals)
        self.assertIsInstance(ret, dict)
        self.assertEqual(ret['zip'], '34379')
