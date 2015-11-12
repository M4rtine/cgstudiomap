# -*- coding: utf-8 -*-
from collections import defaultdict
import collections
import functools
import random
import time
import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


_logger = logging.getLogger(__name__)


class Memorized(object):
    """Decorator. Caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned
    (not reevaluated).
    """

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        if not isinstance(args, collections.Hashable):
            # uncacheable. a list, for instance.
            # better to not cache than blow up.
            return self.func(*args)
        if args in self.cache:
            return self.cache[args]
        else:
            value = self.func(*args)
            self.cache[args] = value
            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


class MainPage(Website):
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):

        @Memorized
        def get_partners_by_country(country):
            """Method to be memorized that return the number of partner in a country.

            :param instance country: record of a country
            :return: dict {country instance: count of partners in the country}
            """
            number_partners = self.partner_pool.search_count(
                filters + [('country_id', '=', country.id)],
            )
            if number_partners:
                return {country: number_partners}

            return {}

        _logger.debug('index')
        time1 = time.time()
        page = 'homepage'
        env = request.env
        user_pool = env['res.users']
        # optimisation as it is used in get_partners_by_country
        self.partner_pool = env['res.partner']
        country_pool = env['res.country']
        filters = [
            ('active', '=', True),
            ('is_company', '=', True),
        ]
        by_countries = defaultdict(int)
        for country in country_pool.search([]):
            by_countries.update(get_partners_by_country(country))

        values = {
            'page': page,
            'geochart_data': by_countries,
            'geochart_target': 'geochart_div',
            'nbr_partners': self.partner_pool.search_count(filters),
            'nbr_countries': len(by_countries.keys()),
            'nbr_users': user_pool.search_count([('active', '=', True)]),
            'partners': self.get_most_popular_studios(8),
        }

        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2 - time1) * 1000.0))
        return request.render('frontend.homepage', values)


    @staticmethod
    def get_most_popular_studios(sample):
        """Return a list of partners that have a logo.

        The list is filtered to just returns partner that match:
        - is active
        - is a company
        - is not the partner related to cgstudiomap
        - has an image.
        :param partner_pool: pool of partners
        :param list filters: domains to apply on top of the domain about images.
        :return: list of partner records.
        """
        env = request.env
        company_pool = env['res.company']
        partner_pool = env['res.partner']
        # #294
        # Looking for cgstudiomap to avoid to have it displayed.
        # cgstudiomap is actually the partner linked to the res.company
        # of the instance.
        # looking for the first (and only so far) res.company
        company = company_pool.browse(1)

        # https://github.com/cgstudiomap/cgstudiomap/issues/177
        # search return a recordset and we cannot do len() on it.
        partners = [
            partner for partner in partner_pool.search(
                [
                    ('active', '=', True),
                    ('is_company', '=', True),
                    ('id', '!=', company.partner_id.id),
                    [('image', '!=', False)]
                ]
            )
        ]

        # doing kind of unittest in here as I do not know how to
        # do unittest with request :(
        assert company.partner_id.id not in partners, (
            'cgstudiomap is in the most popular studio list'
        )
        return random.sample(partners, min(len(partners), sample))
