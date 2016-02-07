# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)
from openerp.addons.frontend_listing.controllers.listing import Listing

from openerp import http
from openerp.exceptions import ValidationError
from openerp.http import request

_logger = logging.getLogger(__name__)


class Studio(Base):
    """Representation of the homepage of the website."""
    partner_url = '/directory/company'

    @http.route(
        '{0}/<model("res.partner"):partner>/save'.format(partner_url),
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
            values = self.get_value_for_edit_page(partner)
            # website is part of the kwargs, but it interfers with a call of
            # website module.
            del kwargs['website']
            values.update(kwargs)
            values['error'] = err[-1]
            return request.website.render('frontend_studio.edit', values)

        values = {
            'partner': partner,
            'partner_url': '/'.join([self.partner_url, str(partner.id)]),
            'map_url': Listing.map_url,
        }
        return request.website.render('frontend_studio.save', values)

    @statsd.timed(
        'odoo.frontend.studio.view.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>'.format(partner_url),
        type='http',
        auth="public",
        website=True
    )
    def view(self, partner):
        """Render the page of a studio in view mode.

        :param object partner: record of a res.partner.
        :return: request.render
        """
        values = self.common_values(partner)
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
        type='http',
        auth="user",
        website=True
    )
    def edit(self, partner):
        """Render the page of a studio in edit mode

        :param object partner: record of a res.partner.
        :return: request.render
        """
        return request.website.render(
            'frontend_studio.edit',
            self.get_value_for_edit_page(partner)
        )

    def get_value_for_edit_page(self, partner):
        """Gather the details needed to render the edit page.

        :param object partner: record of a res.partner.

        :return: mapping of the value to render the page with.
        :rtype: dict
        """
        values = self.common_values(partner)
        values.update({
            'countries': request.env['res.country'].search([]),
            'industries': request.env['res.industry'].search([]),
        })
        return values

    def common_values(self, partner):
        """Build the values shared by different views of the module."""
        _logger.debug('main')
        _logger.debug('partner: %s', partner)
        url = '{0}/{1}'.format(self.partner_url, partner.id)
        keep = QueryURL(url)
        social_networks = (
            'twitter',
            'youtube',
            'vimeo',
            'facebook',
            'linkedin',
        )

        fields = partner.fields_get()
        state_selections = fields['state']['selection']
        _logger.debug('selections: %s', state_selections)

        return {
            'fields': fields,
            'partner': partner,
            'keep': keep,
            'state_selections': state_selections,
            'getattr': getattr,
            'social_networks': social_networks,
            'calls': ('phone', 'fax', 'mobile'),
        }
