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
from openerp.tests import common


class TestTagUrlLinkDetails(common.TransactionCase):
    """Test suite of the static method of tag_url_link_details."""

    def setUp(self):
        super(TestTagUrlLinkDetails, self).setUp()
        self.industry_pool = self.env['res.industry']

    def test_whenListingIsProvided_thenUrlWithDirectoryListIsReturned(self):
        self.assertEqual(
            (
                '<a itemprop="name" href="/directory/list?company_status=open'
                '&search=vfx"><span class="label label-info">vfx</span></a>'
            ),
            self.industry_pool.tag_url_link_details('vfx', 'open', True)
        )

    def test_whenListingIsFalse_thenNoUrlTokenIsAdded(self):
        self.assertEqual(
            (
                '<a itemprop="name" href="?company_status=open&search=vfx">'
                '<span class="label label-info">vfx</span></a>'
            ),
            self.industry_pool.tag_url_link_details('vfx', 'open', False)
        )
