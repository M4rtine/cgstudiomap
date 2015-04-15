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
from openerp.osv import orm, fields

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

class ResPartner(orm.Model):
    _inherit = 'res.partner'

    _columns = {
        'computer_graphics_rule': fields.function(
            lambda self, *a, **kw: {},  # placeholder. Not used further anyway
            string="Computer graphics search rule",
            fnct_search=lambda self, *a, **kw: self._search_rule(*a, **kw),
        ),
    }

    def _search_rule(self, cr, uid, ids, name, args, context=None):
        """Check if the given record has the computer graphics industry."""
        ir_model_data_pool = self.pool('ir.model.data')
        industry_cg = ir_model_data_pool.get_object(
            cr, uid, 'res_group_computer_graphics', 'res_partner_industry_computer_graphics'
        )
        return [('industry_id', 'in', [industry_cg.id])]

