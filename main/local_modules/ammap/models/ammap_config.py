# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap.org <cgstudiomap@gmail.com>
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
__author__ = 'foutoucour'

from openerp import fields, models


class AmMapConfig(models.Model):
    _name = 'ammap.config'
    _description = 'Configs that drive an AmMap (http://www.amcharts.com)'

    name = fields.Char('Map Name', size=256, required=True)
    description = fields.Text('Description')
    color = fields.Char(
        'Color',
        default='#FFFFFF',
        size=7,
        help='Color of the areas.'
    )

    color_solid = fields.Char(
        'High Values Color',
        default='#FF0000',
        size=7,
        help=('Color of area with highest value. '
              'Colors for areas with values less then highest will be colored '
              'with intermediate colors between color and colorSolid.')
    )

    unlisted_areas_color = fields.Char(
        string='Unlisted Areas Color',
        default='#DDDDDD',
        size=7,
        help=('Color of all areas which are in the map svg file, '
              'but not listed as areas in DataSet.')
    )
