# -*- coding: utf-8 -*-
import logging

from datadog import statsd
from openerp.addons.web import http
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)

from openerp.http import request

_logger = logging.getLogger(__name__)


class Studio(Base):
    """Representation of the homepage of the website."""
    studio_url = '/directory/company'


    @statsd.timed('odoo.frontend.studio.time',
                  tags=['frontend', 'frontend:studio'])
    @http.route('{0}/<model("res.partner"):partner>'.format(studio_url),
                type='http', auth="public", website=True)
    def main(self, partner, mode='view'):
        """Dispatch between the different modes of the page.

        :param object partner: record of a res.partner.
        :param str mode: mode the page is viewed. Default: view.
            Can be view, edit, create.

        :return: request.render
        """
        _logger.debug('main')
        _logger.debug('partner: %s', partner)
        _logger.debug('mode: %s', mode)
        url = '{0}/{1}'.format(self.studio_url, partner.id)
        keep = QueryURL(url, mode=mode)
        social_networks = (
                'twitter',
                'youtube',
                'vimeo',
                'facebook',
                'linkedin',
        )

        values = {
            'fields': partner.fields_get(),
            'partner': partner,
            'mode': mode,
            'keep': keep,
            'getattr': getattr,
            'social_networks': social_networks,
            'calls': ('phone', 'fax', 'mobile'),
        }
        if mode == 'view':
            values = self.get_view_mode_specifics(values, partner)
        elif mode == 'edit':
            values = self.get_edit_mode_specifics(values)
        return request.website.render(
            'frontend_studio.{0}'.format(mode), values
        )

    @staticmethod
    def get_edit_mode_specifics(values):
        """Update values with details needed to render the studio page
        in mode edit.

        :param dict values: render parameters that will be passed to the
            template.

        :return: updated values.
        """
        values.update({
            'countries': request.env['res.country'].search([]),
            'industries': request.env['res.industry'].search([]),
        })
        return values


    @staticmethod
    def get_view_mode_specifics(values, partner):
        """Update values with details needed to render the studio page
        in mode view.

        :param dict values: render parameters that will be passed to the
            template.
        :param object partner: record of a res.partner.

        :return: updated values.
        """
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
        return values
