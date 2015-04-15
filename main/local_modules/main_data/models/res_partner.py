# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
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
__author__ = 'foutoucour'

from openerp import api, fields
from openerp.addons.base_geolocalize.models.res_partner import (
    geo_find, geo_query_address
)

from openerp.addons.base_geoengine import geo_model

class ResPartner(geo_model.GeoModel):
    _inherit = 'res.partner'

    @api.model
    def add_geo_localization_details(self, vals):
        result = geo_find(
            geo_query_address(
                street=vals.get('street'),
                zip=vals.get('zip'),
                city=vals.get('city'),
                # state=vals.get('state'),
                country=self.env['res.country'].browse(vals.get('country_id')).name,
            )
        )
        if result:
            vals['partner_latitude'] = result[0]
            vals['partner_longitude'] = result[1]
            vals['date_localization'] = fields.Date.context_today(self)
        return vals

    @api.model
    def create(self, vals):
        return super(ResPartner, self).create(self.add_geo_localization_details(vals))

    @api.multi
    def write(self, vals):
        return super(ResPartner, self).write(self.add_geo_localization_details(vals))

    country_id = fields.Many2one(required=True)
    website = fields.Char(required=True)
    street = fields.Char(required=True)
    city = fields.Char(required=True)
    zip = fields.Char(required=True)
