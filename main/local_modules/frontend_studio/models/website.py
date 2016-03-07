# -*- coding: utf-8 -*-
"""Improvement of website model."""
import logging

from openerp import models, fields
from openerp.osv import osv
_logger = logging.getLogger(__name__)


class WebsiteStudioEditionText(models.Model):
    """Add fields to website that will be displayed in the edition of
    a studio page.
    """
    _inherit = 'website'

    studio_common_details= fields.Text(
        'Common Tab Details', help='Text displayed at the Common tab'
    )
    studio_location_details= fields.Text(
        'Location Tab Details', help='Text displayed at the Location tab'
    )
    studio_links_details= fields.Text(
        'Links Tab Details', help='Text displayed at the Links tab'
    )
    studio_socials_details= fields.Text(
        'Socials Tab Details', help='Text displayed at the Socials tab'
    )
    studio_calls_details= fields.Text(
        'Calls Tab Details', help='Text displayed at the Calls tab'
    )
    studio_industries_details= fields.Text(
        'Industries Tab Details', help='Text displayed at the Industries tab'
    )


class WebsiteConfigSettings(osv.osv_memory):
    """Link of website new field into config settings."""
    _inherit = 'website.config.settings'

    studio_common_details = fields.Text(
        string='Common Tab Details', store=True,
        related='website_id.studio_common_details'
    )
    studio_location_details = fields.Text(
        string='Location Tab Details', store=True,
        related='website_id.studio_location_details'
    )
    studio_links_details = fields.Text(
        string='Links Tab Details', store=True,
        related='website_id.studio_links_details'
    )
    studio_socials_details = fields.Text(
        string='Socials Tab Details', store=True,
        related='website_id.studio_socials_details'
    )
    studio_calls_details = fields.Text(
        string='Calls Tab Details', store=True,
        related='website_id.studio_calls_details'
    )
    studio_industries_details = fields.Text(
        string='Industries Tab Details', store=True,
        related='website_id.studio_industries_details'
    )
