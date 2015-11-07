# -*- coding: utf-8 -*-
from collections import defaultdict
import datetime
import time
import logging

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website
from cachetools import cached, TTLCache


# Cache of 12hours
# The decorated method are refreshed every 12hours.
cache = TTLCache(100, 43200)

_logger = logging.getLogger(__name__)


# First day of the beta
first_day = datetime.date(2015, 07, 15)
month = str(datetime.date.today() - datetime.timedelta(days=30))
week = str(datetime.date.today() - datetime.timedelta(days=7))


class MainPage(Website):
    @staticmethod
    def fill_dict_days(by_date, first_day):
        """Fill the missing dates with 0

        :param by_date: dict
        :param first_day: the day to start
        :return: dict
        """
        today = datetime.date.today()
        first_day = datetime.datetime.strptime(first_day,
                                               '%Y-%m-%d').date()
        _logger.debug('today: %s, first day: %s', today, first_day)
        while first_day <= today:
            if str(first_day) not in by_date:
                by_date[str(first_day)] = 0
            first_day = first_day + datetime.timedelta(days=1)

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

        def get_users_by_date(day, earliest_day):
            """Sort user by each days

            :param str day: stamp for the memorized so it is done once a day.
            :param str earliest_day: the earliest day the user is created.

            :return: dict
            """
            earliest_day = datetime.datetime.strptime(earliest_day,
                                                      '%Y-%m-%d').date()
            by_date = defaultdict(int)
            for user in self.user_pool.search([]):
                created_time = user.create_date
                # Admin does not have a create_date.
                if created_time:
                    date_object = datetime.datetime.strptime(
                        created_time, '%Y-%m-%d %H:%M:%S'
                    ).date()
                    if date_object >= earliest_day:
                        # datetime pattern: 2015-04-14 15:47:03
                        by_date[str(date_object)] += 1

            return by_date
        filters = [
            ('is_company', '=', True),
        ]

        def get_partners_by_updated_date(day, earliest_day):
            """Sort user by each days

            :param str day: stamp for the memorized so it is done once a day.
            :param str earliest_day: the earliest day the user is created.

            :return: dict
            """
            earliest_day = datetime.datetime.strptime(earliest_day,
                                                      '%Y-%m-%d').date()
            by_date = defaultdict(int)
            for partner in self.partner_pool.search(filters):
                created_time = partner.write_date
                if created_time:
                    date_object = datetime.datetime.strptime(
                        created_time, '%Y-%m-%d %H:%M:%S'
                    ).date()
                    if date_object >= earliest_day:
                        # datetime pattern: 2015-04-14 15:47:03
                        by_date[str(date_object)] += 1

            return by_date

        def get_partners_by_created_date(day, earliest_day):
            """Sort user by each days

            :param str day: stamp for the memorized so it is done once a day.
            :param str earliest_day: the earliest day the user is created.

            :return: dict
            """
            earliest_day = datetime.datetime.strptime(earliest_day,
                                                      '%Y-%m-%d').date()
            by_date = defaultdict(int)
            for partner in self.partner_pool.search(filters):
                created_time = partner.create_date
                if created_time:
                    date_object = datetime.datetime.strptime(
                        created_time, '%Y-%m-%d %H:%M:%S'
                    ).date()
                    if date_object >= earliest_day:
                        # datetime pattern: 2015-04-14 15:47:03
                        by_date[str(date_object)] += 1

            return by_date

        _logger.debug('reports users')
        env = request.env
        self.user_pool = env['res.users']
        self.partner_pool = env['res.partner']
        today = datetime.date.today()
        first_day_str = str(first_day)
        by_date_users = self.fill_dict_days(
            get_users_by_date(str(today), first_day_str), first_day_str
        )

        by_date_created_companies = self.fill_dict_days(
            get_partners_by_created_date(today, first_day_str), first_day_str
        )
        by_date_updated_companies = self.fill_dict_days(
            get_partners_by_updated_date(today, first_day_str), first_day_str
        )
        values = {
            'data_users': self.sort_dict(by_date_users),
            'data_created_companies': self.sort_dict(by_date_created_companies),
            'data_updated_companies': self.sort_dict(by_date_updated_companies),
        }
        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2 - time1) * 1000.0))
        return request.render(
            'frontend_reports.reports_line_chart_all', values
        )

