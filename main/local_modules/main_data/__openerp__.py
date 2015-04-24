# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
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
    'name': 'Main Data Module',
    'version': '0.1',
    'author': 'Jordi Riera',
    'maintainer': 'Jordi Riera',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Main Module, that install data, views etc.',
    'description': """
Main Data Module
================
This module contains the data, views, models.

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

""",
    'depends': [
        'crm',
        'website',
        'website_crm',
        'base_geolocalize',
        'geoengine_partner',
        'base_geoengine',
        'geoengine_base_geolocalize',
        'auth_signup',
        'web_tree_image',
        'web_widget_text_markdown',
    ],
    'data': [
        'data/company_details.xml',
        'data/res_groups_data.xml',
        'data/res_users_data.xml',
        'security/ir_rules.xml',
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/geo_partner_view.xml',
        'templates/web_layout.xml',
    ],
    'installable': True,
}
