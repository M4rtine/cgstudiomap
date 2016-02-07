# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
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
import pprint
import logging
import socket
from urllib2 import urlopen, URLError, HTTPError

from openerp import models, api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError, except_orm

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as DjangoValidationError

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add a validation of the email address of the partner."""
    _inherit = 'res.partner'
    _default_timeout = 20  # timeout in seconds

    _url_fields_valid_status = 'valid'

    @property
    def _url_fields(self):
        """Returns the name of fields used in `_check_url_fields` method

        A property is used here, instead of a simple list to be able to
        add more fields in other definition of the model using super()
        """
        return ['website']

    @api.multi
    def action_check_url_fields(self):
        """Action to inform the user about the statuses of
        fields registered in `_url_fields`.

        It actually raises a except_orm. It is dirty but
        it was quicker than creata a wizard.
        """
        statuses = self._check_url_fields()
        msg = ''
        for key, value in statuses.iteritems():
            msg = '\n'.join([msg, '{}: {}'.format(key, value)])

        raise except_orm(
            _('information'),
            msg
        )

    @api.model
    def _check_url_fields(self):
        """Check the field registered to self._url_fields against our test.

        return: dict, describe the status of all the fields
            status can be: valid if all test went well, or the error from
            the tests
        """
        _logger.debug('_check_url_fields')
        statuses = {}

        for field_name in self._url_fields:
            msg = ''
            url = getattr(self, field_name)
            _logger.debug('url: {}'.format(url))

            if url:
                try:
                    self._url_validation(url)
                except ValidationError as e:
                    _logger.debug('_url_validation error: {}'.format(e))
                    msg = str(e)

                if not msg:
                    try:
                        self._ping_url(url)
                        msg = self._url_fields_valid_status
                    except ValidationError as e:
                        msg = str(e)

                statuses[field_name] = msg

        _logger.debug('statuses: {}'.format(pprint.pformat(statuses)))
        return statuses

    @classmethod
    def _ping_url(cls, url):
        """Use a request to the url to check the server answer"""
        socket.setdefaulttimeout(cls._default_timeout)
        err_msg = ''

        try:
            urlopen(url)
        except HTTPError as e:
            err_msg = _(
                'The server couldn\'t fulfill the request. Reason: {}'.format(
                    str(e.code)
                )
            )
        except URLError as e:
            err_msg = _('We failed to reach a server. Reason: {}'.format(
                str(e.reason)))

        if err_msg:
            raise ValidationError(err_msg)

        return True

    @classmethod
    def _url_validation(cls, url):
        """Test a url to see if it passes our requirements

        The test use the URLValidator of django.
        Check https://docs.djangoproject.com/en/1.8/ref/validators/ for more
        details

        :param url: str, url to test
        :return: bool
        """
        val = URLValidator()
        _logger.debug('url: {}'.format(url))

        if not url:
            return True

        try:
            val(url)

        # We can't actually read the error message without to init a django
        # instance
        # Trying to read the error will raise:
        # ```
        # django.core.exceptions.ImproperlyConfigured: Requested setting
        # USE_I18N, but settings are not configured. You must either define
        # the environment variable DJANGO_SETTINGS_MODULE or call
        # settings.configure() before accessing settings.
        # ```
        except DjangoValidationError:
            err_msg = _(
                'The given url ("{}") is not correct.'
                '\nDoes it starts with "http://"?'.format(url)
            )
            raise ValidationError(err_msg)

        return True
