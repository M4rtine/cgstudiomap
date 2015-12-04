# -*- coding: utf-8 -*-
import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


_logger = logging.getLogger(__name__)


class MainPage(Website):
    LOGIN_REDIRECTION = '/web/login/processing'

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=LOGIN_REDIRECTION, **kw):
        """Redirect the user to homepage after he logged in."""
        _logger.debug('web_login redirection.')
        return super(MainPage, self).web_login(redirect=redirect, **kw)

    @http.route(LOGIN_REDIRECTION, type='http', auth="none")
    def web_login_temp_page(self, redirect=LOGIN_REDIRECTION, **kw):
        """Redirect the user to homepage after he logged in."""
        _logger.debug('web_login_temp_page redirection.')
        return request.render('frontend.web_login_temp_page')
