# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
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

{
    'name': 'Website Blog Group Published Only',
    'version': '1.0',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'website': 'http://www.cgstudiomap.org',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': ('Create a new group to allow portal member to be also blog '
                'poster'),
    'depends': [
        'website_blog',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'website_blog_data.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
