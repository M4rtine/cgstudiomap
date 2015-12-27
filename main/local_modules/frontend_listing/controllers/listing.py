# -*- coding: utf-8 -*-
import logging

import simplejson
from cachetools import cached, TTLCache
from datadog import statsd
from openerp.addons.web import http
from openerp.addons.frontend_base.models.caches import caches
from openerp.addons.website.controllers.main import Website

from openerp.http import request, werkzeug

_logger = logging.getLogger(__name__)

cache = caches.get('cache_1h')


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

    @cached(cache)
    def get_partners(self, partner_pool, search=''):
        """Wrapper to be able to cache the result of a search in the
        partner_pool
        """
        domain = partner_pool.open_companies_domain
        if search:
            domain.extend(partner_pool.search_domain(search))
        _logger.debug('Domain: %s', domain)
        return partner_pool.search(domain)

    @statsd.timed('odoo.frontend.list.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(map_url, type='http', auth="public", website=True)
    def map(self, search='', **post):
        """Render the list of studio under a map."""
        url = self.map_url
        keep = QueryURL(url, search=search)

        if search:
            post["search"] = search

        partners = self.get_partners(request.env['res.partner'], search=search)
        geoloc = simplejson.dumps(
            {
                partner.name: [
                    partner.partner_latitude,
                    partner.partner_longitude,
                    partner.name
                ]
                for partner in partners
            }
        )
        safe_search = search.replace(' ', '+')
        _logger.debug(geoloc)
        values = {
            'geoloc': geoloc,
            'search': search,
            'partners': partners,
            'keep': keep,
            'list_url': '{}{}'.format(
                self.list_url,
                safe_search and '?search={}'.format(safe_search) or ''
            )
        }

        return request.website.render("frontend_listing.map", values)

    @statsd.timed('odoo.frontend.map.time', tags=['frontend', 'frontend:listing'])
    @http.route(list_url, type='http', auth="public", website=True)
    def list(self, page=0, search='', **post):
        """Render the list of studio under a table."""
        url = self.list_url

        keep = QueryURL(url, search=search)

        if search:
            post["search"] = search

        partners = self.get_partners(request.env['res.partner'], search=search)
        _logger.debug('search: %s', search)
        safe_search = search.replace(' ', '+')
        values = {
            'search': search,
            'partners': partners,
            'keep': keep,
            'map_url': '{}{}'.format(
                self.map_url,
                safe_search and '?search={}'.format(safe_search) or ''
            )
        }

        return request.website.render("frontend_listing.list", values)
