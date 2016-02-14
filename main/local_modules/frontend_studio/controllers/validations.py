# -*- coding: utf-8 -*-
import logging

import phonenumbers
import simplejson
from openerp.addons.frontend_base.controllers.base import Base

from openerp import http
from openerp.exceptions import ValidationError
from openerp.http import request

_logger = logging.getLogger(__name__)

validation_base_url = '/directory/validations'


class PhoneNumberValidator(Base):
    """Represent validation of the form's phone numbers."""

    @http.route(
        '{0}/phone'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_phone(self, phone, country_id):
        """Validate the phone field.

        :param str phone: ``phone`` in :meth:`_validation_phone_numbers`.
        :param int country_id: ``country_id`` in :meth:`_validation_phone_numbers`.
        
        :return: see :meth:`_validation_phone_numbers` return
        """
        return self.validation_phone_numbers(phone, 'phone', country_id)

    @http.route(
        '{0}/fax'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_fax(self, fax, country_id):
        """Validate the fax field.

        :param str fax: ``phone`` in :meth:`_validation_fax_numbers`.
        :param int country_id: ``country_id`` in :meth:`_validation_fax_numbers`.
        
        :return: see :meth:`_validation_fax_numbers` return
        """
        return self.validation_phone_numbers(fax, 'fax', country_id)

    @http.route(
        '{0}/mobile'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_mobile(self, mobile, country_id):
        """Validate the mobile field.

        :param str mobile: ``phone`` in :meth:`validation_mobile_numbers`.
        :param int country_id: ``country_id`` in :meth:`validation_mobile_numbers`.
        
        :return: see :meth:`validation_mobile_numbers` return
        """
        return self.validation_phone_numbers(mobile, 'mobile', country_id)

    @staticmethod
    def validation_phone_numbers(phone_number, field_name, country_id):
        """Force the validation using phonenumbers of a given number

        :param str phone_number: phone number to validate.
        :param str field_name: name of the field the number is related to.
        :param int country_id: id of the country the phone number should be
            checked against.

        :return: error msg if not validate, true otherwise.
        :rtype: json
        """
        country = request.env['res.country'].browse(int(country_id))
        try:
            number = phonenumbers.parse(phone_number, country.code)
        except phonenumbers.phonenumberutil.NumberParseException as err:
            return simplejson.dumps(err[-1])

        if not phonenumbers.is_valid_number(number):
            error_msg = '\n'.join([
                'The number ({0}) "{1}" seems not valid for {2}.'.format(
                    field_name, phone_number, country.name
                ),
                'Please double check it.'
            ])
            return simplejson.dumps(error_msg)

        return simplejson.dumps('true')

class SocialNetworkValidator(Base):
    """Represent validation of the form's phone numbers."""

    @http.route(
        '{0}/twitter'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_twitter(self, twitter):
        """Validation of twitter account url.

        :param str twitter: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('twitter: %s', twitter)
        return self.validation_social_network(
            twitter, '_validate_twitter_url'
        )
    @http.route(
        '{0}/linkedin'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_linkedin(self, linkedin):
        """Validation of linkedin account url.

        :param str linkedin: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('linkedin: %s', linkedin)
        return self.validation_social_network(
            linkedin, '_validate_linkedin_url'
        )
    @http.route(
        '{0}/facebook'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_facebook(self, facebook):
        """Validation of facebook account url.

        :param str facebook: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('facebook: %s', facebook)
        return self.validation_social_network(
            facebook, '_validate_facebook_url'
        )
    @http.route(
        '{0}/youtube'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_youtube(self, youtube):
        """Validation of youtube account url.

        :param str youtube: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('youtube: %s', youtube)
        return self.validation_social_network(
            youtube, '_validate_youtube_url'
        )

    @http.route(
        '{0}/vimeo'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_vimeo(self, vimeo):
        """Validation of vimeo account url.

        :param str vimeo: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('vimeo: %s', vimeo)
        return self.validation_social_network(
            vimeo, '_validate_vimeo_url'
        )

    @http.route(
        '{0}/facebook'.format(validation_base_url),
        type='http', auth="user", methods=['POST'], website=True
    )
    def validation_facebook(self, facebook):
        """Validation of facebook account url.

        :param str facebook: url for the field
        :return: see :meth:`validation_social_network` return
        """
        _logger.debug('facebook: %s', facebook)
        return self.validation_social_network(
            facebook, '_validate_facebook_url'
        )

    @staticmethod
    def validation_social_network(url, method_name):
        """Validation of a social network url.

        :param str url: url to validate
        :param str method_name: name of the method to use to validate the url.

        :return: error msg if not validate, true otherwise.
        :rtype: json
        """

        partner_pool = request.env['res.partner']
        method = getattr(partner_pool, method_name)
        try:
            method(url)

        except ValidationError as err:
            return simplejson.dumps(err[-1])

        return simplejson.dumps('true')
