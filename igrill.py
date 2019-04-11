import bluepy.btle as btle
import random

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


class IDevicePeripheral(btle.Peripheral):
    encryption_key = None

    def __init__(self, address):
        """
        Connects to the device given by address performing necessary authentication
        """
        btle.Peripheral.__init__(self, address)

        # iDevice devices require bonding. I don't think this will give us bonding
        # if no bonding exists, so please use bluetoothctl to create a bond first
        self.setSecurityLevel("medium")

        # enumerate all characteristics so we can look up handles from uuids
        self.characteristics = self.getCharacteristics()

        # authenticate with iDevices custom challenge/response protocol
        if not self.authenticate():
            raise RuntimeError("Unable to authenticate with device")

    def characteristic(self, uuid):
        """
        Returns the characteristic for a given uuid.
        """
        for c in self.characteristics:
            if c.uuid == uuid:
                return c

    def authenticate(self):
        """
        Performs iDevices challenge/response handshake. Returns if handshake succeeded

        Works for all devices using this handshake, no key required
        """
        print "Authenticating..."

        # send app challenge (16 bytes)
        challenge = str([0] * 16)
        self.characteristic(UUIDS.APP_CHALLENGE).write(challenge, True)

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
        encrypted_device_challenge = self.characteristic(UUIDS.DEVICE_CHALLENGE).read()
        print "encrypted device challenge:", str(encrypted_device_challenge).encode("hex")
        self.characteristic(UUIDS.DEVICE_RESPONSE).write(encrypted_device_challenge, True)

        print("Authenticated")

        return True


class IGrillMiniPeripheral(IDevicePeripheral):
    """
    Specialization of iDevice peripheral for the iGrill Mini
    """

    def __init__(self, address):
        IDevicePeripheral.__init__(self, address)

        # find characteristics for battery and temperature
        self.battery_char = self.characteristic(UUIDS.BATTERY_LEVEL)
        self.temp_char = self.characteristic(UUIDS.PROBE1_TEMPERATURE)

    def read_temperature(self):
        # possibly change to unpack?
        temp = ord(self.temp_char.read()[1]) * 256
        temp += ord(self.temp_char.read()[0])

        return { 1: int(temp), 2: 63536, 3: 63536, 4: 63536 }

    def read_battery(self):
        return int(ord(self.battery_char.read()[0]))


class IGrillV2Peripheral(IDevicePeripheral):

    def __init__(self, address):
        IDevicePeripheral.__init__(self, address)

        # find characteristics for battery and temperature
        self.battery_char = self.characteristic(UUIDS.BATTERY_LEVEL)
        self.temp_chars = {}

        for probe_num in range(1,5):
            temp_char_name = 'PROBE{}_TEMPERATURE'.format(probe_num)
            temp_char = self.characteristic(getattr(UUIDS, temp_char_name))
            self.temp_chars[probe_num] = temp_char

    def read_temperature(self):
        temps = {}
        for probe_num, temp_char in self.temp_chars.items():
            temp = ord(temp_char.read()[1]) * 256
            temp += ord(temp_char.read()[0])
            temps[probe_num] = int(temp)

        return temps

    def read_battery(self):
        return int(ord(self.battery_char.read()[0]))
