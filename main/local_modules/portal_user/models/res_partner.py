# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
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
from openerp import fields, models, api
from openerp import osv

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _columns = {
        'computer_graphics_active_rule': osv.fields.function(
            lambda self, *a, **kw: {},  # placeholder. Not used further anyway
            string="Computer graphics search rule",
            fnct_search=lambda self, *a, **kw: self._search_active_rule(*a, **kw),
            ),
        }

    def _search_active_rule(self, cr, uid, ids, name, args, context=None):
        # FIXME: raise assert stack==1 when ran.
        _logger.debug('_search_active_rule')
        domain = self._search_rule(cr, uid, ids, name, args, context=context)
        domain.append(('active', '=', True))
        _logger.debug('domain: {}'.format(domain))
        return domain

    def _search_rule(self, cr, uid, ids, name, args, context=None):
        """Check if the given records meet the requirement to be seen by a member
        of computer graphics group.
        """
        _logger.debug('_search_rule')
        domain = []
        _logger.debug('user_in_cg_group: {}'.format(self.user_in_cg_group(cr, uid, context=context)))

        if self.user_in_cg_group(cr, uid, context=context):
            # A member of the group CG will only see companies from the industry.
            domain = [
                ('is_company', '=', True),
                ('industry_ids', 'in', [self.get_industry_cg(cr, uid, context=context).id])
            ]

        _logger.debug('domain: {}'.format(domain))
        return domain

    @api.multi
    def _is_portal_user(self):
        """Check if the current user is a portal user.

        This hack allows to set a sort of context to the view.
        """
        user = self.env['res.users'].browse(self._uid)
        portal_group = self.env['ir.model.data'].get_object('base', 'group_portal')
        return portal_group in user.groups_id

    @api.model
    def create(self, vals):
        """Set True to is_company if the res.partner is created by someone using
        the portal."""
        vals['is_company'] = self._is_portal_user()
        return super(ResPartner, self).create(vals)

    # Constant to test against to see if the current user is a portal user
    # Should be used in couple with context
    is_portal_user = fields.Boolean(default=True)

