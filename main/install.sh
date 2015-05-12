#!/bin/bash

PROJECT_HOME=`pwd`
# Force to use the frozen configuration.
# BUILDOUT_CFG=$PROJECT_HOME/frozen.cfg
BUILDOUT_CFG=$PROJECT_HOME/frozen.cfg
PARTS="reset_repos odoo"
#PARTS="odoo"

# Prepare buildout environment
/usr/bin/env python2 $PROJECT_HOME/bootstrap.py -c $BUILDOUT_CFG

# Prepare Odoo environment
$PROJECT_HOME/bin/buildout -c $BUILDOUT_CFG install $PARTS

# Create .openerp_serverrc file
echo -n "Creating ~/.openerp_serverrc file... "
if [ ! -e ~/.openerp_serverrc ]
then
    cat>~/.openerp_serverrc<<EOF
[options]
admin_passwd = admin
db_password = odoo
EOF
    echo "OK"
else
    echo "File exists!"
fi

# Make sure there's no admin_passwd or db_password in the generated config file
sed -i '/admin_passwd/d' etc/odoo.cfg
sed -i '/db_password/d' etc/odoo.cfg

# improve python_dev
patch -d $PROJECT_HOME -p 0 -i $PROJECT_HOME/patches/python_odoo.patch

exit 0

# EOF
