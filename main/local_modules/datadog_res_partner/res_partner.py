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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def update_count(self):
        company_filters = [
            ('is_company', '=', True),
            ('active', '=', True)
        ]
        statsd.gauge(
            'odoo.res_partner.count.total',
            self.search_count(company_filters)
        )

        statsd.gauge(
            'odoo.res_partner.count.total.open',
            self.search_count(company_filters + [('state', '=', 'open')])
        )

        statsd.gauge(
            'odoo.res_partner.count.total.closed',
            self.search_count(company_filters + [('state', '=', 'closed')])
        )

    @statsd.timed('odoo.res_partner.write.time')
    @api.multi
    def write(self, vals):
        """Track writes of res.partners."""
        _logger.debug('self: %s', self)
        record = super(ResPartner, self).write(vals)
        if self.is_company:
            statsd.increment('odoo.res_partner.writes')

        self.update_count()
        return record

    @statsd.timed('odoo.res_partner.create.time')
    @api.model
    def create(self, vals):
        """Track creates of res.partners."""
        _logger.debug('self: %s', self)
        record = super(ResPartner, self).create(vals)
        if self.is_company:
            statsd.increment('odoo.res_partner.creates')

        self.update_count()
        return record
