# -*- coding: utf-8 -*-
import logging
from collections import defaultdict

from cachetools import cached, TTLCache
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

# Cache of 3hours
# The decorated method are refreshed every 1hour.
cache = TTLCache(100, 3600)


class Listing(Website):
    """Representation of the page listing companies."""

    @http.route('/directory/map', type='http', auth="public", website=True)
    def listing(self, **kw):
        """Dispatch between homepage depending on the status of the user."""
        _logger.debug('listing')
        return request.render('frontend_listing.map', {})

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
                number_partners = partner_pool.search_count(
                    partner_pool.active_companies_domain + [
                        ('country_id', '=', country_.id)
                    ],
                )
                if number_partners:
                    by_countries_[country_] = number_partners

            return by_countries_

        _logger.debug('index_public_user')
        page = 'homepage'
        env = request.env
        user_pool = env['res.users']
        partner_pool = env['res.partner']
        # optimisation as it is used in get_partners_by_country
        by_countries = get_partners_by_country(
            request.env['res.country'].search([]))

        values = {
            'page': page,
            'geochart_data': [['Country', 'Popularity']] + [
                [str(country.name), int(value)]
                for country, value in by_countries.items()
            ],
            'nbr_companies': partner_pool.get_number_active_companies(),
            'nbr_users': user_pool.get_number_active_users(),
            'partners': partner_pool.get_most_popular_studios(8),
        }
        return request.render('frontend_homepage.homepage', values)

