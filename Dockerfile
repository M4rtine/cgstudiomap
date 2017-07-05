###################################
## IMAGE SETUP
###################################
FROM ubuntu:15
MAINTAINER cgstudiomap <cgstudiomap@gmail.com>
ENV PROJECT_HOME=/opt/cgstudiomap
ENV LOCAL_SHARE=/home/cgstudiomap/.local/share/Odoo/
#VOLUME ["/opt/cgstudiomap/", "/home/cgstudiomap/.local/share/Odoo/"]

# To avoid errors like debconf: unable to initialize frontend: Dialog
# See http://askubuntu.com/questions/506158/unable-to-initialize-frontend-dialog-when-using-ssh
ENV DEBIAN_FRONTEND=noninteractive

ADD requirements_apt.txt /

RUN apt-get update && \
    apt-get upgrade -yq && \
    apt-get install -y $(cat /requirements_apt.txt)

ADD requirements_pip.txt /

RUN pip install pip --upgrade && \
    pip install -r requirements_pip.txt

RUN useradd -m -s /bin/bash cgstudiomap
ADD main $PROJECT_HOME
RUN chown -R cgstudiomap:cgstudiomap $PROJECT_HOME
RUN mkdir -p $LOCAL_SHARE && chown -R cgstudiomap:cgstudiomap /home/cgstudiomap
EXPOSE 8069 8072
USER cgstudiomap

WORKDIR $PROJECT_HOME