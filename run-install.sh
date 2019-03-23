#!/bin/bash
set -ue
sudo apt-get update
sudo apt-get install -y libglib2.0-dev npm lighttpd certbot
sudo npm install -g tplink-smarthome-api
sudo pip install -r requirements.txt
pushd /usr/local/lib/python2.7/dist-packages/bluepy
sudo make
popd
