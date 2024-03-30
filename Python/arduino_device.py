"""class ArduinoDevice is a base class
for devices built on Arduino boards using serial communication"""

__version__ = '29.03.2024'
__author__ = 'Serhiy Kobyakov'

import time
import os
import re
import configparser
import serial
import serial.tools.list_ports


class ArduinoDevice:
    """Base Arduino device class"""
    # several values
    # inherent to Arduino serial port communication:
    COMPORTPARITY = serial.PARITY_NONE
    COMPORTSTOPBITS = serial.STOPBITS_ONE
    COMPORTBITS = serial.EIGHTBITS

    # Speed of serial communication may vary
    # but for the sake of unification and simplification
    # let it be 115200 across all devices.
    # This value have been carefully tested
    # on various Arduino boards starting from UNO R3
    COMPORTSPEED = 115200

    _device_name = ""
    _ser = None

    # timestamp of the last serial communication
    _lastcomtimestamp = 0.0

    def __repr__(self) -> str:
        return f'{self._device_name} at {self._ser.port}'

    def __str__(self) -> str:
        return f'{self._device_name} at {self._ser.port}'

    @classmethod
    def get_arduino_serial_devices_dict(cls):
        """get the dictionary of available adruino devices
in the form of 'device id string': 'the serial port'"""
        ports = serial.tools.list_ports.comports()
        dev_dict = {}
        for port in ports:
            if len(re.findall(r".*ttyACM\d", port)) > 0 or \
               len(re.findall(r".*ttyUSB\d", port)) > 0 or \
               len(re.findall(r"^COM\d", port)) > 0:
                arduino_dev = cls.get_device_id_str(port.device)
                if len(arduino_dev) > 0:
                    dev_dict[arduino_dev] = port.device
        return dev_dict

    @classmethod
    def get_device_id_str(cls, comport) -> str:
        """Returns True if the device is connected at COM port \"comport\""""
        result = b''
        if not isinstance(comport, str):
            raise TypeError(f"comport: string value expected, \
            got {type(str)} instead")
        # if the device doesn't respond immediately it may be
        # a board with non-native USB
        # suppose the board has not been initialized yet.
        # give it 5 seconds as timeout to do it, but no more!
        # If it's not an Arduino,
        # this routine will block the main app
        # for this amount of time (for each device!)
        cls._ser = serial.Serial(port=comport,
                                 baudrate=cls.COMPORTSPEED,
                                 writeTimeout=2.,
                                 timeout=5.,
                                 parity=cls.COMPORTPARITY,
                                 stopbits=cls.COMPORTSTOPBITS,
                                 bytesize=cls.COMPORTBITS)
        try:
            cls._ser.flush()
            cls._ser.write(b'?')
            result = cls._ser.readline().strip().decode()
            # ~ print(f"{comport}: {result} of len: {len(result)}")
            if 0 < len(result) <= 2:
                # give it a second chance
                # if the answer is too short but not zero length
                cls._ser.flush()
                cls._ser.write(b'?')
                result = cls._ser.readline().strip().decode()
        finally:
            cls._ser.close()
        return result

    def __new__(cls, comport):
        """few checks before we start init an instance..."""
        instance = super().__new__(cls)

        # check if ini file exists
        if not os.path.isfile(cls._device_name + '.INI'):
            print(f"\n  ERROR: no {cls._device_name + '.INI'} file found!\n")
            return

        return instance

    def __init__(self, comport):
        """ device initialization - connecting to comport """

        # read the serial port parameters from INI file
        inifname = self._device_name + '.INI'
        with open(inifname, "r") as f:
            config = configparser.ConfigParser()
            config.read_file(f)
            self.COMPORTREADTIMEOUT = -1
            self.COMPORTREADTIMEOUT = \
                float(config['serial']['READTIMEOUT'])
            if self.COMPORTREADTIMEOUT == -1:
                print(f"""  {self._device_name} at {comport}:
  Error reading {inifname} file!""")
                return
            self.COMPORTWRITETIMEOUT = \
                float(config['serial']['WRITETIMEOUT'])
            self.COMPORTLONGREADTIMEOUT = \
                float(config['serial']['LONGREADTIMEOUT'])
            self.SHORTESTTIMEBETWEENREADS = \
                float(config['serial']['SHORTESTTIMEBETWEENREADS'])

        # connecting to comport:
        self._ser = serial.Serial(port=comport,
                                  baudrate=self.COMPORTSPEED,
                                  write_timeout=self.COMPORTWRITETIMEOUT,
                                  timeout=self.COMPORTREADTIMEOUT,
                                  parity=self.COMPORTPARITY,
                                  stopbits=self.COMPORTSTOPBITS,
                                  bytesize=self.COMPORTBITS)
        if not self._ser.isOpen():
            print(f"Error establishing communication with {comport} device!")
        self._ser.write(b'?')
        result = self._ser.readline().strip()
        if len(result) == 0:
            self._ser.timeout = 5
            result = self._ser.readline().strip()
            self._ser.timeout = self.COMPORTREADTIMEOUT
        if self._device_name != result.decode('UTF-8'):
            print(f"Error: got {result.decode('UTF-8')}, \
but expected {self._device_name} \
while establishing _serial communication!")
            return

    def __del__(self):
        self._ser.close()

    @property
    def is_connected(self):
        """ check if the device is still connected to serial port """
        return bool(os.path.exists(self._ser.port))

    @property
    def device_info(self) -> str:
        """ get device-specific attributes as a text """
        list_of_prop = [f'{key}: {self.__dict__[key]}'
                        for key in self.__dict__]
        the_info = "\n".join(list_of_prop)
        return the_info

    @property
    def serial_info(self) -> str:
        """ get serial communication attributes as a text """
        list_of_strings = [f'{key}: {self._ser.__dict__[key]}'
                           for key in self._ser.__dict__]
        the_info = "\n".join(list_of_strings)
        return the_info

    @property
    def comport_info(self) -> str:
        """ get COM port attributes as a text """
        list_of_strings = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == self._ser.name:
                list_of_strings = [f'{key}: {port.__dict__[key]}'
                                   for key in port.__dict__]
        the_info = "\n".join(list_of_strings)
        return the_info

    def send_and_get_answer(self, cmd) -> str:
        """ send command and get answer, short timeout """
        if not self.is_connected:
            print(f"The device{self._device_name} is disconnected!")
            return ""
        self._ser.write(cmd.encode())
        answer = self._ser.readline().strip().decode()
        self._lastcomtimestamp = time.time()
        return answer

    def send_and_get_late_answer(self, cmd) -> str:
        """ send command and get answer, long timeout """
        if not self.is_connected:
            print(f"The device{self._device_name} is disconnected!")
            return ""
        self._ser.timeout = self.COMPORTLONGREADTIMEOUT
        self._ser.write(cmd.encode())
        answer = self._ser.readline().strip().decode()
        self._lastcomtimestamp = time.time()
        self._ser.timeout = self.COMPORTREADTIMEOUT
        return answer
