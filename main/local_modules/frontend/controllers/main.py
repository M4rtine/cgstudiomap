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

_logger = logging.getLogger(__name__)


class MainPage(Website):
    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect='/', **kw):
        """Redirect the user to homepage after he logged in."""
        return super(MainPage, self).web_login(redirect=redirect, **kw)

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        """Dispatch between homepage depending on the status of the user."""
        uid = request.uid
        public_user_id = request.website.user_id.id
        is_public_user = uid == public_user_id
        _logger.debug('user is public user? %s', is_public_user)
        if is_public_user:
            return self.index_public_user(**kw)
        else:
            return self.index_logged_user(**kw)

    @cached(cache)
    def index_logged_user(self, **kw):
        """Build the home for a logged user.
        The page is aimed to show the activity on the website.
        """
        time1 = time.time()

        def get_companies(day, hour):
            _logger.debug('day: %s, hour: %s', day, hour)
            filters = [
                ('is_company', '=', True),
                ('active', '=', True)
            ]
            by_date = defaultdict(list)
            for company in self.partner_pool.search(filters):
                by_date[company.write_date].append(company)
                by_date[company.create_date].append(company)

            return by_date

        env = request.env
        # models = env['ir.model.data']
        # res_partner_log = models.get_object('main_data', 'res_partner_write')
        # we don't care about the timezone here as it is just for tokenize
        now = datetime.now()
        self.partner_pool = env['res.partner']
        by_date = get_companies(now.day, now.hour)
        values = {
            'sorted_keys': sorted(by_date.keys(), reverse=True)[:20],
            'by_date': by_date,
        }
        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2 - time1) * 1000.0))
        return request.render('frontend.homepage_logged_user', values)

    @cached(cache)
    def index_public_user(self, **kw):
        """Build the homepage for a public user.
        This homepage is aimed to attract the user to login.
        """

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
            'geochart_data': [['Country', 'Popularity']] + [
                [str(country.name), int(value)]
                for country, value in by_countries.items()
            ],
            'nbr_partners': self.partner_pool.search_count(filters),
            'nbr_countries': len(by_countries.keys()),
            'nbr_users': user_pool.search_count([('active', '=', True)]),
            'partners': self.get_most_popular_studios(8),
        }
        _logger.debug('geochart_data: %s', values['geochart_data'])
        time2 = time.time()


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
                    ('image', '!=', False)
                ]
            )
        ]

        # doing kind of unittest in here as I do not know how to
        # do unittest with request :(
        assert company.partner_id.id not in [p.id for p in partners], (
            'cgstudiomap is in the most popular studio list'
        )
        return random.sample(partners, min(len(partners), sample))
