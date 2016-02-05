# -*- coding: utf-8 -*-
import base64
import logging

from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (Base, QueryURL)

from openerp import http
from openerp.http import request

_logger = logging.getLogger(__name__)


class Studio(Base):
    """Representation of the homepage of the website."""
    studio_url = '/directory/company'

    @http.route(
        '{0}/<model("res.partner"):partner>/save'.format(studio_url),
        type='http', auth="public", methods=['POST'], website=True
    )
    def save(self, partner,
             country_id=None,
             remove_image=False,
             image_file=None,
             **kwargs):
        """Save new data of the partner.

        Data might be converted to be ingest by odoo.
        For example, list of industries has to be gathered from all the keys
        starting by industry_ids and converted into an odoo leaf to be ingested
        into the X2X industry_ids field.

        For the image several options to the user:
         - a bool (remove_image) that will just remove the current image.
         - a browse (image_file) that will replace the current image by the
         newly selected.

        If the remove_image is True, the image_file is ignored.


        :param object partner: record of a res.partner.
        :param int country_id: id of the country to set the partner to.
        :param bool remove_image: if the current image of the partner should
            be removed.
        :param werkzerg.Filestore image_file: instance that represents the
            new image of the partner.
        :param dict kwargs: list of additional fields to update.

        :return: request.render
        """
        _logger.debug('save')
        _logger.debug('kwargs: %s', kwargs)

        if country_id:
            kwargs['country_id'] = int(country_id)

        if remove_image:
            kwargs['image'] = None

        _logger.debug('condition: %s', image_file and not remove_image)
        if image_file and not remove_image:
            image_b64 = base64.b64encode(image_file.read())
            kwargs['image'] = image_b64

        kwargs['industry_ids'] = [(6, 0, [
            int(value) for key, value in kwargs.iteritems()
            if 'industry_id' in key
        ])]
        # _logger.debug('kwargs: %s', kwargs)


        partner.write(kwargs)
        return self.view(partner)

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
