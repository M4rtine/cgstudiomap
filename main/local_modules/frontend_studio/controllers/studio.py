# -*- coding: utf-8 -*-
import logging

from cachetools import cached
from openerp.addons.frontend_base.models.caches import caches
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

cache = caches.get('cache_3h')


class Homepage(Website):
    """Representation of the homepage of the website."""

    @http.route('/directory/company/<model("res.partner"):partner>',
                type='http', auth="public", website=True)
    def main(self, partner, mode='view'):
        """Dispatch between the different modes of the page.

        :param str mode: mode the page is viewed. Default: view.
            Can be view, edit, create.

        :return: request.render
        """
        _logger.debug('main')
        _logger.debug('partner: %s', partner)
        _logger.debug('mode: %s', mode)
        values = {}
        return request.website.render("frontend_studio.view", values)
