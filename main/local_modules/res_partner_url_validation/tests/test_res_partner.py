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
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
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
        self.valid_urls = [
            'http://www.cgstudiomap.org',
            'https://www.cgstudiomap.org',
            'https://www.test.co.uk',
            'http://api.cgstudiomap.org',
        ]
        self.invalid_urls = [
            'http//www.cgstudiomap.org',
            'http:/www.cgstudiomap.org',
            'http:www.cgstudiomap.org',
            'cgstudiomap',
        ]

    def test_url_validation_method_valid_urls(self):
        for url in self.valid_urls:
            self.assertTrue(self.partner_pool._url_validation(url))

    def test_url_validation_method_invalid_urls(self):
        for url in self.invalid_urls:
            self.assertFalse(self.partner_pool._url_validation(url))

    def test_validate_during_create_valid_website_url(self):
        for url in self.valid_urls:
            partner = self.partner_pool.create(
                {'name': 't_name', 'website': url}
            )
            self.assertEqual(partner.website, url)

    def test_validate_website_url_reformat(self):
        """Odoo format url to add the http:// before at creation if needed.

        Even if it can be considered as out of scope of the these module, but
        I want to be sure the url pass the validation after the formating.
        """
        url = 'cgstudiomap.org'
        partner = self.partner_pool.create(
            {'name': 't_name', 'website': url}
        )
        self.assertEqual(partner.website, ''.join(['http://', url]))

    def test_validate_during_create_invalid_website_url(self):
        for url in self.invalid_urls:
            self.assertRaises(
                ValidationError,
                self.partner_pool.create,
                {'name': 't_name', 'website': url}
            )

    def test_validate_during_write_valid_website_url(self):
        partner = self.partner_pool.create(
            {'name': 't_name'}
        )
        for url in self.valid_urls:
            partner.write({'website': url})
            self.assertEqual(partner.website, url)

    def test_validate_during_write_invalid_website_url(self):
        partner = self.partner_pool.create({'name': 't_name'})
        for url in self.invalid_urls:
            self.assertRaises(
                ValidationError,
                partner.write,
                {'website': url}
            )

