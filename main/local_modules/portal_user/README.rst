Portal User
===========
The module gathers all the settings for the portal user.

Quoted from odoo portal module:
  A portal defines a specific user menu and access rights for its members. This
  menu can be seen by portal members, public users and any other user that
  have the access to technical features (e.g. the administrator).
  Also, each portal member is linked to a specific partner.
  
A portal user is any user that aim to search for companies or manage their job hunting.
In that sense, the adminstrator won't be a portal user as its aim is to manage the website.

Because of the default configuration, the portal user has access to several menu 
that are not usefull for the purpose of the project. It is not supposed to manage sale.order
or message (yet). The module moves the unwanted menu in settings>old portal menus (only accessible by admin)

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

