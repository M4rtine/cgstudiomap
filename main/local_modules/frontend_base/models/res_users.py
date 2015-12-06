# -*- coding: utf-8 -*-
"""Suite of methods common operation on res.users."""
import logging

from openerp import api, models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def get_active_users(self):
        """Return recordsets of all the active users.

        :return: recordset.
        """
        return self.search([('active', '=', True)])

    @api.model
    def get_number_active_users(self):
        """Return number of active users.

        :return: int
        """
        return len(self.get_active_users())
