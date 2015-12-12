# -*- coding: utf-8 -*-
import logging

from cachetools import cached, TTLCache
from openerp.addons.web import http
from openerp.addons.website.controllers.main import Website

from openerp.http import request

_logger = logging.getLogger(__name__)



class Base(Website):
    """Representation of the homepage of the website."""

    def render(self, template, values=None):
        """Update of render to add values that are required to render
        template in base.

        Adds:
        * directory_menu
        * shop_menu
        * about_menu

        :param str template: name of a template
        :param dict values: value to render the template
        :return: request.render return
        """
        if values is None:
            values = {}
        # menu_pool = request.env['website.menu']
        values.update({
            'directory_menu': '/web/',
            'shop_menu': '/shop',
            'about_menu': '/page/website.contactus'
        })
        return request.render(template, values)
