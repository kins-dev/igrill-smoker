# Starting with Raspberry Pi Stretch

You must have:

* Raspberry Pi 3
* TP-Link Kasa
* iGrill2 or iGrill3

Optional items:

* LEDs with current limiting resistors
* Speaker with 3.5 mm stereo jack input

*Note: This has been tested using a Raspberry Pi B 3 with Raspian Strecth.  Your milage may vary.*

This guide assumes you've done the basic setup of network and updated the system on your Raspberry Pi.  Rember, you probably want to enable ssh access.  You must have your iGrill ready to complete the installation and setup.  This does require python 3 to be installed.

## Installation

Either download and run ```go.sh``` or run the following commands:

```bash
git clone https://git.kins.dev/igrill-smoker
cd igrill-smoker
bash run-install.sh
```

After starting the ```run-install.sh``` script, you should turn on your iGrill v2.  Installation shouldn't take long and the device is needed for setup.

## Setup

Find your Kasa IP address:

```bash
tplink-smarthome-api search
```

Copy ```user-config.example.sh``` to ```user-config.sh```.  Update ```user-config.sh``` with that IP address.

Edit the chart.html file to suit your needs and copy it to your ```/var/www/html``` directory.

## Running

Start a smoking session by running:

```bash
./startup.sh
```

## Lighttpd Setup

Secure your instance of lighttpd using the instructions at <https://github.com/galeone/letsencrypt-lighttpd/blob/master/renew.sh>.  You may want a wildcard certificate and you can find instructions via <https://asknetsec.com/generate-lets-encrypt-free-wildcard-certificate-using-certbot-ubuntu-16-04/>.  Check your SSL setup via <https://www.ssllabs.com/ssltest/index.html>.

Also, it may be a good idea to setup lighttpd such that ```*.csv```/```*.json``` is not cached.  Here's an example lighttpd config file:

```ruby
server.modules = (
        "mod_expire",
        "mod_access",
        "mod_alias",
        "mod_compress",
        "mod_redirect",
        "mod_setenv",
        "mod_dirlisting",
)

server.document-root                            = "/var/www/html"
server.upload-dirs                              = ( "/var/cache/lighttpd/uploads" )
server.errorlog                                 = "/var/log/lighttpd/error.log"
server.pid-file                                 = "/var/run/lighttpd.pid"
server.username                                 = "www-data"
server.groupname                                = "www-data"
server.port                                     = 80

index-file.names                                = ( "index.php", "index.html", "index.lighttpd.html" )
url.access-deny                                 = ( "~", ".inc" )
static-file.exclude-extensions                  = ( ".php", ".pl", ".fcgi" )

compress.cache-dir                              = "/var/cache/lighttpd/compress/"
compress.filetype                               = ( "application/javascript", "text/css", "text/html", "text/plain" )

# default listening port for IPv6 falls back to the IPv4 port
## Use ipv6 if available
#include_shell "/usr/share/lighttpd/use-ipv6.pl " + server.port
include_shell "/usr/share/lighttpd/create-mime.assign.pl"
include_shell "/usr/share/lighttpd/include-conf-enabled.pl"

# SSL Config
$SERVER["socket"] == ":443" {
        protocol                                = "https://"
        ssl.engine                              = "enable"
        ssl.ca-file                             = "/etc/lighttpd/fullchain.pem"
        ssl.pemfile                             = "/etc/lighttpd/wildcard.cert.pem"

        setenv.add-environment  = (
                "HTTPS"                         => "on"
        )

        setenv.add-response-header  = (
                # Allow cross domain accesss
                # Safari requires *
                "Access-Control-Allow-Origin"   => "*",

                # Used to identify the server based on headers
                "Server"                        => "Server name",

                # Set timeout for ssl access
                "Strict-Transport-Security"     => "max-age=15768000;"
        )

        # Mitigate BEAST attack:
        #
        # A stricter base cipher suite. For details see:
        # http://blog.ivanristic.com/2011/10/mitigating-the-beast-attack-on-tls.html
        ssl.cipher-list                         = "ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256"

        # Make the server prefer the order of the server side cipher suite instead of the client suite.
        # This is necessary to mitigate the BEAST attack (unless you disable all non RC4 algorithms).
        # This option is enabled by default, but only used if ssl.cipher-list is set.
        ssl.honor-cipher-order                  = "enable"

        # Mitigate CVE-2009-3555 by disabling client triggered renegotation
        # This is enabled by default.
        ssl.disable-client-renegotiation        = "enable"
        ssl.ec-curve                            = "secp384r1"
        ssl.use-compression                     = "disable"

        # Disable SSLv2 because is insecure
        ssl.use-sslv2                           = "disable"

        # Disable SSLv3 (can break compatibility with some old browser) /cares
        ssl.use-sslv3                           = "disable"
}

# Prevent caching of json/csv files
$HTTP["url"] =~ "/.*\.(json|csv)$" {
        expire.url = (
                ""                              => "access 0 seconds",
        )
}
```