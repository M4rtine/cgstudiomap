# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import logging
import random

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Overcharge the definition of a partner."""
    _inherit = 'res.partner'

    @api.model
    def get_studios_from_same_location(self):
        """Return a list of partners that have a logo with the same locations
        that the given partner.

        :return: list of partner records.
        """
        company_pool = self.env['res.company']
        # #294
        # Looking for cgstudiomap to avoid to have it displayed.
        # cgstudiomap is actually the partner linked to the res.company
        # of the instance.
        # looking for the first (and only so far) res.company
        company = company_pool.browse(1)

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        # search return a recordset and we cannot do len() on it.
        partners = [
            partner for partner in self.search(
                self.open_companies_domain +
                [
                    ('id', '!=', company.partner_id.id),
                    ('image', '!=', False),
                    ('country_id', '=', self.country_id.id),
                    ('id', '!=', self.id)
                ]
            )
            ]

        return partners

    @api.model
    def get_random_studios_from_same_location(self, sample_):
        """Return a random sample from the list of partners
        are returned from `self.get_studios_from_same_location`

        :param int sample_: size of the sample of partners.
        :return: list of partner records.
        """
        partners = self.get_studios_from_same_location()
        return random.sample(partners, min(len(partners), sample_))
