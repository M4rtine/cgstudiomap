# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import logging

from openerp import models, api, fields

_logger = logging.getLogger(__name__)
__codec__ = 'utf-8'


class ResMissingDetail(models.Model):
    _name = 'res.missing_detail'
    _description = 'Missing Detail'

    name = fields.Char('Name', size=128, required=True)
    image = fields.Binary(
        "Image",
        help="This field holds the image used as avatar for this industry,"
             " limited to 1024x1024px"
    )
    description = fields.Text('Description')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    missing_detail_ids = fields.Many2many(
        'res.missing_detail',
        string='Missing Details'
    )
    last_missing_details_check = fields.Date()

    @api.model
    def get_missing_details(self):
        """Get all the missing details for the current partner.

        :return: list of missing detail ids.
        """
        return []

    @api.model
    def set_missing_details(self, vals=None):
        """Method to call to write the missing details to the partner."""
        vals = vals or {}
        missing_details = self.get_missing_details()

        if missing_details:
            leaves = [(6, 0, missing_details)]
        else:
            leaves = [(5)]

        vals.update({
            'missing_detail_ids': leaves,
            'last_missing_details_check': fields.date.today(),
        })

        return vals

    @api.model
    def set_missing_details_bot(self, limit=10):
        """Method called by the bot."""
        leaves = [
            '|',
            ('last_missing_details_check', '=', False),
            ('last_missing_details_check', '<', fields.date.today()),
            ('is_company', '=', True)
        ]
        for partner in self.search(leaves,
                                   order='last_missing_details_check',
                                   limit=limit):
            _logger.info(
                'Checking for missing details: {}'.format(
                    partner.name.encode(__codec__)
                )
            )
            _logger.debug('Write from bot.')
            details = partner.set_missing_details()
            _logger.debug('Missing Details: {}'.format(details))
            partner.write(details)
