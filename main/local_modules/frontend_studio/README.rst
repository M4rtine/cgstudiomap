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


Additionally, fields are added to website to display text to the page of
edition of a studio.
The fields can be edited in website settings in settings tabs.
The aim of these fields is to be able to update these fields without to
have to involve developer but also that will promote these area to potential
advertising, teasing and other communication the team would like to do.

Contributors
------------
* Jordi Riera <kender.jr@gmail.com>
* David Mazeau <d.mazeau@gmail.com>
