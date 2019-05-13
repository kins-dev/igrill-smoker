# Copyright (c) 2019:   Scott Atkins <scott@kins.dev>
#                       (https://git.kins.dev/igrill-smoker)
# License:              MIT License
#                       See the LICENSE file
import bluepy.btle as btle
import logging
import struct
import configparser
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
    m_probe_count = 0
    m_iGrillChars = {}
    m_battery_char = None
    m_temp_chars = {}
    m_threshold_chars = {}
    LOW_TEMP_KEY = "LOW_TEMP"
    HIGH_TEMP_KEY = "HIGH_TEMP"
    LOW_DEFAULT = -32768
    HIGH_DEFAULT = 32767

    def __init__(self, address):
        """
        Connects to the device given by address performing necessary authentication
        """
        btle.Peripheral.__init__(self, address)

        # iDevice devices require bonding. I don't think this will give us bonding
        # if no bonding exists, so please use bluetoothctl to create a bond first
        self.setSecurityLevel("medium")

        # save all the characteristics in a dictionary, as the iGrill will disconnect
        # if they are querried at the wrong time
        characteristics = self.getCharacteristics()
        for c in characteristics:
            self.m_iGrillChars[c.uuid] = c

        # authenticate with iDevices custom challenge/response protocol
        if not self.Authenticate():
            raise RuntimeError("Unable to authenticate with device")

        # Setup battery which is the same regardless of device
        self.m_battery_char = self.m_iGrillChars[UUIDS.BATTERY_LEVEL]

        for probe_num in range(1, self.m_probe_count + 1):
            temp_char_name = 'PROBE{}_TEMPERATURE'.format(probe_num)
            temp_char = self.m_iGrillChars[getattr(UUIDS, temp_char_name)]
            threshold_char_name = 'PROBE{}_THRESHOLD'.format(probe_num)
            threshold_char = self.m_iGrillChars[getattr(UUIDS, threshold_char_name)]
            self.m_temp_chars[probe_num] = temp_char
            self.m_threshold_chars[probe_num] = threshold_char

    def ReadTemperature(self):
        config = configparser.ConfigParser()
        # does not throw an error, just returns the empty set if the file doesn't exist
        config.read(sys.path[0]+'/py_config/threshold_config.ini')

        temps = [-2000] * UUIDS.MAX_PROBE_COUNT
        for probe_num, temp_char in list(self.m_temp_chars.items()):
            temps[probe_num - 1] = struct.unpack("<h",temp_char.read()[:2])[0]
            probe_name = 'Probe{0}'.format(probe_num)
            self.m_threshold_chars[probe_num].write(struct.pack("<hh",
                config.getint(probe_name, self.LOW_TEMP_KEY, fallback=self.LOW_DEFAULT),
                config.getint(probe_name, self.HIGH_TEMP_KEY, fallback=self.HIGH_DEFAULT)))
        return temps

    def Authenticate(self):
        """
        Performs iDevices challenge/response handshake. Returns if handshake succeeded
        Works for all devices using this handshake, no key required
        """
        logging.debug("Authenticating...")

        # send app challenge (16 bytes) (must be wrapped in a bytearray)
        challenge = bytes(b'\0' * 16)
        logging.debug(("Sending key of all 0's: {}").format(challenge.hex()))
        self.m_iGrillChars[UUIDS.APP_CHALLENGE].write(challenge, True)

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
        We just hand back the same encrypted value we get and we're good.
        """
        encrypted_device_challenge = self.m_iGrillChars[UUIDS.DEVICE_CHALLENGE].read()
        logging.debug("encrypted device challenge: {0}".format((encrypted_device_challenge).hex()))
        self.m_iGrillChars[UUIDS.DEVICE_RESPONSE].write(encrypted_device_challenge, True)

        logging.debug("Authenticated")

        return True

    def ReadBattery(self):
        return int(ord(self.m_battery_char.read()))

class IGrillMiniPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the iGrill Mini
    """
    m_probe_count = 1

class IGrillPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the iGrill2/iGrill3
    """
    m_probe_count = 4
