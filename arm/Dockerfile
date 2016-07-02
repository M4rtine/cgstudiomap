###################################
## IMAGE SETUP
###################################
FROM ioft/armhf-ubuntu:15.10
MAINTAINER cgstudiomap <cgstudiomap@gmail.com>
ENV PROJECT_HOME=/opt/cgstudiomap
ENV LOCAL_SHARE=/home/cgstudiomap/.local/share/Odoo/
VOLUME [ $PROJECT_HOME, LOCAL_SHARE]

# To avoid errors like debconf: unable to initialize frontend: Dialog
# See http://askubuntu.com/questions/506158/unable-to-initialize-frontend-dialog-when-using-ssh
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -yq && \
	apt-get install -y apt-utils && \
	apt-get install -y git && \
	apt-get install -y libfreetype6 && \
	apt-get install -y libfreetype6-dev && \
	apt-get install -y libgeos-dev && \
	apt-get install -y libjpeg-dev && \
	apt-get install -y libjpeg8-dev && \
	apt-get install -y libldap2-dev && \
	apt-get install -y libsasl2-dev && \
	apt-get install -y libssl-dev && \
	apt-get install -y libxml2-dev && \
	apt-get install -y libxslt1-dev && \
	apt-get install -y postgresql-server-dev-9.4 && \
	apt-get install -y postgresql-client-9.4 && \
	apt-get install -y python-pychart && \
	apt-get install -y python-dev && \
	apt-get install -y python-pip && \
	apt-get install -y python2.7 && \
	apt-get install -y zlib1g-dev && \
	apt-get clean

RUN rm /usr/bin/python && \
    ln -s /usr/bin/python2.7 /usr/bin/python

ADD requirements_pip.txt /
ADD ./main/parts/odoo/requirements.txt /

RUN pip install pip --upgrade
# the second round of pips needs to happen after the upgrade of pip.
RUN pip install zc.buildout && \
    pip install -r requirements.txt --no-cache-dir && \
    pip install -r requirements_pip.txt --no-cache-dir

RUN useradd -m -s /bin/bash cgstudiomap
EXPOSE 8069 8072

USER cgstudiomap
WORKDIR $PROJECT_HOME
