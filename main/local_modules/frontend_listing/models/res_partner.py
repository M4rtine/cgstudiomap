# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging

from openerp import api, models, fields

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    small_image_url = fields.Char('Url to the small image of the partner.')

    def search_domain(self, search):
        """Return the domain that should be used to when a search is processed.

        :param str search: string used for the search.
        :return: list
        """
        _logger.debug('search domain')
        _logger.debug('search: %s', search)
        domain = []

        for sub_search in search.split(' '):
            _logger.debug('sub search: %s', sub_search)
            domain += [
                    '|', '|', '|',
                    ('name', 'ilike', sub_search),
                    ('city', 'ilike', sub_search),
                    ('country_id.name', 'ilike', sub_search),
                    ('industry_ids.name', 'ilike', sub_search)
            ]
        _logger.debug('domain: %s', domain)
        return domain

    @api.multi
    def write(self, vals):
        """Reset the small_image_url value if the image has a new value."""
        _logger.debug('vals: %s', vals)
        if 'image' in vals:
            vals.update({'small_image_url': False})

        _logger.debug('vals: %s', vals)
        return super(ResPartner, self).write(vals)
