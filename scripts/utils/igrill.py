import bluepy.btle as btle
import logging
import struct
import configparser
import binascii
import sys

class UUIDS:
    FIRMWARE_VERSION   = btle.UUID("64ac0001-4a4b-4b58-9f37-94d3c52ffdf7")

    BATTERY_LEVEL      = btle.UUID("00002A19-0000-1000-8000-00805F9B34FB")

    APP_CHALLENGE      = btle.UUID("64AC0002-4A4B-4B58-9F37-94D3C52FFDF7")
    DEVICE_CHALLENGE   = btle.UUID("64AC0003-4A4B-4B58-9F37-94D3C52FFDF7")
    DEVICE_RESPONSE    = btle.UUID("64AC0004-4A4B-4B58-9F37-94D3C52FFDF7")

    CONFIG             = btle.UUID("06ef0002-2e06-4b79-9e33-fce2c42805ec")
    PROBE1_TEMPERATURE = btle.UUID("06ef0002-2e06-4b79-9e33-fce2c42805ec")
    PROBE1_THRESHOLD   = btle.UUID("06ef0003-2e06-4b79-9e33-fce2c42805ec")
    PROBE2_TEMPERATURE = btle.UUID("06ef0004-2e06-4b79-9e33-fce2c42805ec")
    PROBE2_THRESHOLD   = btle.UUID("06ef0005-2e06-4b79-9e33-fce2c42805ec")
    PROBE3_TEMPERATURE = btle.UUID("06ef0006-2e06-4b79-9e33-fce2c42805ec")
    PROBE3_THRESHOLD   = btle.UUID("06ef0007-2e06-4b79-9e33-fce2c42805ec")
    PROBE4_TEMPERATURE = btle.UUID("06ef0008-2e06-4b79-9e33-fce2c42805ec")
    PROBE4_THRESHOLD   = btle.UUID("06ef0009-2e06-4b79-9e33-fce2c42805ec")
    MAX_PROBE_COUNT    = 4

class IDevicePeripheral(btle.Peripheral):
    encryption_key = None
    probe_count = 0

    def __init__(self, address):
        """
        Connects to the device given by address performing necessary authentication
        """
        btle.Peripheral.__init__(self, address)

        # iDevice devices require bonding. I don't think this will give us bonding
        # if no bonding exists, so please use bluetoothctl to create a bond first
        self.setSecurityLevel("medium")

        # authenticate with iDevices custom challenge/response protocol
        if not self.Authenticate():
            raise RuntimeError("Unable to authenticate with device")

        self.temps = [-2000] * UUIDS.MAX_PROBE_COUNT

        # Setup battery which is the same regardless of device
        self.battery_char = self.getCharacteristics(uuid=UUIDS.BATTERY_LEVEL)[0]

        self.temp_chars = {}
        self.threshold_chars = {}

        for probe_num in range(1, self.probe_count + 1):
            temp_char_name = 'PROBE{}_TEMPERATURE'.format(probe_num)
            temp_char = self.getCharacteristics(uuid=getattr(UUIDS, temp_char_name))[0]
            threshold_char_name = 'PROBE{}_THRESHOLD'.format(probe_num)
            threshold_char = self.getCharacteristics(uuid=getattr(UUIDS, threshold_char_name))[0]
            self.temp_chars[probe_num] = temp_char
            self.threshold_chars[probe_num] = threshold_char

    def ReadTemperature(self):
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'/../config/tempdata.ini')

        temps = {}
        for probe_num, temp_char in list(self.temp_chars.items()):
            temps[probe_num] = struct.unpack("<h",temp_char.read()[:2])[0]
            self.threshold_chars[probe_num].write(struct.pack("<hh",
                int(config['Probe{0}'.format(probe_num)]['LOW_TEMP']),
                int(config['Probe{0}'.format(probe_num)]['HIGH_TEMP'])))
        return temps

    def Authenticate(self):
        """
        Performs iDevices challenge/response handshake. Returns if handshake succeeded
        Works for all devices using this handshake, no key required
        """
        logging.debug("Authenticating...")

        # send app challenge (16 bytes) (must be wrapped in a bytearray)
        challenge = bytearray([0] * 16)
        logging.debug("Sending key of all 0's")
        self.getCharacteristics(uuid=UUIDS.APP_CHALLENGE)[0].write(challenge, True)

        """
        Normally we'd have to perform some crypto operations:
            Write a challenge (in this case 16 bytes of 0)
            Read the value
            Decrypt w/ the key
            Check the first 8 bytes match our challenge
            Set the first 8 bytes 0
            Encrypt with the key
            Send back the new value
        
        But wait!  Our first 8 bytes are already 0.  That means we don't need the key.
        We just hand back the same encypted value we get and we're good.
        """
        encrypted_device_challenge = self.getCharacteristics(uuid=UUIDS.DEVICE_CHALLENGE)[0].read()
        logging.debug("encrypted device challenge:{0}".format(binascii.hexlify(encrypted_device_challenge)))
        self.getCharacteristics(uuid=UUIDS.DEVICE_RESPONSE)[0].write(encrypted_device_challenge, True)

        logging.debug("Authenticated")

        return True

    def ReadBattery(self):
        return int(ord(self.battery_char.read()))

class IGrillMiniPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the iGrill Mini
    """
    probe_count = 1

class IGrillPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the iGrill2/iGrill3
    """
    probe_count = 4
