import os
from bluepy.btle import Scanner

from scan import DeviceForwardingDelegate
from igrill import IGrillHandler

device_settings = {
    "d4:81:ca:03:ab:80": {
        "device": "iGrill Mini",
        "addr": "d4:81:ca:03:ab:80",
        "type": "kitchen"
    },
}

if __name__ == "__main__":
    print "Creating Scanner"
    delegate = DeviceForwardingDelegate()
    delegate.handlers.append(IGrillHandler(device_settings))

    scanner = Scanner()
    scanner.withDelegate(delegate)

    while True:
        print "Scanning..."
        scanner.scan(30)

        print "Persisting..."
        for handler in delegate.handlers:
            handler.persist_stats(persistence)
