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
from openerp import api, models
from datadog import statsd

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    def update_count(self):
        filters = [
            ('active', '=', True)
        ]
        statsd.gauge(
            'odoo.res_users.count.total',
            self.search_count(filters)
        )


    @statsd.timed('odoo.res_users.write.time')
    @api.multi
    def write(self, vals):
        """Track writes of res.partners."""
        _logger.debug('self: %s', self)
        record = super(ResUsers, self).write(vals)
        statsd.increment('odoo.res_users.writes')

        self.update_count()
        return record

    @statsd.timed('odoo.res_users.create.time')
    @api.model
    def create(self, vals):
        """Track creates of res.partners."""
        _logger.debug('self: %s', self)
        record = super(ResUsers, self).create(vals)
        statsd.increment('odoo.res_users.creates')

        self.update_count()
        return record
