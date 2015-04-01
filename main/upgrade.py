# -*- python -*-

client_module = '__main__'


def run(session, logger):
    """Update all modules."""
    if session.is_initialization:
        logger.info("Usage of upgrade script for initialization detected. "
                    "Installing Client Module...")
        session.install_modules([client_module])
        return

    logger.info("Updating module list")
    session.update_modules_list()

    logger.info("Default upgrade procedure : updating all modules.")
    session.update_modules(['all'])
