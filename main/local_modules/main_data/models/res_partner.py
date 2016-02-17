# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
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

from openerp.addons.base_geoengine import geo_model
from openerp.addons.base_geolocalize.models.res_partner import (
    geo_find, geo_query_address
)

from openerp import api, fields

_logger = logging.getLogger(__name__)
__codec__ = 'utf-8'


class ResPartner(geo_model.GeoModel):
    _inherit = 'res.partner'

    # set on to avoid that some function are called during tests.
    __dryRun__ = False

    @api.model
    def add_geo_localization_details(self, vals):
        """Add geo localization details to the current partner."""
        # skip during dry runs.
        if self.__dryRun__:
            return vals

        street = vals.get('street')
        zip = vals.get('zip')
        city = vals.get('city')
        country_id = vals.get('country_id')

        if street and zip and city and country_id:
            result = geo_find(
                geo_query_address(
                    street=vals.get('street', '').encode(__codec__),
                    zip=vals.get('zip', '').encode(__codec__),
                    city=vals.get('city', '').encode(__codec__),
                    country=self.env['res.country'].browse(
                        vals.get('country_id')).name.encode(__codec__),
                )
            )
            if result:
                vals['partner_latitude'] = result[0]
                vals['partner_longitude'] = result[1]
                vals['date_localization'] = fields.Date.context_today(self)
        else:
            _logger.debug('Missing details. Skipping.')
        return vals

    @api.model
    def create(self, vals):
        return super(ResPartner, self).create(
            self.add_geo_localization_details(vals))

    @api.multi
    def write(self, vals):
        return super(ResPartner, self).write(
            self.add_geo_localization_details(vals))

    def _states(self):
        return [('open', 'Open'), ('closed', 'Closed for business')]

    @api.multi
    def action_close_company(self):
        """Change the state of the companies to set them as closed."""
        self.state = 'closed'

    @api.multi
    def action_open_company(self):
        """Change the state of the companies to set them as opened."""
        self.state = 'open'

    country_id = fields.Many2one(required=True)
    website = fields.Char(required=True)
    street = fields.Char(required=True)
    city = fields.Char(required=True)

    state = fields.Selection(
        selection='_states',
        default='open',
        string='Status',
        readonly=True,
        copy=False,
        help='Current state of the company.',
        select=True
    )
