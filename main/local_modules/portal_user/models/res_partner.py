# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
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
import pprint
from openerp import fields, models, api

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _is_portal_user(self):
        """Check if the current user is a portal user.

        This hack allows to set a sort of context to the view.
        """
        user = self.env['res.users'].browse(self._uid)
        portal_group = self.env['ir.model.data'].get_object('base',
                                                            'group_portal')
        ret = portal_group in user.groups_id
        _logger.debug('_is_portal_user (uid = {}): {}'.format(self._uid, ret))
        return ret

    @api.model
    def create(self, vals):
        """Set True to is_company if the res.partner is created by someone using
        the portal."""
        vals['is_company'] = self._is_portal_user()
        _logger.debug('vals: {}'.format(pprint.pformat(vals)))
        return super(ResPartner, self).create(vals)

    # Constant to test against to see if the current user is a portal user
    # Should be used in couple with context
    is_portal_user = fields.Boolean(default=True)
