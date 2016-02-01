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
    """Test suites for social network fields added in res.partner."""

    def setUp(self):
        """Overcharge the default setUp to expose the partner_pool."""
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']

    def test_twitter_value(self):
        """Check if we can add value to the twitter field."""
        url = 'https://twitter.com/cgstudiomap'
        partner = self.partner_pool.create({'name': 'tname', 'twitter': url})
        self.assertEqual(partner.twitter, url)

    def test_youtube_value(self):
        """Check if we can add value to the youtube field."""
        url = 'https://www.youtube.com/user/mpcvfx'
        partner = self.partner_pool.create({'name': 'tname', 'youtube': url})
        self.assertEqual(partner.youtube, url)

    def test_vimeo_value(self):
        """Check if we can add value to the vimeo field."""
        url = 'https://vimeo.com/mpcvfx'
        partner = self.partner_pool.create({'name': 'tname', 'vimeo': url})
        self.assertEqual(partner.vimeo, url)

    def test_linkedin_value(self):
        """Check if we can add value to the linkedin field."""
        url = 'https://www.linkedin.com/company/cgstudiomap-com'
        partner = self.partner_pool.create({'name': 'tname', 'linkedin': url})
        self.assertEqual(partner.linkedin, url)

    def test_facebook_value(self):
        """Check if we can add value to the facebook field."""
        url = 'https://www.facebook.com/Moving.Picture.Company/'
        partner = self.partner_pool.create({'name': 'tname', 'facebook': url})
        self.assertEqual(partner.facebook, url)

    def test_wikipedia_value(self):
        """Check if we can add value to the wikipedia field."""
        url = 'https://en.wikipedia.org/wiki/Sony_Pictures_Imageworks'
        partner = self.partner_pool.create({'name': 'tname', 'wikipedia': url})
        self.assertEqual(partner.wikipedia, url)
