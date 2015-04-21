# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
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
from openerp.exceptions import ValidationError

__author__ = 'foutoucour'

import logging
from openerp import models, api
from pygeocoder import Geocoder

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'

    @api.constrains('street', 'city', 'zip')
    def _validate_location(self):
        """Check if a location matches a geocode."""
        _logger.debug('_validate_location')
        geocode = self._build_geocode()
        _logger.debug(
            'geocode.valid_address: {}'.format(geocode.valid_address)
        )
        if not geocode.valid_address:
            error_msg = '\n'.join([
                'The given address ({}) cannot be located.'.format(geocode),
                'Please double check it.'
            ])
            _logger.error(error_msg)
            raise ValidationError(error_msg)

    @api.model
    def _build_geocode(self, vals=None):
        """Build the geocode from the data from the user.

        The Geocode is built from the street, city, zip, state and country
        details from the record.

        The Geocode is built from the the data in vals completed by the data
        in the record itself.

        :param vals: set of values for the record. Default: {}
        :return: Geocoder.geocode instance
        """
        _logger.debug('_build_geocode')
        if vals is None:
            vals = {}
        _logger.debug('vals: {}'.format(vals))

        location = vals.get('street', self.street)
        street2 = vals.get('street2', self.street2)

        if street2:
            location = ' '.join([location, street2])

        location = ' '.join([
            location,
            vals.get('city', self.city),
            vals.get('zip', self.zip)
        ])
        _logger.debug(
            'location (street, street2, city, zip): {}'.format(location)
        )
        state_id = vals.get('state_id')
        _logger.debug('vals.get("state_id"): {}'.format(state_id))
        if state_id:
            location = ' '.join([
                location,
                self.env['res.country.state'].browse(state_id).name
            ])

        elif self.state_id:
            location = ' '.join([location, self.state_id.name])
        _logger.debug('location (state): {}'.format(location))

        country_id = vals.get('country_id')
        _logger.debug('vals.get("country_id"): {}'.format(country_id))
        if country_id:
            location = ' '.join([
                location,
                self.env['res.country'].browse(country_id).name
            ])
        elif self.country_id:
            location = ' '.join([location, self.country_id.name])
        _logger.debug('location (country): {}'.format(location))

        geocode = Geocoder.geocode(location)
        _logger.debug('geocode: {}'.format(geocode))
        return geocode

    @api.model
    def _clean_location_data(self, vals):
        """Build a geocode from the details of the partner to then inject
        into the records the cleaned data caught from google.

        :return: dict with the values for the orm.
        """
        _logger.debug('_clean_location_data')
        # First a geocode is build from the data of the record.
        # the build is done with the data from vals completed by
        # the data in the record (in case of write ie)
        location = self._build_geocode(vals)
        # then the cleaned data are reinjected to the values the
        # record will be created/written with.
        street_number = location.street_number
        if not street_number is None:
            vals['street'] = ' '.join(
                [location.street_number, location.route]
            )
        else:
            vals['street'] = location.route

        vals['zip'] = location.postal_code
        vals['city'] = location.city

        # Getting the country of the location
        # Normally all the countries are registered to odoo by default.
        country_pool = self.env['res.country']
        country = country_pool.search(
            [('code', '=', location.country__short_name)]
        )

        if country:
            vals['country_id'] = country.id

        # the case of state is a bit more tricky.
        # all the countries don't have state.
        if location.state:
            # Even tho, all the states are not registered by default to odoo.
            # We have first to check if there is a record for the given state
            # code (state__short__name)
            state_pool = self.env['res.country.state']
            state = state_pool.search([
                ('code', '=', location.state__short_name),
                ('country_id', '=', country.id)
            ])
            # Checking the search returned something
            # otherwise that means it needs to be created.
            if not state:
                state = state_pool.create({
                    'country_id': country.id,
                    'name': location.state__long_name,
                    'code': location.state__short_name,
                })

            vals['state_id'] = state.id

        return vals

    @api.model
    def create(self, vals):
        _logger.debug('res_partner_location_validation.create')
        return super(ResPartner, self).create(self._clean_location_data(vals))

    @api.multi
    def write(self, vals):
        return super(ResPartner, self).write(self._clean_location_data(vals))
