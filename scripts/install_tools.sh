#!/bin/bash
sudo apt-get install nodejs-legacy
sudo apt-get install npm
sudo npm install -g azure-cli
sudo pip install paramiko PyYAML jinja2 httplib2 ansible
sudo dpkg -i vagrant_1.8.1_x86_64.deb
vagrant plugin install vagrant-azure
