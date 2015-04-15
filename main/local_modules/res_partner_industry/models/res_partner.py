# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
from openerp import models, fields

_logger = logging.getLogger(__name__)


class ResPartnerIndustry(models.Model):
    """Industry is simply a copy of res.partner.category"""
    _inherit = 'res.partner.category'
    _name = 'res.partner.industry'
    _description = 'Industry the partner work in.'


class ResPartner(models.Model):
    _inherit = 'res.partner'

    industry_ids = fields.Many2many(
        'res.partner.industry',
        'res_partner_industry_rel',
        'partner_id',
        'industry_id',
        string='Industry',
    )
