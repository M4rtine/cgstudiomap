# -*- coding: utf-8 -*-
import logging

import werkzeug
from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


_logger = logging.getLogger(__name__)

class MainPage(Website):
    @http.route(['/directory/company/<model("res.partner"):partner>'],
                type='http', auth="public", website=True)
    def partner(self, partner, search=''):
        env = request.env
        partner_pool = env['res.partner']

        values = {
            'partner': partner,
            'same_name': partner_pool.search_count(
                [('name', '=', partner.name)]) - 1,
            'same_city': partner_pool.search_count(
                [('city', '=', partner.city)]) - 1,
            'same_country': partner_pool.search_count(
                [('country_id', '=', partner.country_id.id)]) - 1,
        }
        return request.render('frontend.partner', values)

    def partners(self, url='directory', partner_per_page=20, page=0, search='',
                 **post):
        env = request.env
        partner_pool = env['res.partner']
        domain = [
            ('active', '=', True),
            ('is_company', '=', True),
            ('state', '=', 'open'),
        ]
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|',
                    ('name', 'ilike', srch),
                    ('city', 'ilike', srch),
                    ('country_id.name', 'ilike', srch),
                    ('industry_ids.name', 'ilike', srch),
                ]

        keep = QueryURL('/shop', search=search)
        if search:
            post["search"] = search
        partner_count = partner_pool.search_count(domain)
        pager = request.website.pager(
            url=url,
            total=partner_count,
            page=page,
            step=partner_per_page,
            scope=7,
            url_args=post
        )

        partners = partner_pool.search(
            domain,
            limit=partner_per_page,
            offset=pager['offset'],
        )

        values = {
            'search': search,
            'pager': pager,
            'partners': partners,
            'bins': table_compute(partner_per_page=partner_per_page).process(
                partners),
            'rows': PPR,
            'keep': keep,
        }

        return values


    @http.route(['/directory/kanban',
                 '/directory/kanban/page/<int:page>',
                 ], type='http', auth="public", website=True)
    def directory_kanban(self, **post):
        values = self.partners(url='/directory/kanban', partner_per_page=50,
                               **post)
        return request.website.render("frontend.kanban_partners", values)

