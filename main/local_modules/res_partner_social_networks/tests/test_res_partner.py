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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.exceptions import ValidationError
from openerp.tests import common


class TestResPartner(common.TransactionCase):
    """Set of two types of test:
        * test that a valid url goes through the contrains. That allows to be sure the
            reg ex is not to restricive
        * test on invalid urls to be sure the reg ex is not too loose.
    """

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    def test_valid_twitter_accounts(self):
        # random accounts from twitter
        # testing https/http and with or without www.
        accounts = [
            'https://twitter.com/WoodcoteEwan',
            'http://www.twitter.com/NHSEnglandLDN',
            'https://www.twitter.com/warwickuni',
            'http://twitter.com/alexvdm'
        ]
        self._test_valid_accounts('twitter', accounts)

    def test_invalid_twitter_accounts(self):
        accounts = [
            'http://www?twitter.com/alexvdm'
            'http://www.twitter?com/alexvdm'
            'https://twitter.com',
            'https://twitter?com',
            'http://www.twitter.eu/NHSEnglandLDN',
            'http://www.cgstudiomap.org',
        ]
        self._test_invalid_accounts('twitter', accounts)

    def test_valid_linkedin_accounts(self):
        accounts = [
            'https://www.linkedin.com/company/savoir-faire-linux',
            'https://www.linkedin.com/company/method-studios',
            'https://www.linkedin.com/company/sony-pictures-imageworks',
            'https://www.linkedin.com/company/165049',  # MPC, the url can be with the id too
            'http://www.linkedin.com/company/animation-lab',
            'https://linkedin.com/company/cgstudiomap.com',
            'https://www.linkedin.com/company/method-studios?trk=company_logo',  # Linkedin as a tracking system in the url
            ]
        self._test_valid_accounts('linkedin', accounts)

    def test_invalid_linkedin_accounts(self):
        accounts = [
            # typo in linkedin
            'https://www.likedin.com/company/savoir-faire-linux',
            # no company folder
            'https://www.linkedin.com/method-studios',
            'https://www.linkedin.com',
            'https://linkedin?com/company/cgstudiomap.com',
            # no company folder
            'https://www.linkedin.com/165049',  # MPC, the url can be with the id too
            'http://www.cgstudiomap.org',
        ]
        self._test_invalid_accounts('linkedin', accounts)

    def test_valid_facebook_accounts(self):
        accounts = [
            'https://www.facebook.com/Moving.Picture.Company?fref=ts',
            'http://www.facebook.com/Moving.Picture.Company?fref=ts',
            'https://facebook.com/DisneyPixar',
            'https://www.facebook.com/CGMeetup',
            ]
        self._test_valid_accounts('facebook', accounts)

    def test_invalid_facebook_accounts(self):
        accounts = [
            'https://www.fabook.com/Moving.Picture.Company?fref=ts',
            'http://www.facebook.eu/Moving.Picture.Company',
            'http://www5facebook.com/Moving.Picture.Company',
            'http://www.facebook3com/Moving.Picture.Company',
            'https://facebook.com',
            'http://www.cgstudiomap.org',
        ]
        self._test_invalid_accounts('facebook', accounts)

    def test_valid_wikipedia_accounts(self):
        accounts = [
            'https://en.wikipedia.org/wiki/Pixar',
            'https://www.wikipedia.org/wiki/Pixar',
            'https://wikipedia.org/wiki/Pixar',
            'https://en.wikipedia.org/wiki/Moving_Picture_Company',
            'https://fr.wikipedia.org/wiki/Pixar_Animation_Studios',
        ]
        self._test_valid_accounts('wikipedia', accounts)

    def test_invalid_wikipedia_accounts(self):
        accounts = [
            # .com instead of .org
            'https://en.wikipedia.com/wiki/Pixar',
            # no wiki
            'https://en.wikipedia.org/Pixar',
            # typo in wikipedia
            'https://fr.wiipedia.org/wiki/Pixar_Animation_Studios',
            'http://www.cgstudiomap.org',
            ]
        self._test_invalid_accounts('wikipedia', accounts)

    def _test_valid_accounts(self, field_name, accounts):
        partner = self.partner_pool.create({'name': 't_name'})
        for account in accounts:
            partner.write({field_name: account})
            self.assertEqual(getattr(partner, field_name), account)

    def _test_invalid_accounts(self, field_name, accounts):
        partner = self.partner_pool.create({'name': 't_name'})
        for account in accounts:
            with self.assertRaises(ValidationError):
                partner.write({field_name: account})
