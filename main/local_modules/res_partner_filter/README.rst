Res Partner Filter
==================
This module modify ``res.partner`` to allow to search a partner by city or country.

In Odoo, a partner is a people or a company. Only the boolean ``is_company`` makes the difference between 
a company and a people.
As the website is about companies, the boolean is hidden to portal user and set to true by default.
People are created through the ``crm``.

By default, the filters for res.partner are not focusing on the location of the partner but more 
on the occupation or who is the user behind it.

The module removes the filters that are not focusing on location and create new filters like 
by city, by country, by state.
The module also enhances the main filter so the main search will take in count the name, ref and email 
as it is by default but also the country, the state and the city. This allows to make quick, 
but dirty searches. This mode should be enough for most of searches tho.


Contributors
------------
* Jordi Riera <kender.jr@gmail.com>

