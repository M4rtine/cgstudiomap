import logging

from openerp.tests import common
from openerp.exceptions import except_orm
_logger = logging.getLogger(__name__)


class TestResPartner(common.TransactionCase):
    """Use case of creation of a partner."""
    def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner_pool = self.env['res.partner']
        self.partner_pool.__dryRun__ = True
        self.country_pool = self.env['res.country']
        self.canada = self.country_pool.browse(39)

    def test_create_byPublicUser(self):
        """Check a public user can't create a res.partner."""
        public_user = self.ref('base.public_user')
        with self.assertRaises(except_orm):
            # sudo() allows to act as another user.
            self.partner_pool.sudo(public_user).create({
                'name': 'tpartner',
                'street': '8017 Avenue Chateaubriand',
                'zip': 'H2R 2M7',
                'city': 'Montreal',
                'state_id': 1,
                'country_id': self.canada.id,
            })
