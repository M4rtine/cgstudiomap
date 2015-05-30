# -*- python -*-
import logging

client_module = 'main'



def update_res_partner_state(session, logger):
    """Method to go throught all the partner and to move from management by
    `active` field to `state`
    """
    logger.setLevel(logging.DEBUG)
    logger.info('update_res_partner_state()')
    partner_pool = session.registry('res.partner')
    domain = ['|', ('active', '=', False), ('active', '=', True)]

    for partner_id in partner_pool.search(session.cr, session.uid, domain):
        partner = partner_pool.browse(session.cr, session.uid, partner_id)

        # Before the update, a company was considered as closed if `active`
        # was set to False. Now it depends on the state.
        if partner.is_company:
            if partner.active:
                partner.write({'state': 'open'})
            else:
                partner.write({'state': 'closed', 'active': True})


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

    # it is the first time upgrade process is used so no version is set yet.
    # Note: The version of the db is set at the end of the process.
    # We don't want to run this update twice tho.
    if session.db_version is None:
        update_res_partner_state(session, logger)
