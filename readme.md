# Starting with Raspberry Pi Stretch

## These instructions are not complete yet

You must have a Raspberry Pi 3 (only tested on B)

This assumes you've done the basic setup of network and updated the system

Also you must have your iGrill V2 ready to complete the installation and setup

Either download and run go.sh or run the following commands

```bash
git clone https://git.kins.dev/igrill-smoker
cd igrill-smoker
bash run-install.sh
```

Secure your instance using the instructions at <https://github.com/galeone/letsencrypt-lighttpd/blob/master/renew.sh>

After starting the run-install.sh script, you should turn on your iGrill v2.  Installation shouldn't take long and the device is needed for setup.

Find your Kasa IP address

Update data.sh with that IP address

Exit the desktop (run at the command line)

Link the data.csv to the correct directory

```bash
ln -s /tmp/data.csv /var/www/html/.
```

Edit the chart.html file to suit your needs and copy it to your /var/www/html directory