# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
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
    'name': 'Datadog',
    'version': 'beta',
    'author': 'cgstudiomap',
    'maintainer': 'cgstudiomap',
    'license': 'AGPL-3',
    'category': 'Main',
    'summary': 'Gather module that add tracker to datadog',
    'description': """
Datadog
=======
This module contains the dependencies to install all datadog related modules.

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

""",
    # Keep main as dependency so this module is loaded after all the other
    'depends': [
        # odoo
        'main',
        # datadog modules
        'datadog_res_partner',
    ],
    'data': [],
    'installable': True,
    'application': True,
}
