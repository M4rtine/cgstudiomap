# -*- coding: utf-8 -*-
from collections import defaultdict

import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
import time
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class MainPage(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        _logger.debug('index')
        time1 = time.time()
        page = 'homepage'
        cr, uid, context = request.cr, request.uid, request.context
        pool = request.registry
        user_pool = pool['res.users']
        partner_pool = pool['res.partner']
        country_pool = pool['res.country']
        ir_model_data_pool = pool['ir.model.data']
        ammap_homepage = ir_model_data_pool.get_object(
            cr, uid, 'frontend', 'homepage_ammap_config', context=context
        )
        filters = [
            ('active', '=', True),
            ('is_company', '=', True),
        ]
        by_countries = defaultdict(int)
        for country in country_pool.search(cr, uid, [], context=context):
            number_partners = partner_pool.search_count(
                cr, uid,
                filters + [('country_id', '=', country)],
                context=context
            )
            if number_partners:
                by_countries[
                    country_pool.browse(cr, uid, country, context=context)
                ] = number_partners

        partners = [
            partner_pool.browse(cr, uid, partner_id)
            for partner_id in partner_pool.search(
                cr, uid, filters, limit=8, order='write_date'
            )
        ]

        # this is too slow I think. Need to make some test on how to have a
        # really fast homepage.
        # cities = set()
        # for partner_id in partner_pool.search(cr, uid, filters):
        #     cities.add(partner_pool.browse(cr, uid, partner_id).city)

        values = {
            'page': page,
            'geochart_data': by_countries,
            'geochart_target': 'geochart_div',
            'ammap_config': ammap_homepage,
            'nbr_partners': partner_pool.search_count(cr, uid, filters),
            'nbr_countries': len(by_countries.keys()),
            # 'nbr_cities': len(cities),
            'nbr_users': user_pool.search_count(
                cr, uid, [('active', '=', True)]
            ),
            'partners': partners,
        }

        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2-time1)*1000.0))
        return request.render('frontend.homepage', values)
