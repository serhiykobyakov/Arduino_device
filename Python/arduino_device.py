""" Base Arduino device class """

__version__ = '24.02.2024'
__author__ = 'Serhiy Kobyakov'

import time
import os
import configparser
import serial
import serial.tools.list_ports


class ArduinoDevice:
    """Basic arduino device class"""
    # serial communication constants:
    COMPORTPARITY = serial.PARITY_NONE
    COMPORTSTOPBITS = serial.STOPBITS_ONE
    COMPORTBITS = serial.EIGHTBITS
    COMPORTSPEED = 115200
    # the longest time which is necessary to send the command to device:
    # COMPORTWRITETIMEOUT = 0.2
    # the shortest time the device may need
    # to finish the task and give an answer
    # COMPORTREADTIMEOUT = 1
    # the longest time the device may need
    # to finish the task and give an answer
    # COMPORTLONGREADTIMEOUT = 5
    # the shortest time between consequent device commands
    # it is not reasonable in this short time
    # to ask the device do something twice
    # in this case it is better that the device
    # just return previous answer
    # to the second inquiry:
    # SHORTESTTIMEBETWEENREADS = 0.46

    _device_name = ""
    _ser = None

    # timestamp of the last communication with the device
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

        # ~ print("\nserial devices found in system:")
        # ~ for port in ports:
            # ~ print(port.device)
        # ~ print()

        dev_dict = {}
        # ~ print("Scanning serial ports for arduino devices:")
        for port in ports:
            if port.device.find("ttyACM") > 0 or \
               port.device.find("ttyUSB") > 0:
                arduino_dev = cls.get_device_id_str(port.device)
                if len(arduino_dev) > 0:
                    dev_dict[arduino_dev] = port.device
                    # ~ print(arduino_dev, port.device)
        # ~ print("done!")
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
                # give it a second chance if the answer is too short
                # but not zero
                # ~ print(f"  EE {comport}: can't read answer!")
                cls._ser.flush()
                cls._ser.write(b'?')
                result = cls._ser.readline().strip().decode()
                # ~ print(f"  finally {comport}: {result}")
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
        self.COMPORTWRITETIMEOUT = 0.2
        self.COMPORTREADTIMEOUT = 1.
        self.COMPORTLONGREADTIMEOUT = 2.
        self.SHORTESTTIMEBETWEENREADS = 0.1

        # read the serial port parameters from INI file
        inifname = self._device_name + '.INI'
        with open(inifname, "r") as f:
            config = configparser.ConfigParser()
            config.read_file(f)
            self.COMPORTSPEED = -1
            self.COMPORTSPEED = int(config['serial']['COMPORTSPEED'])
            # simple check if we read the config file:
            if self.COMPORTSPEED == -1:
                print(f"Error reading {inifname} file!")
            self.COMPORTREADTIMEOUT = \
                float(config['serial']['READTIMEOUT'])
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
