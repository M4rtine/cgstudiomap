Frontend Studio
===============
Module dedicated to the generation of the studio that display data of studios.
Three modes for the page:
* View
* Edit
* Create

It should be composed by
* templates
* models
* controllers

needed by the page.

Urls from the module:
* create: GET /directory/company/create
* create_save: POST /directory/company/create/process
* view: GET /directory/company/{slug(res.partner)}
* edit: GET /directory/company/{slug(res.partner)}/edit
* save: POST /directory/company/{slug(res.partner)}/save

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>
* David Mazeau <d.mazeau@gmail.com>
