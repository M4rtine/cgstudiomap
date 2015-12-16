# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def search_domain(self, search):
        """Return the domain that should be used to when a search is processed.

        :param str search: string used for the search.
        :return: list
        """
        domain = []

        for srch in search.split(' '):
            domain += [
                    '|', '|', '|',
                    ('name', 'ilike', srch),
                    ('city', 'ilike', srch),
                    ('country_id.name', 'ilike', srch),
                    ('industry_ids.name', 'ilike', srch)
            ]

        return domain
