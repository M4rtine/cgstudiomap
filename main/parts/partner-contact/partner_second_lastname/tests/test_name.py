# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U.

from openerp.tests.common import TransactionCase
from openerp.addons.partner_firstname.tests.base import MailInstalled


class CompanyCase(TransactionCase):
    """Test ``res.partner`` when it is a company."""
    def tearDown(self):
        try:
            new = self.env["res.partner"].create({
                "is_company": True,
                "name": self.name,
            })

            # Name should be cleaned of unneeded whitespace
            clean_name = u" ".join(self.name.split(None))

            # Check it's saved OK
            self.assertEqual(
                new.name,
                clean_name,
                "Saved company name is wrong.")

            # Check it's saved in the lastname
            self.assertEqual(
                new.lastname,
                clean_name,
                "Company name should be saved in the lastname field.")

            # Check that other fields are empty
            self.assertEqual(
                new.firstname,
                False,
                "Company first name must always be empty.")
            self.assertEqual(
                new.lastname2,
                False,
                "Company last name 2 must always be empty.")

        finally:
            super(CompanyCase, self).tearDown()

    def test_long_name(self):
        """Create a company with a long name."""
        self.name = u"Söme very lóng nâme"

    def test_short_name(self):
        """Create a company with a short name."""
        self.name = u"Shoŕt"

    def test_whitespace_before(self):
        """Create a company with name prefixed with whitespace."""
        self.name = u"  Wĥitespace befòre"

    def test_whitespace_after(self):
        """Create a company with name suffixed with whitespace."""
        self.name = u"Whitespâce aftér   "

    def test_whitespace_inside(self):
        """Create a company with whitespace inside the name."""
        self.name = u"Whitespacé   ïnside"

    def test_whitespace_everywhere(self):
        """Create a company with whitespace everywhere in the name."""
        self.name = u"  A  lot  öf    whitespace   "


class PersonCase(TransactionCase):
    """Test ``res.partner`` when it is a person."""
    model = "res.partner"
    context = dict()

    def setUp(self):
        super(PersonCase, self).setUp()

        self.firstname = u"Fírstname"
        self.lastname = u"Làstname1"
        self.lastname2 = u"Lâstname2"
        self.template = u"%(last1)s %(last2)s, %(first)s"

    def tearDown(self):
        try:
            new = (self.env[self.model].with_context(self.context)
                   .create(self.params))

            # Check that each individual field matches
            self.assertEqual(
                self.firstname,
                new.firstname,
                "First name saved badly.")
            self.assertEqual(
                self.lastname,
                new.lastname,
                "Last name 1 saved badly.")
            self.assertEqual(
                self.lastname2,
                new.lastname2,
                "Last name 2 saved badly.")

            # Check that name gets saved fine
            self.assertEqual(
                self.template % ({"last1": self.lastname,
                                  "last2": self.lastname2,
                                  "first": self.firstname}),
                new.name,
                "Name saved badly.")

        finally:
            super(PersonCase, self).tearDown()

    def test_firstname_first(self):
        """Create a person setting his first name first."""
        self.params = {
            "is_company": False,
            "name": "%s %s %s" % (self.firstname,
                                  self.lastname,
                                  self.lastname2),
        }

    def test_firstname_last(self):
        """Create a persong setting his first name last."""
        self.params = {
            "is_company": False,
            "name": "%s %s, %s" % (self.lastname,
                                   self.lastname2,
                                   self.firstname),
        }

    def test_firstname_only(self):
        """Create a persong setting his first name only."""
        self.lastname = self.lastname2 = False
        self.template = "%(first)s"
        self.params = {
            "is_company": False,
            "name": self.firstname,
        }

    def test_firstname_lastname_only(self):
        """Create a persong setting his first name and last name 1 only."""
        self.lastname2 = False
        self.template = "%(last1)s, %(first)s"
        self.params = {
            "is_company": False,
            "name": "%s %s" % (self.firstname, self.lastname),
        }

    def test_lastname_firstname_only(self):
        """Create a persong setting his last name 1 and first name only."""
        self.lastname2 = False
        self.template = "%(last1)s, %(first)s"
        self.params = {
            "is_company": False,
            "name": "%s, %s" % (self.lastname, self.firstname),
        }

    def test_separately(self):
        """Create a person setting separately all fields."""
        self.params = {
            "is_company": False,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "lastname2": self.lastname2,
        }


class UserCase(PersonCase, MailInstalled):
    """Test ``res.users``."""
    model = "res.users"
    context = {"default_login": "user@example.com"}

    def tearDown(self):
        # Skip if ``mail`` is installed
        if not self.mail_installed():
            super(UserCase, self).tearDown()
