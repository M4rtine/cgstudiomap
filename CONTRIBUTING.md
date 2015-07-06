### Module version

When editing modules in `local_modules`, change the version of each update modules to the number of the Pull Request.
Version of a module can be found in the file `__openerp.py__`

### Release version

When a module is released, meaning merged into `master`, several steps are needed to be done:
* create a tag `PR` followed by the number of the Pull Request.
* Update the version of the database in the VERSION.txt
