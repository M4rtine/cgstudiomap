# -*- coding: utf-8 -*-
import logging
import werkzeug

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)
PPR = 4  # Products Per Row


class table_compute(object):
    def __init__(self, partner_per_page=20):
        self.table = {}
        self.partner_per_page = partner_per_page

    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in xrange(sizey):
            for x in xrange(sizex):
                if posx + x >= PPR:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(PPR):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, products):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        for p in products:
            x = min(max(1, 1), PPR)
            y = min(max(1, 1), PPR)
            if index >= self.partner_per_page:
                x = y = 1

            pos = minpos
            while not self._check_place(pos % PPR, pos / PPR, x, y):
                pos += 1
            if index >= self.partner_per_page and ((pos + 1.0) / PPR) > maxy:
                break

            if x == 1 and y == 1:  # simple heuristic for CPU optimization
                minpos = pos / PPR

            for y2 in xrange(y):
                for x2 in xrange(x):
                    self.table[(pos / PPR) + y2][(pos % PPR) + x2] = False
            self.table[pos / PPR][pos % PPR] = {
                'product': p, 'x': x, 'y': y,
                'class': " ",
            }
            if index <= self.partner_per_page:
                maxy = max(maxy, y + (pos / PPR))
            index += 1

        # Format table according to HTML needs
        rows = self.table.items()
        rows.sort()
        rows = map(lambda x: x[1], rows)
        for col in xrange(len(rows)):
            cols = rows[col].items()
            cols.sort()
            x += len(cols)
            rows[col] = [
                c for c in map(lambda x: x[1], cols) if c
            ]

        return rows


class QueryURL(object):
    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        l = []
        for k, v in kw.items():
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k, i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k, v)]))
        if l:
            path += '?' + '&'.join(l)
        return path


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

    def partners(self, url='directory', partner_per_page=20, page=0, search='', **post):
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
            'bins': table_compute(partner_per_page=partner_per_page).process(partners),
            'rows': PPR,
            'keep': keep,
            }

        return values

    @http.route(['/directory/list',
                 '/directory/list/page/<int:page>',
                 ], type='http', auth="public", website=True)
    def directory_list(self, **post):
        values = self.partners(url='/directory/list', **post)
        return request.website.render("frontend.list_partners", values)

    @http.route(['/directory/kanban',
                 '/directory/kanban/page/<int:page>',
                 ], type='http', auth="public", website=True)
    def directory_kanban(self, **post):
        values = self.partners(url='/directory/kanban', partner_per_page=50, **post)
        return request.website.render("frontend.kanban_partners", values)

    @http.route(['/directory/map',
                 ], type='http', auth="public", website=True)
    def directory_map(self, **post):
        values = self.partners(url='/directory/map', **post)
        return request.website.render("frontend.map_partners", values)
