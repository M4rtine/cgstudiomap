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
import logging
import re

from openerp import models, api, fields
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add Social Networks fields."""
    _inherit = 'res.partner'

    twitter = fields.Char('Twitter')
    youtube = fields.Char('Youtube')
    vimeo = fields.Char('Vimeo')

    linkedin = fields.Char('Linkedin')
    facebook = fields.Char('Facebook')
    wikipedia = fields.Char('Wikipedia')

    # art_of_vfx = fields.Char('Art of VFX')

    @api.model
    def _validate_social_network_url(self, url, regex, err_msg):
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
            'twitter', 'youtube', 'vimeo', 'facebook', 'linkedin',
            # 'wikipedia', 'art_of_fx',
        ])
        return fields

    @api.one
    @api.constrains('twitter')
    def _validate_twitter_url_constrains(self):
        """Add a constrains to the twitter field."""
        self._validate_twitter_url(self.twitter)

    def _validate_twitter_url(self, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = self.__strip_value(value)
        regex = r'https?://(www\.)?twitter\.com/\w+'
        if url:
            self._url_validation(url)
            if not re.match(regex, url):
                err_msg = _(
                    (
                        '"{}" seems not to be an twitter account.'
                        '\nA twitter account should be something '
                        'like https://www.twitter.com/cgstudiomap'.format(url)
                    )
                )
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('linkedin')
    def _validate_linkedin_url_constrains(self):
        """Add a constrains to the linkedin field."""
        self._validate_linkedin_url(self.linkedin)

    def _validate_linkedin_url(self, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = self.__strip_value(value)
        # Linkedin got its page tracking system embed in the url
        # then the url can be followed by ?trk...
        regex = r'https?://(www\.)?linkedin\.com/company/[\w-]+'
        if url:
            self._url_validation(url)
            if not re.match(regex, url):
                err_msg = _(
                    (
                        '"{}" seems not to be an linkedin account.'
                        '\nA linkedin account should be something '
                        'like https://www.linkedin.com/'
                        'company/cgstudiomap.com'.format(url)
                    )
                )
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('facebook')
    def _validate_facebook_url(self):
        """Add a constrains to the facebook field."""
        self._validate_facebook_url(self.facebook)

    def _validate_facebook_url(self, value):
        """Test against the given url against RFC requirements.

        :param str value: url to check. Can be False.
        """
        url = self.__strip_value(value)
        # Facebook got its page tracking system embed in the url
        # then the url can be followed by ?fref...
        regex = r'https?://(www\.)?facebook\.com/[\w-]+'
        if url:
            self._url_validation(url)
            if not re.match(regex, url):
                err_msg = _(
                    (
                        '"{}" seems not to be an facebook account.'
                        '\nA facebook account should be something '
                        'like https://www.facebook.com/'
                    )
                )
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('youtube')
    def _validate_youtube_url_constrains(self):
        """Add a constrains to the youtube field."""
        self._validate_youtube_url(self.youtube)

    def _validate_youtube_url(self, value):
        """Check the youtube url.

        :param str value: url to check. Can be False.
        """
        url = self.__strip_value(value)
        regex = r'https?://(www\.)?youtube\.com/user/'
        if url:
            self._url_validation(url)
            if not re.match(regex, url):
                err_msg = _(
                    (
                        '"{}" seems not to be an youtube account.'
                        '\nA youtube account should start by '
                        'https://www.youtube.com'.format(url)
                    )
                )
                raise ValidationError(err_msg)

    @api.one
    @api.constrains('vimeo')
    def _validate_vimeo_url_constrains(self):
        """Add a constrains to the vimeo field."""
        self._validate_vimeo_url(self.vimeo)

    def _validate_vimeo_url(self, value):
        """Check the vimeo url.

        :param str value: url to check. Can be False.
        """
        url = self.__strip_value(value)
        regex = r'https?://(www\.)?vimeo\.com'
        if url:
            self._url_validation(url)
            if not re.match(regex, url):
                err_msg = _(
                    (
                        '"{}" seems not to be an vimeo account.'
                        '\nA vimeo account should start by '
                        'https://www.vimeo.com'.format(url)
                    )
                )
                raise ValidationError(err_msg)

    @staticmethod
    def __strip_value(value):
        """strip if the value is a string.

        :param object value: value to attempt to strip.
        :return: striped value.
        """
        if isinstance(value, basestring):
            return value.strip()

        return value
