# -*- coding: utf-8 -*-
import logging
import time

import simplejson
from cachetools import TTLCache, cached
from datadog import statsd
from openerp.addons.frontend_base.controllers.base import (
    Base,
    small_image_url,
    QueryURL,
)
from openerp.addons.web import http

from openerp.http import request

_logger = logging.getLogger(__name__)


def reset_cache(max_size=10, ttl=10800):
    """Reset the given cache.

    :param int max_size: the max number of caches. Default: 10
    :param int ttl: The time max the cache lives. The cache
        will reset itself after this time. Default: 10800 (3hrs)

    :return: cachetools.TTLCache instance.
    """
    return TTLCache(max_size, ttl)


class Listing(Base):
    """Representation of the page listing companies.

    Pages of listing are cached using list_cache and map_cache. That is
    because there is a lot of data to load and many because of the build of
    the list object from this data.

    To manage the cache, the attribute `force_reset_cache` has been set.
    It allows a user to force to rebuild the cache if for example a massive
    update on data has been operated.

    To use the force_cache_reset the url should look like:
    * to reset the cache of the map
        /directory?force_cache_reset=1
    * to reset the cache of the list
        /directory/list?force_cache_reset=1
    """
    # the cache are set to None so they are set at the first call of the pages.
    list_cache = None
    map_cache = None
    map_url = '/directory'
    list_url = '/directory/list'

    @staticmethod
    def is_beta_tester():
        """Return if the user is illegible to beta test features.

        :rtype: boolean
        """
        uid = request.uid
        public_user_id = request.website.user_id.id
        is_public_user = uid == public_user_id
        if not is_public_user:
            user_pool = request.env['res.users']
            user = user_pool.browse(uid)

            ir_model_data = request.env['ir.model.data']
            group_beta_tester = ir_model_data.xmlid_to_object(
                'res_group_archetype.group_archetype_beta_tester'
            )
            is_beta_tester = group_beta_tester in user.groups_id
            _logger.debug('is_beta_tester: %s', is_beta_tester)

            return is_beta_tester

        return False

    def get_partners(self, partner_pool, search='', company_status='open'):
        """Wrapper to be able to cache the result of a search in the
        partner_pool.

        :return: record set answering the search criteria.
        """
        return partner_pool.search(
            self.get_company_domain(search, company_status)
        )

    @statsd.timed('odoo.frontend.ajax.get_partner',
                  tags=['frontend', 'frontend:listing', 'ajax'])
    @http.route('/directory/get_partners',
                type='http', auth="public", methods=['POST'], website=True)
    def get_partner_json(self, search='', company_status='open'):
        """Return a json with the partner matching the search

        :param str search: search to filter with
        :return: json dumps
        """

        def build_details_beta_test(partners):
            """Gather the details to build later the table of companies.
            FOR BETA TESTING PURPOSE.

            :param list partners: recordsets of partner to gather the details
                from.
            :return: json dump.
            """
            return simplejson.dumps(
                [
                    {
                        'logo': '<img itemprop="image" '
                                'class="img img-responsive" '
                                'src="{0}"'
                                '/>'.format(
                            small_image_url(partner, 'image_small')),

                        # self.partner_url = ''.format(self.id)
                        'name': '<a href="/directory/company/{0.id}">{1}</a>'.format(  # noqa
                            partner, partner.name.encode('utf-8')
                        ),
                        'email': partner.email or '',
                        'industries': ' '.join(
                            [
                                ind.tag_url_link(
                                    company_status=company_status,
                                    listing=True
                                )
                                for ind in partner.industry_ids
                                ]
                        ),
                        'location': partner.location,
                    }
                    for partner in partners
                    ],
            )

        @cached(self.list_cache)
        def build_details(partners):
            """Gather the details to build later the table of companies.

            :param list partners: recordsets of partner to gather the details
                from.
            :return: json dump.
            """
            return simplejson.dumps(
                [
                    {
                        'logo': '<img itemprop="image" '
                                'class="img img-responsive" '
                                'src="{0}"'
                                '/>'.format(
                            small_image_url(partner, 'image_small')),
                        'name': '<a href="{0.partner_url}">{1}</a>'.format(
                            partner, partner.name.encode('utf-8')
                        ),
                        'email': partner.email or '',
                        'industries': ' '.join(
                            [
                                ind.tag_url_link(
                                    company_status=company_status,
                                    listing=True
                                )
                                for ind in partner.industry_ids
                                ]
                        ),
                        'city': partner.city,
                        'state_name': partner.state_id.name,
                        'country_name': partner.country_id.name,
                    }
                    for partner in partners
                ],
            )

        _logger.debug('search: %s', search)
        _logger.debug('company_status: %s', company_status)
        t1 = time.time()
        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )
        _logger.debug('Query time: %s', time.time() - t1)
        t1 = time.time()
        build_details_method = (
            self.is_beta_tester() and build_details_beta_test or build_details
        )
        details = build_details_method(partners)
        _logger.debug(
            'cache.currsize: %s', self.list_cache.currsize
        )
        statsd.gauge(
            'odoo.frontend.list_cache_currsize',
            self.list_cache.currsize
        )
        _logger.debug('dump timing: %s', time.time() - t1)
        return details

    @statsd.timed('odoo.frontend.map.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(map_url, type='http', auth="public", website=True)
    def map(self,
            company_status='open',
            search='',
            force_cache_reset=False,
            **post):
        """Render the list of studio under a map.

        :param bool force_cache_reset: if the cache of the
            page needs to be reset.
        """

        _logger.debug('force_cache_reset: %s', force_cache_reset)
        if self.map_cache is None or force_cache_reset:
            _logger.debug('Reset the cache map_cache')
            self.map_cache = reset_cache()

        @cached(self.map_cache)
        def build_details(partners):
            """Gather details from partners to be displayed on the map.

            :param recordset partners: partners to gather the details from.
            :return: json dump.
            """
            statsd.gauge(
                'odoo.frontend.map_cache.currsize',
                self.map_cache.currsize
            )
            return simplejson.dumps(
                {
                    partner.id: [
                        partner.partner_latitude,
                        partner.partner_longitude,
                        partner.info_window(company_status),
                    ]
                    for partner in partners
                    }
            )

        url = self.map_url
        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        partners = self.get_partners(
            request.env['res.partner'],
            search=search,
            company_status=company_status
        )

        t1 = time.time()
        geoloc = build_details(partners)
        _logger.debug('dump timing: %s', time.time() - t1)

        values = {
            'geoloc': geoloc,
            'search': search,
            'company_status': company_status,
            'partners': partners,
            'keep': keep,
            'map_url': self.map_url,
            'list_url': self.list_url,
            'url': self.map_url,
        }

        return request.website.render("frontend_listing.map", values)

    @statsd.timed('odoo.frontend.list.time',
                  tags=['frontend', 'frontend:listing'])
    @http.route(list_url, type='http', auth="public", website=True)
    def list(self,
             company_status='open',
             page=0,
             search='',
             force_cache_reset=False,
             **post):
        """Render the list of studio under a table.

        :param bool force_cache_reset: if the cache of the
            page needs to be reset.
        """
        _logger.debug('force_cache_reset: %s', force_cache_reset)

        if self.list_cache is None or force_cache_reset:
            _logger.debug('Reset the cache list_cache')
            self.list_cache = reset_cache()

        url = self.list_url

        keep = QueryURL(url, search=search, company_status=company_status)

        if search:
            post["search"] = search

        values = {
            'search': search,
            'company_status': company_status,
            'keep': keep,
            'map_url': self.map_url,
            'list_url': self.list_url,
            'url': self.list_url,
        }

        return request.website.render("frontend_listing.list", values)
