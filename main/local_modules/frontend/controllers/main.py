# -*- coding: utf-8 -*-
import logging

import werkzeug.utils
from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
from openerp.addons.web.controllers.main import ensure_db
import openerp


_logger = logging.getLogger(__name__)


class MainPage(Website):
    LOGIN_REDIRECTION = '/web/login/processing'

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=LOGIN_REDIRECTION, **kw):
        """Redirect the user to homepage after he logged in."""
        _logger.debug('web_login redirection.')
        ensure_db()

        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = openerp.SUPERUSER_ID

        values = request.params.copy()
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params['login'], request.params['password'])
            if uid is not False:
                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"
        if request.env.ref('web.login', False):
            return request.render('web.login', values)
        else:
            # probably not an odoo compatible database
            error = 'Unable to login on database %s' % request.session.db
            return werkzeug.utils.redirect('/web/database/selector?error=%s' % error, 303)

        # return super(MainPage, self).web_login(redirect=redirect, **kw)

    @http.route(LOGIN_REDIRECTION, type='http', auth="none")
    def web_login_temp_page(self, redirect=LOGIN_REDIRECTION, **kw):
        """Redirect the user to homepage after he logged in."""
        _logger.debug('web_login_temp_page redirection.')
        return self.render('frontend.web_login_temp_page')

    @http.route(['/page/website.contactus', '/page/contactus'], type='http', auth="public", website=True)
    def contact(self, **kwargs):
        values = {}
        for field in ['description', 'partner_name', 'phone', 'contact_name', 'email_from', 'name']:
            if kwargs.get(field):
                values[field] = kwargs.pop(field)
        values.update(kwargs=kwargs.items())
        return self.render("website.contactus", values)
