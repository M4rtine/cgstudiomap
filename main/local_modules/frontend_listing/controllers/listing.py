# -*- coding: utf-8 -*-
import logging
from cachetools import cached, TTLCache
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website
import simplejson
from openerp.http import request, werkzeug

_logger = logging.getLogger(__name__)

# Cache of 3hours
# The decorated method are refreshed every 1hour.
cache = TTLCache(100, 3600)

PPR = 4  # Products Per Row


class TableCompute(object):
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


class Listing(Website):
    """Representation of the page listing companies."""

    map_url = '/directory/map'
    list_url = '/directory/list'

    @http.route(map_url, type='http', auth="public", website=True)
    def map(self, search='', **post):
        """Render the list of studio under a map."""
        url = self.map_url
        env = request.env
        partner_pool = env['res.partner']
        domain = partner_pool.active_companies_domain

        if search:
            domain.extend(partner_pool.search_domain(search))

        _logger.debug('Domain: %s', domain)
        keep = QueryURL(url, search=search)

        if search:
            post["search"] = search

        partners = partner_pool.search(domain)
        geoloc = simplejson.dumps({
            partner.name: [
                partner.partner_latitude,
                partner.partner_longitude,
                partner.name
            ]
            for partner in partners
        })
        safe_search = search.replace(' ', '+')
        _logger.debug(geoloc)
        values = {
            'geoloc': geoloc,
            'search': search,
            'partners': partners,
            'keep': keep,
            'list_url': '{}{}'.format(
                self.list_url, safe_search and '?search={}'.format(safe_search) or ''
            )
        }

        return request.website.render("frontend_listing.map", values)

    @http.route([list_url, '{}/page/<int:page>'.format(list_url),
                 ], type='http', auth="public", website=True)
    def list(self, page=0, search='', **post):
        """Render the list of studio under a table."""
        url = self.list_url
        partner_per_page = 100
        env = request.env
        partner_pool = env['res.partner']
        domain = partner_pool.active_companies_domain

        if search:
            domain.extend(partner_pool.search_domain(search))

        _logger.debug('Domain: %s', domain)
        keep = QueryURL(url, search=search)

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
        _logger.debug('search: %s', search)
        safe_search = search.replace(' ', '+')
        values = {
            'search': search,
            'pager': pager,
            'partners': partners,
            'rows': PPR,
            'keep': keep,
            'map_url': '{}{}'.format(
                self.map_url, safe_search and '?search={}'.format(safe_search) or ''
            )
        }

        return request.website.render("frontend_listing.list", values)

