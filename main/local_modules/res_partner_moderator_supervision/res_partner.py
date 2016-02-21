# -*- encoding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
#    This module copyright (C)  cgstudiomap <cgstudiomap@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging

from slack_log_handler import SlackLogHandler

from openerp import models, api

_logger = logging.getLogger(__name__)

WEBHOOK_URL = 'https://hooks.slack.com/services/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'  # noqa
# WEBHOOK for tests
# WEBHOOK_URL = 'https://hooks.slack.com/services/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'  # noqa


def get_slack_logger(name, hook):
    """Build a `logging.logger` instance with a special handler that will
    send a notification to cgstudiomap slack.

    :param str name: name of the logger.
    :param str hook: url of the hook to use to send the notification.

    :return: logging.logger instance.
    """
    slack_handler = SlackLogHandler(hook, username='Jazz')
    slack_handler.formatter = logging.Formatter(
        "%(asctime)s GMT - %(message)s", "%Y-%m-%d %H:%M"
    )
    slack_handler.setLevel(logging.INFO)
    slack_handler.EMOJIS[logging.INFO] = ':jazz:'
    slack_handler.EMOJIS[logging.NOTSET] = ':jazz:'
    slack_handler.EMOJIS[logging.WARNING] = ':jazz:'
    slack_handler.EMOJIS[logging.ERROR] = ':jazz:'
    slack_logger = logging.getLogger(name)
    slack_logger.addHandler(slack_handler)
    return slack_logger


_slack_logger = get_slack_logger(__name__, WEBHOOK_URL)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def do_notification(self, user):
        """Check if the update of the partner should be notified.
        Notifications are only for companies and if update is done by a user
        not member of group_archetype_contributor.

        :param record user: user that did the update.
        :return: boolean, True if the notfication should be done
        """
        ir_model_data = self.env['ir.model.data']
        contributor_group = ir_model_data.xmlid_to_object(
            'res_group_archetype.group_archetype_contributor'
        )
        ret = self.is_company and contributor_group not in user.groups_id
        _logger.debug('Do notification? %s', ret)
        return ret

    @api.multi
    def write(self, vals):
        """Overcharge to add notification to slack."""
        ret = super(ResPartner, self).write(vals)
        user = self.env['res.users'].browse(self._uid)

        if self.do_notification(user):
            message = ''.join([
                '<http://www.cgstudiomap.org{0.partner_url}|{0.name}> '
                '(id: {0.id}) has been *updated*. ',
                'Update done by {1.login} (id: {1.id}).'
            ])
            _slack_logger.info(message.format(self, user))

        return ret

    @api.model
    def create(self, vals):
        """Overcharge to add notification to slack."""
        ret = super(ResPartner, self).create(vals)
        user = self.env['res.users'].browse(self._uid)
        if ret.do_notification(user):
            message = '. '.join([
                'A new company has been *added*: '
                '<http://www.cgstudiomap.org{0.partner_url}|{0.name}> '
                '(id: {0.id}). ',
                'Update done by {1.login} (id: {1.id}).'
            ])

            _slack_logger.info(message.format(ret, user))

        return ret
