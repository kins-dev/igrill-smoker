#!/bin/bash
true
# shellcheck disable=2086
set -$-ue${DEBUG+xv}
sudo apt-get update
sudo apt-get install -y libglib2.0-dev npm lighttpd certbot screen
sudo npm install -g tplink-smarthome-api
sudo pip3 install -r requirements.txt
# Not sure I need this still
pushd /usr/local/lib/python2.7/dist-packages/bluepy
sudo make
popd
bash get_mac.sh