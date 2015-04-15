# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  Jordi Riera <kender.jr@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
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
from openerp import api, models

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def __get_cg_data(self, external_id):
        """Get in ir_model_data, the external_id related to res_group_computer_graphics namespace"""
        ir_model_data_pool = self.env['ir.model.data']
        return ir_model_data_pool.get_object(
            'res_group_computer_graphics', external_id
        )

    @api.model
    def get_industry_cg(self):
        """Return the record representing the industry Computer Graphics.

        :return: res.partner.industry record
        """
        return self.__get_cg_data('res_partner_industry_computer_graphics')

    @api.model
    def get_group_cg(self):
        """Return the record representing the group Computer Graphics.

        :return: res.groups record
        """
        return self.__get_cg_data('group_computer_graphics')

    @api.model
    def user_in_cg_group(self):
        """Check if the user related to the uid is in the group computer graphics.

        :return: boolean
        """
        user_pool = self.env['res.users']
        return self.get_group_cg() in user_pool.browse(self._uid).groups_id

    @api.model
    def create(self, vals):
        """Force the addition of industry CG if the user is from the group CG."""
        if self.user_in_cg_group():
            vals['industry_ids'] = [(6, 0, [self.get_industry_cg().id])]

        return super(ResPartner, self).create(vals)
