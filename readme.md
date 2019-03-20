# Starting with Raspberry Pi Stretch

*These instructions are not complete yet*

This assumes you've installed the stretch desktop image on your raspberry pi.

First you need to install glib2-dev

```bash
sudo apt-get install glib2-dev
```

Then install your pip modules

```bash
sudo pip install -r requirements.txt
```

You may need to rebuild the executables for bluepy

```bash
cd /usr/local/lib/python/.../bluepy
sudo make
```

Turn on your igrill

Find the mac address

```bash
lshci lescan
```

Edit monitor_igrill.py or monitor_igrill2.py with your mac address

Install npm

Install kasa cli

Find your Kasa IP address

Update data.sh with that IP address

Exit the desktop (run at the command line)

Install lighttp

Link the data.csv to the correct directory

```bash
ln -s /tmp/data.csv /var/www/html/.
```

Edit the chart.html file to suit your needs