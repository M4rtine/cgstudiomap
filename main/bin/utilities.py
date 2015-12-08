import glob
import logging
import os
import pprint
import sys

logger = logging.getLogger(__name__)
logging.basicConfig()


def set_sys_path():
    """Find all the packages that should be added to make the instance run
    properly.
    """
    # Root of the project
    root = os.path.dirname(os.path.dirname(__file__))

    # where python eggs are
    eggs = glob.glob(os.path.join(root, 'eggs', '*'))

    # where 3rd party modules are
    parts = glob.glob(os.path.join(root, 'parts', '*'))
    # need to add special folders for odoo
    parts.extend(
        [
            os.path.join(root, 'parts', 'odoo', 'openerp', 'addons'),
            os.path.join(root, 'parts', 'odoo', 'addons'),
        ]
    )

    # where local modules are.
    main = glob.glob(os.path.join(root, 'local_modules'))

    paths = eggs + parts + main

    sys.path.extend(paths)
    logger.debug('paths: %s', pprint.pformat(sys.path))
