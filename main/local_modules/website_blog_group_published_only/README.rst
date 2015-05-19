Website Blog Group Published Only
=================================

Due to current setup, a member of portal group can't write a post for blogs.
Te issues comes from a rule that is set to portal group and public group which
restrict members to see only published blog post. But a new blog post is by default
not published.

This module fixes the case with moving the rule to a a new group: see_published_post_only.
Public and portal group inherit by default from this new group, so the default behaviour
is preserved.

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>
