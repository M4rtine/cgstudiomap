# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp import http
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)

from openerp.http import request

_logger = logging.getLogger(__name__)


class Studio(Base):
    """Representation of the homepage of the website."""
    studio_url = '/directory/company'


    @statsd.timed(
        'odoo.frontend.studio.view.time',
        tags=['frontend', 'frontend:studio']
    )
    @http.route(
        '{0}/<model("res.partner"):partner>'.format(studio_url),
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
        '{0}/<model("res.partner"):partner>/edit'.format(studio_url),
        type='http',
        auth="user",
        website=True
    )
    def edit(self, partner):
        """Render the page of a studio in edit mode

        :param object partner: record of a res.partner.
        :return: request.render
        """
        values = self.common_values(partner)
        values.update({
            'countries': request.env['res.country'].search([]),
            'industries': request.env['res.industry'].search([]),
        })
        return request.website.render('frontend_studio.edit', values)

    def common_values(self, partner):
        """Build the values shared by different views of the module."""
        _logger.debug('main')
        _logger.debug('partner: %s', partner)
        url = '{0}/{1}'.format(self.studio_url, partner.id)
        keep = QueryURL(url)
        social_networks = (
                'twitter',
                'youtube',
                'vimeo',
                'facebook',
                'linkedin',
        )

        return {
            'fields': partner.fields_get(),
            'partner': partner,
            'keep': keep,
            'getattr': getattr,
            'social_networks': social_networks,
            'calls': ('phone', 'fax', 'mobile'),
        }
