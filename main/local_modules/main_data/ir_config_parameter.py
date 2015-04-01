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

from openerp import SUPERUSER_ID
from openerp import models


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    # init might have more arguments than cr.
    # I already saw init called with force kwarg.
    def init(self, cr, *args, **kwargs):
        uid = SUPERUSER_ID
        key = 'geoengine_geonames_username'
        param_id = self.search(cr, uid, [('key', '=', key)], limit=1)
        vals = {'key': key, 'value': 'job_hunting'}
        if param_id:
            self.write(cr, uid, param_id, vals)
        else:
            self.create(cr, uid, vals)
        # Set on the sign in and reset my password features for the front end
        # by default
        self.set_param(cr, uid, 'auth_signup.reset_password', True)
        self.set_param(cr, uid, 'auth_signup.allow_uninvited', True)

# class base_config_settings(models.TransientModel):
#     _inherit = 'base.config.settings'
#
#     def init(self, cr):
#         self.set_param(self._cr, self._uid, 'auth_signup.reset_password', True)
        # icp.set_param(cr, uid, 'auth_signup.allow_uninvited', repr(config.auth_signup_uninvited))
        # icp.set_param(cr, uid, 'auth_signup.template_user_id', repr(config.auth_signup_template_user_id.id))

