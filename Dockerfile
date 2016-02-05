FROM ubuntu:latest

#Autor
MAINTAINER Francisco Javier Garrido Mellado <franciscojaviergarridomellado@gmail.com>

#Actualización del Sistema 
RUN sudo apt-get -y update
#Instalar MySQL
RUN sudo apt-get -y install python-mysqldb
RUN sudo apt-get -y install mysql-server
RUN sudo service mysql start
RUN mysqladmin  -h localhost -u root  create vagrant
#Descarga de la aplicación
RUN sudo apt-get install -y git
RUN sudo git clone https://github.com/javiergarridomellado/DAI.git

# Instalación de Python y PostgreSQL
RUN sudo apt-get install -y python-setuptools
RUN sudo apt-get -y install python-dev
RUN sudo apt-get -y install build-essential
RUN sudo apt-get -y install python-psycopg2
RUN sudo apt-get -y install libpq-dev
RUN sudo easy_install pip
RUN sudo pip install --upgrade pip

#Instalación de dependencias de la aplicacion

RUN cd DAI/ && sudo pip install -r requirements.txt

#Sincronización de la base de datos
RUN cd DAI/ && python manage.py syncdb --noinput



