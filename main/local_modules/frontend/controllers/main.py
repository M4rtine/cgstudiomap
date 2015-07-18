# -*- coding: utf-8 -*-
from collections import defaultdict
import random

import time
import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
_logger = logging.getLogger(__name__)


class MainPage(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        _logger.debug('index')
        time1 = time.time()
        page = 'homepage'
        env = request.env
        user_pool = env['res.users']
        partner_pool = env['res.partner']
        country_pool = env['res.country']
        ammap_homepage = env.ref('frontend.homepage_ammap_config')
        filters = [('active', '=', True), ('is_company', '=', True)]
        by_countries = defaultdict(int)
        for country in country_pool.search([]):
            number_partners = partner_pool.search_count(
                filters + [('country_id', '=', country.id)],
            )
            if number_partners:
                by_countries[country] = number_partners

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        partners = [
            p for p in partner_pool.search(filters + [('image', '!=', False)])
        ]

        sample_partners = random.sample(partners, min(len(partners), 8))

        values = {
            'page': page,
            'geochart_data': by_countries,
            'geochart_target': 'geochart_div',
            'ammap_config': ammap_homepage,
            'nbr_partners': partner_pool.search_count(filters),
            'nbr_countries': len(by_countries.keys()),
            'nbr_users': user_pool.search_count([('active', '=', True)]),
            'partners': sample_partners,
        }

        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2-time1)*1000.0))
        return request.render('frontend.homepage', values)
