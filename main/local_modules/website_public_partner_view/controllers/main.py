# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website

_logger = logging.getLogger(__name__)
PPG = 20 # Partner Per Page
PPR = 4  # Products Per Row

class table_compute(object):
    def __init__(self):
        self.table = {}

    def _check_place(self, posx, posy, sizex, sizey):
        res = True
        for y in xrange(sizey):
            for x in xrange(sizex):
                if posx+x>=PPR:
                    res = False
                    break
                row = self.table.setdefault(posy+y, {})
                if row.setdefault(posx+x) is not None:
                    res = False
                    break
            for x in range(PPR):
                self.table[posy+y].setdefault(x, None)
        return res

    def process(self, products):
        # Compute products positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        for p in products:
            x = min(max(1, 1), PPR)
            y = min(max(1, 1), PPR)
            if index>=PPG:
                x = y = 1

            pos = minpos
            while not self._check_place(pos%PPR, pos/PPR, x, y):
                pos += 1
            # if 21st products (index 20) and the last line is full (PPR products in it), break
            # (pos + 1.0) / PPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= PPG and ((pos + 1.0) / PPR) > maxy:
                break

            if x==1 and y==1:   # simple heuristic for CPU optimization
                minpos = pos/PPR

            for y2 in xrange(y):
                for x2 in xrange(x):
                    self.table[(pos/PPR)+y2][(pos%PPR)+x2] = False
            self.table[pos/PPR][pos%PPR] = {
                'product': p, 'x':x, 'y': y,
                'class': " ",
            }
            if index<=PPG:
                maxy=max(maxy,y+(pos/PPR))
            index += 1

        # Format table according to HTML needs
        rows = self.table.items()
        rows.sort()
        rows = map(lambda x: x[1], rows)
        for col in range(len(rows)):
            cols = rows[col].items()
            cols.sort()
            x += len(cols)
            rows[col] = [c for c in map(lambda x: x[1], cols) if c != False]

        return rows

        # TODO keep with input type hidden

class QueryURL(object):
    def __init__(self, path='', **args):
        self.path = path
        self.args = args

    def __call__(self, path=None, **kw):
        if not path:
            path = self.path
        for k,v in self.args.items():
            kw.setdefault(k,v)
        l = []
        for k,v in kw.items():
            if v:
                if isinstance(v, list) or isinstance(v, set):
                    l.append(werkzeug.url_encode([(k,i) for i in v]))
                else:
                    l.append(werkzeug.url_encode([(k,v)]))
        if l:
            path += '?' + '&'.join(l)
        return path

class MainPage(Website):

    @http.route(['/directory/company/<model("res.partner"):partner>'],
                type='http', auth="public", website=True)
    def partner(self, partner, search=''):
        keep = QueryURL('/directory', search=search)
        values = {'partner': partner, keep: 'keep'}

        return request.render('website_public_partner_view.partner', values)


    @http.route(['/directory',
                 '/directory/page/<int:page>',
                 ], type='http', auth="public", website=True)
    def partners(self, page=0, search='', **post):
        if search:
            print '-'*20
            print 'SEARCH', search
            print '-'*20

        if page:
            print '='*20
            print 'PAGE:', page
            print '='*20
        env = request.env
        partner_pool = env['res.partner']
        domain = [
            ('active', '=', True),
            ('is_company', '=', True),
        ]
        if search:
            for srch in search.split(" "):
                domain += ['|',  ('name', 'ilike', srch), ('city', 'ilike', srch)]
        keep = QueryURL('/shop', search=search)
        if search:
            post["search"] = search
        url = "/directory"
        partner_count = partner_pool.search_count(domain)
        pager = request.website.pager(
            url=url,
            total=partner_count,
            page=page,
            step=PPG,
            scope=7,
            url_args=post
        )

        partners = partner_pool.search(
            domain,
            limit=PPG,
            offset=pager['offset'],
            # order='website_published desc, website_sequence desc',
        )

        values = {
            'search': search,
            'pager': pager,
            'partners': partners,
            'bins': table_compute().process(partners),
            'rows': PPR,
            'keep': keep,
        }

        pprint.pprint(values)
        return request.website.render("website_public_partner_view.partners", values)

