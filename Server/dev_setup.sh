#!/bin/bash

sudo -E apt-get -y install python-dev
sudo -E apt-get -y install python-pip
sudo -E pip install virtualenv
virtualenv --no-site-packages sc

source sc/bin/activate
unset PYTHONPATH
pip install --upgrade pip
pip install -r requirements.txt
deactivate

sudo -E apt-get install unzip

wget -N http://chromedriver.storage.googleapis.com/2.10/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver

sudo mv -f chromedriver /usr/local/share/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
rm chromedriver_linux64.zip

sudo -E apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo -E apt-get update
sudo -E apt-get install mongodb-10gen=2.4.14
echo "mongodb-10gen hold" | sudo dpkg --set-selections
