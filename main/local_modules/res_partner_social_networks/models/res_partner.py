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
__author__ = 'foutoucour'

from openerp import models, api, fields
from openerp import exceptions


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'

    twitter = fields.Char('Twitter')
    linkedin = fields.Char('Linkedin')
    facebook = fields.Char('Facebook')
    wikipedia = fields.Char('Wikipedia')
    art_of_fx = fields.Char('Art of FX')

    @api.constrains('twitter')
    def _validate_twitter_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.twitter):
            raise exceptions.ValidationError(
                _('The given url for the twitter is not correct.')
            )

    @api.constrains('linkedin')
    def _validate_linkedin_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.linkedin):
            raise exceptions.ValidationError(
                _('The given url for the linkedin is not correct.')
            )

    @api.constrains('facebook')
    def _validate_facebook_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.facebook):
            raise exceptions.ValidationError(
                _('The given url for the facebook is not correct.')
            )

    @api.constrains('wikipedia')
    def _validate_wikipedia_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.wikipedia):
            raise exceptions.ValidationError(
                _('The given url for the wikipedia is not correct.')
            )

    @api.constrains('art_of_fx')
    def _validate_art_of_fx_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.art_of_fx):
            raise exceptions.ValidationError(
                _('The given url for the art_of_fx is not correct.')
            )
