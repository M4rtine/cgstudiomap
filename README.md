[![Build Status](https://travis-ci.org/foutoucour/cgstudiomap.svg?branch=develop)](https://travis-ci.org/foutoucour/cgstudiomap)
[![Coverage Status](https://coveralls.io/repos/foutoucour/cgstudiomap/badge.png?branch=develop)](https://coveralls.io/r/foutoucour/cgstudiomap?branch=develop)


# cgstudiomap



### Requirements

#### Install dependencies 

  sudo apt-get install git python-pip postgresql python-dev postgresql-server-dev-9.3 libldap2-dev \
    libsasl2-dev libjpeg-dev libxml2-dev libxslt1-dev zlib1g-dev postfix libgeoip-dev

#### Add a PostgreSQL user

  sudo -s
  su - postgres -c "createuser --superuser --createdb --username postgres --no-createrole -w odoo8dev"

#### and change its password 

  su - postgres -c "psql -c \"ALTER USER odoo8dev WITH PASSWORD 'odoo'\""
  exit

##### this guide might help you to understand better the configuration of your server

  http://www.theopensourcerer.com/2014/09/how-to-install-openerp-odoo-8-on-ubuntu-server-14-04-lts/

#### In order to user geolocation with postgres, postgis is required

  sudo apt-get install postgis

##### Issues can be experienced with installing postgis, this post mught help to fix it:
(for ubuntu 14.04, you might have to use a different version of postgres tho)
  http://stackoverflow.com/questions/18696078/postgresql-error-when-trying-to-create-an-extension

  * Extracted from the post
  
  echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" | sudo tee /etc/apt/sources.list.d/postgis.list

  wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  
  sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 postgresql-client-9.3
  
  sudo -u postgres psql -c 'create extension postgis;'echo "deb http://apt.postgresql.org/pub/repos/apt/ trusty-pgdg main" | sudo tee /etc/apt/sources.list.d/postgis.list
  
  wget --quiet -O - http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc | sudo apt-key add -
  sudo apt-get update
  
  sudo apt-get install postgresql-9.3 postgresql-9.3-postgis-2.1 postgresql-client-9.3
  
  sudo -u postgres psql -c 'create extension postgis;'

#### Shapely and geojson are required by geoengine

  pip install shapely geojson


### Installation steps

* build of the environment

  ./install.sh

* set up the database

  createdb {database_name}

* set up the database

  ./upgrade.py -d {database_name}

* Start Odoo

  ./bin/start_odoo.sh -d {database_name}

* and connect to http://localhost:8069

