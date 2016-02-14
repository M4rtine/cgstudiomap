# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.partner."""
import base64
import logging
import random
import re

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartnerGetStudios(models.Model):
    """Overcharge the definition of a partner with methods to get studios
    from the location of the partner.
    """
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


class ResPartnerSave(models.Model):
    """Overcharge the definition of a partner to add methods to update
    from the save page.
    """
    _inherit = 'res.partner'

    @staticmethod
    def get_base64_from_filestore(filestore):
        """Encode a werkzerg.Filestore to a string using base64.

        :param werkzerg.Filestore filestore: instance that represents the
            new image of the partner.
        :return: image encoded using base64
        :rtype: str
        """
        return base64.b64encode(filestore.read())

    @api.model
    def clean_values_from_post_request(self,
                                       country_id=None,
                                       remove_image=False,
                                       image_file=None,
                                       **kwargs):
        """Clean the different values coming from the save post request.

        Data might be converted to be ingested by odoo.
        For example, list of industries has to be gathered from all the keys
        starting by industry_ids and converted into an odoo leaf to be ingested
        into the X2X industry_ids field.

        For the image several options to the user:
         - a bool (remove_image) that will just remove the current image.
         - a browse (image_file) that will replace the current image by the
         newly selected.

        If the remove_image is True, the image_file is ignored.

        :param int country_id: id of the country to set the partner to.
        :param bool remove_image: if the current image of the partner should
            be removed.
        :param werkzerg.Filestore image_file: instance that represents the
            new image of the partner.
        :param dict kwargs: list of additional fields to update.

        :return: request.render
        """
        values = kwargs
        if country_id:
            values['country_id'] = int(country_id)

        if remove_image:
            values['image'] = None

        _logger.debug('condition: %s', image_file and not remove_image)
        if image_file and not remove_image:
            values['image'] = self.get_base64_from_filestore(image_file)
        industry_ids = []
        for key, value in kwargs.items():
            if 'industry_ids' in key:
                industry_ids.append(int(value))
                del kwargs[key]

        if industry_ids:
            values['industry_ids'] = [(6, 0, industry_ids)]

        return values

    @api.model
    def create_from_post_request(self, kwargs):
        """Process a create from data coming from a post request."""
        return self.create(self.clean_values_from_post_request(**kwargs))

    @api.model
    def write_from_post_request(self, kwargs):
        """Process a write from data coming from a post request."""
        return self.write(self.clean_values_from_post_request(**kwargs))
