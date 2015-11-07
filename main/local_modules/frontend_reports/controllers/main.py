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
        self.user_pool = env['res.users']
        self.partner_pool = env['res.partner']

        values = {
            'data_users': self.sort_dict(
                self.fill_dict_days(self.__get_users_by_date())
            ),
            'data_created_companies': self.sort_dict(
                self.fill_dict_days(
                    self.__get_partners_by_created_date(filters)
                )
            ),
            'data_updated_companies': self.sort_dict(
                self.fill_dict_days(
                    self.__get_partners_by_updated_date(filters)
                )
            ),
            'latest_refresh': '{0} (GMT)'.format(
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ),
        }
        time2 = time.time()
        _logger.debug('function took %0.3f ms' % ((time2 - time1) * 1000.0))
        return request.render(
            'frontend_reports.reports_line_chart_all', values
        )

    def __get_users_by_date(self):
            """Sort user by creation dates.

            :return: dict
            """
            by_date = defaultdict(int)
            for user in self.user_pool.search([]):
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

    def __get_partners_by_created_date(self, filters):
        """Sort companies by create dates.

        :return: dict
        """
        return self.__get_partners_field('create_date', filters)

    def __get_partners_by_updated_date(self, filters):
        """Sort companies by update dates.

        :return: dict
        """
        return self.__get_partners_field('write_date', filters)

    def __get_partners_field(self, date_field_name, filters):
        """Sort companies by a date field.

        :return: dict
        """
        by_date = defaultdict(int)
        for partner in self.partner_pool.search(filters):
            update_time = getattr(partner, date_field_name)
            if update_time:
                date_object = datetime.datetime.strptime(
                    update_time, '%Y-%m-%d %H:%M:%S'
                ).date()
                if date_object >= first_day:
                    # datetime pattern: 2015-04-14 15:47:03
                    by_date[str(date_object)] += 1

        return by_date

