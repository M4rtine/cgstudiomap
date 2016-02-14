# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)
from openerp.addons.frontend_listing.controllers.listing import Listing

from openerp import http
from openerp.exceptions import ValidationError
from openerp.http import request

_logger = logging.getLogger(__name__)

partner_url = '/directory/company'


class Studio(Base):
    """Representation of the homepage of the website."""

    @statsd.timed(
        'odoo.frontend.studio.view.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>'.format(partner_url),
        type='http', auth="public", website=True
    )
    def view(self, partner):
        """Render the page of a studio in view mode.

        :param object partner: record of a res.partner.
        :return: request.render
        """
        values = self.common_values()
        values['partner'] = partner
        partner_values = self.get_partner_values()
        values['social_networks'] = partner_values['social_networks'].keys()
        # values['calls'] = partner_values['calls'].keys()

        marquee_plus_social_network = any(
            not getattr(partner, field) for field in values['social_networks']
        )
        _logger.debug(
            'marqueePlusSocialNetwork: %s', marquee_plus_social_network
        )
        values.update({
            'marqueePlusSocialNetwork': marquee_plus_social_network,
            'partners': partner.get_random_studios_from_same_location(6),
            'filter_domain': partner.country_id.name,
        })
        return request.website.render('frontend_studio.view', values)

    @statsd.timed(
        'odoo.frontend.studio.edit.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>/edit'.format(partner_url),
        type='http', methods=['GET'], auth="user", website=True
    )
    def edit(self, partner):
        """Render the page of a studio in edit mode

        :param object partner: record of a res.partner.
        :return: request.render
        """
        return request.website.render(
            'frontend_studio.edit', self.get_values_for_edition_page(partner)
        )

    @statsd.timed(
        'odoo.frontend.studio.create.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/create'.format(partner_url),
        type='http', methods=['GET'], auth="user", website=True
    )
    def create(self):
        """Render the page to create a new res partner in the database."""
        values = self.get_values_for_edition_page()
        values['create'] = True
        return request.website.render('frontend_studio.edit', values)

    @staticmethod
    def get_partner_values():
        """Return the set of data to build edit/create view.

        :return: dict
        """
        return {
            'id': 0,
            'write_date': '',
            'image_url': '',
            'name': '',
            'website': '',
            'email': '',
            'state': '',
            'street': '',
            'street2': '',
            'city': '',
            'zip': '',
            'industry_ids': [],
            'country_id': 0,
            # social network urls
            'social_networks': {
                'twitter': '',
                'youtube': '',
                'vimeo': '',
                'linkedin': '',
                'facebook': '',
            },
            # phone numbers
            'calls': {
                'phone': '',
                'mobile': '',
                'fax': '',
            }

        }

    def build_values_from_partner(self, partner):
        """Fill up the partner_value from a partner record.

        :param object partner: partner to fill the values with.
        :return: dict
        """
        websites = request.env['website']
        partner_values = self.get_partner_values()
        partner_values['id'] = partner.id
        partner_values['write_date'] = partner.write_date
        partner_values['name'] = partner.name
        partner_values['image_url'] = websites.image_url(
            partner, 'image_medium', size='256x256'
        )
        partner_values['website'] = partner.website
        partner_values['email'] = partner.email
        partner_values['state'] = partner.state
        partner_values['street'] = partner.street
        partner_values['street2'] = partner.street2
        partner_values['city'] = partner.city
        partner_values['zip'] = partner.name
        partner_values['industry_ids'] = partner.industry_ids
        partner_values['country_id'] = partner.country_id.id
        partner_values['calls']['phone'] = partner.phone
        partner_values['calls']['mobile'] = partner.mobile
        partner_values['calls']['fax'] = partner.fax
        partner_values['social_networks']['linkedin'] = partner.linkedin
        partner_values['social_networks']['vimeo'] = partner.vimeo
        partner_values['social_networks']['youtube'] = partner.youtube
        partner_values['social_networks']['twitter'] = partner.twitter
        partner_values['social_networks']['facebook'] = partner.facebook

        return partner_values

    def get_values_for_edition_page(self, partner=None):
        """Gather the details needed to render page that edit or create a
        partner. If a partner is given, the value are built from it.

        :param object partner: record of a res.partner. Default: None.

        :return: mapping of the value to render the page with.
        :rtype: dict
        """
        values = self.common_values()
        if partner:
            partner_values = self.build_values_from_partner(partner)
        else:
            partner_values = self.get_partner_values()

        values['partner'] = partner_values

        values.update({
            'countries': request.env['res.country'].search([]),
            'industries': request.env['res.industry'].search([]),
            'partner_pool': request.env['res.partner'],
            'getattr': getattr,
        })
        return values

    @staticmethod
    def common_values():
        """Build the values shared by different views of the module.

        :return: mapping for values for all the views.
        """
        _logger.debug('main')
        keep = QueryURL()

        partner = request.env['res.partner'].browse(1)
        fields = partner.fields_get()
        state_selections = fields['state']['selection']
        _logger.debug('selections: %s', state_selections)

        return {
            'fields': fields,
            'partner': partner,
            'keep': keep,
            'state_selections': state_selections,
            'getattr': getattr,
        }


class StudioPost(Studio):
    """Control of POST methods for the studio page."""
    @statsd.timed(
        'odoo.frontend.studio.save.time',
        tags=['frontend', 'frontend:studio', 'POST']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>/edit'.format(partner_url),
        type='http', auth="public", methods=['POST'], website=True
    )
    def save(self, partner, **kwargs):
        """Save new data of the partner then return the request to render
        the page following the edition.

        :param object partner: record of a res.partner.
        :param dict kwargs: list of fields to update.
        :return: request.render
        """
        _logger.debug('save')
        _logger.debug('kwargs: %s', kwargs)

        try:
            partner.write_from_post_request(kwargs)
        except ValidationError as err:

            # if a validation error has been raised,
            # we go back to the edit page, so the user can fix the error.
            values = self.get_values_for_edition_page(partner)
            # website is part of the kwargs, but it interfers with a call of
            # website module.
            del kwargs['website']
            values.update(kwargs)
            values['error'] = err[-1]
            return request.website.render('frontend_studio.edit', values)

        values = {
            'partner': partner,
            'partner_url': '/'.join([partner_url, str(partner.id)]),
            'map_url': Listing.map_url,
        }
        return request.website.render('frontend_studio.thank_you', values)


    @statsd.timed(
        'odoo.frontend.studio.save_new.time',
        tags=['frontend', 'frontend:studio', 'POST']
    )
    @http.route(
        '{0}/create'.format(partner_url),
        type='http', auth="public", methods=['POST'], website=True
    )
    def save_new(self, **kwargs):
        """Try to save a new partner from the given data.

        :param dict kwargs: list of fields to update.
        :return: request.render
        """
        _logger.debug('save_new')
        _logger.debug('kwargs: %s', kwargs)
        partner_pool = request.env['res.partner']
        try:
            partner = partner_pool.create_from_post_request(kwargs)
        except ValidationError as err:

            # if a validation error has been raised,
            # we go back to the edit page, so the user can fix the error.
            values = self.get_values_for_edition_page()
            # website is part of the kwargs, but it interfers with a call of
            # website module.
            del kwargs['website']
            values.update(kwargs)
            values['error'] = err[-1]
            return request.website.render('frontend_studio.edit', values)

        values = {
            'partner': partner,
            'partner_url': '/'.join([partner_url, str(partner.id)]),
            'map_url': Listing.map_url,
        }
        return request.website.render('frontend_studio.thank_you', values)
