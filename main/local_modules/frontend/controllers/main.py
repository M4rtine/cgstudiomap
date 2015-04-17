# -*- coding: utf-8 -*-
from collections import defaultdict

import logging
import re

import openerp
from openerp.addons.web.controllers.main import WebClient
from openerp.addons.web import http
from openerp.http import request, STATIC_CACHE
from openerp.tools import image_save_for_web
from openerp.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)


class MainPage(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        _logger.debug('index')
        page = 'homepage'
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        partner_pool = pool['res.partner']
        ir_model_data_pool = pool['ir.model.data']
        industry_cg = ir_model_data_pool.get_object(
            cr, uid, 'res_group_computer_graphics', 'res_partner_industry_computer_graphics'
        )
        company_ids = partner_pool.search(
            cr, uid, [('active', '=', True), ('is_company', '=', True), ('industry_ids', 'in', [industry_cg.id])]
        )

        by_countries = defaultdict(int)
        for country in [partner_pool.browse(cr, uid, i).country_id for i in company_ids]:
            by_countries[country] = by_countries[country] + 1

        values = {
            'page': page,
            'geochart_data': by_countries,
            'geochart_target': 'geochart_div',
            }
        # try:
        #     main_menu = request.registry['ir.model.data'].get_object(request.cr, request.uid, 'website', 'main_menu')
        #     _logger.debug('main_menu: {}'.format(main_menu))
        # except Exception:
        #     pass
        # else:
        #     first_menu = main_menu.child_id and main_menu.child_id[0]
        #     _logger.debug('first_menu: {}'.format(first_menu))
        #     if first_menu:
        #         if not (first_menu.url.startswith(('/page/', '/?', '/#')) or (first_menu.url=='/')):
        #             _logger.debug('Rendering first_menu.url')
        #             return request.redirect(first_menu.url, values)
        #         if first_menu.url.startswith('/page/'):
        #             _logger.debug('Rendering ir.http: {}'.format(first_menu.url))
        #             return request.registry['ir.http'].reroute(first_menu.url, values)

        return request.render('frontend.homepage', values)

