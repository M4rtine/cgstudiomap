#! /usr/bin/env python2
"""
This script is a wrapper to buildout to standardize the freeze process.

Using this script the frozen configuration file will have the name of
what install.sh, deploy.sh and upgrade.sh wait for.

A symlink to this script is created to suit the current standard as
all other install/deploy scripts are in bash.
"""

import os
import logging
_logger = logging.getLogger(__name__)
import zc.buildout.buildout


def freeze_to(buildout_section='odoo', target_file='frozen.cfg'):
    """Wrapper to buildout to freeze the buildout configuration to a target
    file.

    :param buildout_section: name of the buildoug section to target
    :param target_file: name of the file the frozen configuration is saved in.
        Note that the file will be save in /tools folder.
    :return: buildout return code:
        0 if everything ran right
        1 if (tested cases):
         - The referenced section was not defined.
         - clean_files failed (ie: syntax error)

    """
    current_folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(current_folder, 'buildout.cfg')
    target_path = os.path.join(current_folder, target_file)

    # For this process, the .installed.cfg is not usefull and even might
    # break the process.
    # It is safer to remove it as it will be regenerated during the
    # process anyway.
    installed_path = os.path.join(current_folder, '.installed.cfg')

    if os.path.exists(installed_path):
        os.remove(installed_path)

    try:
        zc.buildout.buildout.main(
            args=[
                '-c',
                config_file,
                'install',
                'clean_files',
            ]
        )
        _logger.info('Freeze of SHA and Eggs into {}'.format(target_path))
        returncode = zc.buildout.buildout.main(
            args=[
                '-o',  # Offline
                '{}:freeze-to={}'.format(buildout_section, target_path)
            ]
        )
        _logger.debug('returncode: {}'.format(returncode))
        # returncode is none if everything ran well,
        # it is then interpreted as 0 by the shell.
        return returncode

    # Extension of OSError message to add some guides to the user.
    # We might have some other
    except OSError as e:
        msg = '{}. Please try to run install script to fix the issue.'
        raise OSError(msg.format(e))


if __name__ == '__main__':
    exit(freeze_to())
