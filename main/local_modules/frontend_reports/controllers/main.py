# -*- coding: utf-8 -*-
from collections import defaultdict
import datetime
import time
import logging
import operator

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
from cachetools import cached, TTLCache




# Cache of 12hours
# The decorated method are refreshed every 12hours.
cache = TTLCache(100, 43200)

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


# First day of the beta
first_day = datetime.date(2015, 07, 15)
month = str(datetime.date.today() - datetime.timedelta(days=30))
week = str(datetime.date.today() - datetime.timedelta(days=7))


class MainPage(Website):
    @staticmethod
    def fill_dict_days(by_date):
        """Fill the missing dates with 0

        :param by_date: dict
        :param first_day: the day to start
        :return: dict
        """
        today = datetime.date.today()
        current_day = first_day
        while current_day <= today:
            if str(current_day) not in by_date:
                by_date[str(current_day)] = 0
            current_day = current_day + datetime.timedelta(days=1)

        return by_date

    @staticmethod
    def sort_dict(by_date):
        return [
            [[int(i) for i in k.split('-')], by_date[k]]
            for k in sorted(by_date.keys())
        ]


    @http.route('/reports/all', type='http', auth="user", website=True)
    @cached(cache)
    def reports_all(self, **kw):
        """Page showing reports on the activity of the website."""
        time1 = time.time()

        filters = [
            ('is_company', '=', True),
        ]

        _logger.debug('reports users')
        env = request.env
        user_pool = env['res.users']
        partner_pool = env['res.partner']
        values = {
            'latest_refresh': '{0} (GMT)'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),

            # line chart
            'data_users': self.sort_dict(
                self.fill_dict_days(get_users_by_date(user_pool))
            ),
            'data_created_companies': self.sort_dict(
                self.fill_dict_days(
                    get_partners_by_created_date(partner_pool, filters)
                )
            ),
            'data_updated_companies': self.sort_dict(
                self.fill_dict_days(
                    get_partners_by_updated_date(partner_pool, filters)
                )
            ),

            # by country chart and spreadsheet
            'piechart_by_country': [['Name', 'Number']] + [
                # Value is a unicode which is not compatible with JS.
                [str(value[0]), value[1]]
                for value in get_companies_by_country(partner_pool, filters).items()
            ]

        }
        _logger.debug('piechart_by_country: %s', values['piechart_by_country'])
        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2 - time1) * 1000.0))
        return request.render(
            'frontend_reports.reports_line_chart_all', values
        )


def get_companies_by_country(pool, filters=None, number=10):
    """Compile the list of companies to count them by country.

    :return: dict
    """
    if not filters:
        filters = []
    by_country = defaultdict(int)
    companies = pool.search(filters)
    for partner in companies:
        by_country[partner.country_id.name] += 1

    countries = sorted(by_country.items(), key=operator.itemgetter(1))

    result = {
        name: value for name, value in countries[-number:]
    }
    result['Others'] = sum([country[1]for country in countries[:-number]])

    _logger.debug('by country: %s', result)
    sum_after_algorithm = sum([country for country in result.values()])
    _logger.debug(
        'sum after algorithm: %s (should be %s)',
        sum_after_algorithm, len(companies)
    )
    assert sum([country for country in result.values()]) == len(companies), (
        'Seems some copanies were filtered out in the algorithm'
    )
    return result


def get_users_by_date(pool, filters=None):
    """Sort user by creation dates.

    :return: dict
    """
    if not filters:
        filters = []

    by_date = defaultdict(int)
    for user in pool.search(filters):
        created_time = user.create_date
        # Admin does not have a create_date.
        if created_time:
            date_object = datetime.datetime.strptime(
                created_time, '%Y-%m-%d %H:%M:%S'
            ).date()
            if date_object >= first_day:
                # datetime pattern: 2015-04-14 15:47:03
                by_date[str(date_object)] += 1

    return by_date


def get_partners_by_created_date(pool, filters=None):
    """Sort companies by create dates.

    :return: dict
    """
    return get_partners_field(pool, 'create_date', filters=filters)


def get_partners_by_updated_date(pool, filters):
    """Sort companies by update dates.

    :return: dict
    """
    return get_partners_field(pool, 'write_date', filters=filters)


def get_partners_field(pool, date_field_name, filters=None):
    """Sort companies by a date field.

    :return: dict
    """
    if not filters:
        filters = []

    by_date = defaultdict(int)
    for partner in pool.search(filters):
        update_time = getattr(partner, date_field_name)
        if update_time:
            date_object = datetime.datetime.strptime(
                update_time, '%Y-%m-%d %H:%M:%S'
            ).date()
            if date_object >= first_day:
                # datetime pattern: 2015-04-14 15:47:03
                by_date[str(date_object)] += 1

    return by_date

