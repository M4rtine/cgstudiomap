﻿# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2014 CodUP (<http://codup.com>).
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
    'name': 'Cron',
    'version': '1.0',
    'category': 'Extra Tools',
    'summary': 'WSGI cron control',
    'description': """
WSGI cron control
-----------------
User interface for manually start cron.
Usefull if you use WSGI deployment.
    """,
    'author': 'CodUP',
    'website': 'http://codup.com',
    'images': ['static/description/icon.png'],
    'depends': [],
    'demo': [],
    'data': [
        'wizard/start_cron_view.xml',
        'cron_view.xml',
    ],
    'installable': True,
}
