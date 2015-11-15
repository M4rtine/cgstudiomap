# -*- coding: utf-8 -*-
import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


_logger = logging.getLogger(__name__)


class Shop(Website):
    @http.route('/shop', type='http', auth="public", website=True)
    def shop(self, **kw):

        return request.render(
            'frontend_shop.shop',
            {'url': 'https://society6.com/cgstudiomap'}
        )
