""" New Arduino device class template """

__version__ = '10.10.2022'
__author__ = 'Serhiy Kobyakov'

from arduino_device import ArduinoDevice


class NewDevice(ArduinoDevice):
    """ New Arduino device class template """
    # define the device name:
    # this is the string with which the device responds to b'?' query
    _device_name = "NewDevice"

    # other device-specific variables go here:

    def __init__(self, comport):
        super().__init__(comport)
        # self.read_basic_parameters(self._device_name + '.INI')
        # read the device parameters from INI file
        # all except COMPORTSPEED, TIMEOUT, WRITETIMEOUT, SHORTESTTIMEBETWEENREADS
        # YOU STILL HAVE TO PUT ALL THE NECESSARY VALUES INTO INI FILE!!!
        # config = configparser.ConfigParser()
        # config.read(self._device_name + '.INI')
        # self.[some parameter] = config[self._device_name]['some parameter']

        # do some default device-specific init actions here:

    def __del__(self):
        # do some default device-specific finalization actions here:

        # it must be here to close the serial communication correctly:
        super().__del__()
