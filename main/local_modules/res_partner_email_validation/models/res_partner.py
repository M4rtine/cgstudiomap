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

from openerp import models, api
from openerp.tools.translate import _
from openerp.exceptions import ValidationError
from validate_email import validate_email

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Add a validation of the email address of the partner."""
    _inherit = 'res.partner'

    @api.constrains('email')
    def _validate_email(self):
        """Test against the given email against RFC requirements"""
        _logger.debug('self.email: {}'.format(self.email))
        if not validate_email(self.email):
            raise ValidationError(
                _('The current email seems not valid. Please correct it')
            )
