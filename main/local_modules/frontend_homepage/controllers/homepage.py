# -*- coding: utf-8 -*-
from collections import defaultdict
import random
import time
import logging
from datetime import datetime

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
from cachetools import cached, TTLCache


_logger = logging.getLogger(__name__)

# Cache of 12hours
# The decorated method are refreshed every 12hours.
cache = TTLCache(100, 43200)


class Homepage(Website):
    """Representation of the homepage of the website."""
    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        """Dispatch between homepage depending on the status of the user."""
        _logger.debug('index')
        uid = request.uid
        public_user_id = request.website.user_id.id
        is_public_user = uid == public_user_id
        _logger.debug('uid: %s', uid)
        _logger.debug('user is public user? %s', is_public_user)
        if is_public_user:
            return self.index_public_user(**kw)
        else:
            return self.index_public_user(**kw)

    def index_public_user(self, **kw):
        """Build the homepage for a public user.
        This homepage is aimed to attract the user to login.
        """

        @cached(cache)
        def get_partners_by_country(countries):
            """Method to be memorized that return the number of partner in a country.

            :param instance country: record of a country
            :return: dict {country instance: count of partners in the country}

            """
            by_countries_ = defaultdict(int)

            for country_ in countries:
                # by_countries.update(get_partners_by_country(country_))
                number_partners = self.partner_pool.search_count(
                    filters + [('country_id', '=', country_.id)],
                )
                if number_partners:
                    by_countries_[country_] = number_partners

            return by_countries_

        _logger.debug('index_public_user')
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
        by_countries = get_partners_by_country(country_pool.search([]))

        values = {
            'page': page,
            'geochart_data': [['Country', 'Popularity']] + [
                [str(country.name), int(value)]
                for country, value in by_countries.items()
            ],
            'nbr_partners': self.partner_pool.search_count(filters),
            'nbr_countries': len(by_countries.keys()),
            'nbr_users': user_pool.search_count([('active', '=', True)]),
            'partners': self.get_most_popular_studios(8),
        }
        # _logger.debug('geochart_data: %s', values['geochart_data'])
        time2 = time.time()
        return request.render('frontend_homepage.homepage', values)

    @staticmethod
    def get_most_popular_studios(sample_):
        """Return a list of partners that have a logo.

        The list is filtered to just returns partner that match:
        - is active
        - is a company
        - is not the partner related to cgstudiomap
        - has an image.
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
                    ('image', '!=', False)
                ]
            )
        ]

        # doing kind of unittest in here as I do not know how to
        # do unittest with request :(
        assert company.partner_id.id not in [p.id for p in partners], (
            'cgstudiomap is in the most popular studio list'
        )
        return random.sample(partners, min(len(partners), sample_))
