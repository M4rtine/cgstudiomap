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

__author__ = 'foutoucour'

import logging

from openerp import models, api
from openerp.tools.translate import _
from openerp import exceptions

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add a validation of the email address of the partner."""
    _inherit = 'res.partner'

    @staticmethod
    def _url_validation(url):
        """Test a url to see if it passes our requirements

        This test use the URLValidator of django.
        Check https://docs.djangoproject.com/en/1.8/ref/validators/ for more details

        :param url: str, url to test
        :return: bool
        """
        val = URLValidator()
        try:
            val(url)
            ret = True
        except ValidationError:
            ret = False
        _logger.debug('url: {} -- valid: {}'.format(url, ret))
        return ret

    @api.constrains('website')
    def _validate_website_url(self):
        """Test against the given url against RFC requirements"""
        if not self._url_validation(self.website):
            raise exceptions.ValidationError(
                _('The given url for the website is not correct.')
            )
