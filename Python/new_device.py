""" New Arduino device class template """

__version__ = '09.10.2022'
__author__ = 'Serhiy Kobyakov'

from arduino_device import ArduinoDevice


class NewDevice(ArduinoDevice):
    """ New Arduino device class template """
    # define the device name:
    # this is the string with which the device responds to b'?' query
    device_name = "NewDevice"

    def __init__(self, comport):
        super().__init__()
        self.read_basic_parameters(self.device_name + '.INI')
        # read the device parameters from INI file
        # all except COMPORTSPEED, TIMEOUT, WRITETIMEOUT, SHORTESTTIMEBETWEENREADS
        # YOU STILL HAVE TO PUT ALL THE NECESSARY VALUES INTO INI FILE!!!
        # config = configparser.ConfigParser()
        # config.read(self.__device_name + '.INI')
        # self.[some parameter] = config[self.__device_name]['some parameter']

        self.start_serial_communication(comport)

    def __del__(self):
        # some stuff before closing connection to the device
        super().__del__()

