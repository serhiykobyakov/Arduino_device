""" New Arduino device class template """

__version__ = '19.02.2024'
__author__ = 'Serhiy Kobyakov'

from arduino_device import ArduinoDevice


class NewDevice(ArduinoDevice):
    """ New Arduino device class template """
    # define the device name:
    # this is the string with which the device responds to b'?' query
    _device_name = "NewDevice"

    # other device-specific variables go here:

    def __init__(self, comport):
        # repeat assigning class variables,
        # so they are visible in self.__dict__:
        self._device_name = self._device_name

        # read the device parameters from INI file
        # all except COMPORTSPEED, READTIMEOUT, WRITETIMEOUT,
        # LONGREADTIMEOUT and SHORTESTTIMEBETWEENREADS:

        # inifname = self._device_name + '.INI'
        # with open(inifname, "r") as f:
        #    config = configparser.ConfigParser()
        #    config.read_file(f)
        #    self.[some parameter] =
        #    config[self._device_name]['some parameter']

        # start serial communication with the device
        # this is the place for the line!
        super().__init__(comport)

        # do some default device-specific init actions here:

    def __del__(self):
        # do some default device-specific finalization actions here:

        # this is the place for the line!
        super().__del__()
