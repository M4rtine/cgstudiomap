# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
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
import re
import logging
from openerp import models, api, fields
from openerp.tools.translate import _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'

    twitter = fields.Char('Twitter')
    linkedin = fields.Char('Linkedin')
    facebook = fields.Char('Facebook')
    wikipedia = fields.Char('Wikipedia')
    # art_of_vfx = fields.Char('Art of VFX')

    @api.model
    def _validate_social_network_url(self, url, regex):
        _logger.debug('_validate_social_network_url')
        _logger.debug('url: {}'.format(url))
        _logger.debug('regex: {}'.format(regex))
        self._url_validation(url)
        if not re.match(regex, url):
            err_msg = _(
                'The given url ("{}") seems not to be an account.'.format(url)
            )
            raise ValidationError(err_msg)

    @property
    def _url_fields(self):
        """Add social networks fields to inital list of url fields."""
        fields = super(ResPartner, self)._url_fields
        fields.extend([
            'twitter',
            'facebook',
            'linkedin',
            'wikipedia',
            # 'art_of_fx',
        ])
        return fields

    @api.one
    @api.constrains('twitter')
    def _validate_twitter_url(self):
        """Test against the given url against RFC requirements"""
        if self.twitter:
            self._validate_social_network_url(
                self.twitter, r'^https?://(www\.)?twitter\.com/\w+$'
            )

    @api.one
    @api.constrains('linkedin')
    def _validate_linkedin_url(self):
        """Test against the given url against RFC requirements"""
        if self.linkedin:
            self._validate_social_network_url(
                self.linkedin,
                # Linkedin got its page tracking system embed in the url
                # then the url can be followed by ?trk...
                r'https?://(www\.)?linkedin\.com/company/[\w-]+'
            )

    @api.one
    @api.constrains('facebook')
    def _validate_facebook_url(self):
        """Test against the given url against RFC requirements"""
        if self.facebook:
            self._validate_social_network_url(
                self.facebook,
                # Facebook got its page tracking system embed in the url
                # then the url can be followed by ?fref...
                r'https?://(www\.)?facebook\.com/[\w-]+'
            )

    @api.one
    @api.constrains('wikipedia')
    def _validate_wikipedia_url(self):
        """Test against the given url against RFC requirements"""
        if self.wikipedia:
            self._validate_social_network_url(
                self.wikipedia,
                # Facebook got its page tracking system embed in the url
                # then the url can be followed by ?fref...
                r'https?://\w*\.?wikipedia.org/wiki/[\w-]+'
            )
