# Starting with Raspberry Pi Stretch

You must have a Raspberry Pi 3 (only tested on B)

This assumes you've done the basic setup of network and updated the system.  Rember, you probably want to enable ssh access

Also you must have your iGrill V2 ready to complete the installation and setup

Either download and run go.sh or run the following commands

```bash
git clone https://git.kins.dev/igrill-smoker
cd igrill-smoker
bash run-install.sh
```

After starting the run-install.sh script, you should turn on your iGrill v2.  Installation shouldn't take long and the device is needed for setup.

Secure your instance of lighttpd using the instructions at <https://github.com/galeone/letsencrypt-lighttpd/blob/master/renew.sh>

Find your Kasa IP address

```bash
tplink-smarthome-api search
```

Update data.sh with that IP address

Link the data.csv to the correct directory

```bash
ln -s /tmp/data.csv /var/www/html/.
```

Edit the chart.html file to suit your needs and copy it to your /var/www/html directory