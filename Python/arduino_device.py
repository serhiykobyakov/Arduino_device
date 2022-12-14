""" Base Arduino device class """

__version__ = '10.10.2022'
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
    COMPORTWRITETIMEOUT = 0.2
    # the shortest time the device may need to finish the task and give an answer
    COMPORTREADTIMEOUT = 1
    # the longest time the device may need to finish the task and give an answer
    COMPORTLONGREADTIMEOUT = 5
    # the shortest time between consequent device commands
    # it is not reasonable in this short time to ask the device do something twice
    # in this case it is better that the device just return previous answer
    # to the second inquiry:
    SHORTESTTIMEBETWEENREADS = 0.46

    _device_name = ""
    _ser = None

    # timestamp of the last communication with the device
    _lastcomtimestamp = 0.0

    def __repr__(self) -> str:
        return f'{self._device_name} at {self._ser.port}'

    def __str__(self) -> str:
        return f'{self._device_name} at {self._ser.port}'

    @classmethod
    def get_device_id_str(cls, comport) -> str:
        """Returns True if the device is connected at COM port \"comport\""""
        result = b''
        if not isinstance(comport, str):
            raise TypeError(f"comport: string value expected, got {type(str)} instead")

        cls._ser = serial.Serial(port=comport,
                            baudrate=cls.COMPORTSPEED,
                            writeTimeout=cls.COMPORTWRITETIMEOUT,
                            timeout=cls.COMPORTREADTIMEOUT,
                            parity=cls.COMPORTPARITY,
                            stopbits=cls.COMPORTSTOPBITS,
                            bytesize=cls.COMPORTBITS)
        try:
            cls._ser.write(b'?')
            result = cls._ser.readline().strip()
            if len(result) == 0:
                # if the device doesn't respond immediately it may be
                # a board with non-native USB
                cls._ser.timeout = 5  # suppose the board has not been initialized yet.
                # give it 5 seconds to do it, but no more!
                # If it's not an Arduino, this routine will block the main app
                # for this amount of time (for each device!)
                result = cls._ser.readline().strip()
                # cls._ser.write(b'?')
                # cls._ser.timeout = cls.COMPORTTIMEOUT
                # result = cls._ser.readline().strip()
        finally:
            cls._ser.close()
        return result.decode()

    def __init__(self, comport):
        """ device initialization - connecting to comport """
        # read the device parameters from INI file
        inifname = self._device_name + '.INI'
        config = configparser.ConfigParser()
        config.read(inifname)
        self.COMPORTSPEED = -1
        self.COMPORTSPEED = int(config['serial']['COMPORTSPEED'])
        # simple check if we read the config file:
        if self.COMPORTSPEED == -1:
            print(f"Error reading {inifname} file!")
        self.COMPORTREADTIMEOUT = float(config['serial']['READTIMEOUT'])
        self.COMPORTWRITETIMEOUT = float(config['serial']['WRITETIMEOUT'])
        self.COMPORTLONGREADTIMEOUT = float(config['serial']['LONGREADTIMEOUT'])
        self.SHORTESTTIMEBETWEENREADS = float(config['serial']['SHORTESTTIMEBETWEENREADS'])
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
            print(f"Error: got {result.decode('UTF-8')}, but expected {self._device_name} \
while establishing _serial communication!")

    def __del__(self):
        self._ser.close()

    @property
    def is_connected(self):
        """ check if the device is still connected to serial port """
        if os.path.exists(self._ser.port):
            return True
        else:
            return False

    @property
    def device_info(self) -> str:
        """ get device-specific attributes as a text """
        list_of_prop = [f'{key}: {self.__dict__[key]}' for key in self.__dict__]
        the_info = "\n".join(list_of_prop)
        return the_info

    @property
    def serial_info(self) -> str:
        """ get serial communication attributes as a text """
        list_of_strings = [f'{key}: {self._ser.__dict__[key]}' for key in self._ser.__dict__]
        the_info = "\n".join(list_of_strings)
        return the_info

    @property
    def comport_info(self) -> str:
        """ get COM port attributes as a text """
        list_of_strings = []
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == self._ser.name:
                list_of_strings = [f'{key}: {port.__dict__[key]}' for key in port.__dict__]
        the_info = "\n".join(list_of_strings)
        return the_info

    def send_and_get_answer(self, cmd) -> str:
        """ send command and get answer, short timeout """
        if not self.is_connected:
            print(f"The device{self._device_name} is disconnected!")
            return ""
        else:
            self._ser.write(cmd.encode())
            answer = self._ser.readline().strip().decode()
            self._lastcomtimestamp = time.time()
            return answer

    def send_and_get_late_answer(self, cmd) -> str:
        """ send command and get answer, long timeout """
        if not self.is_connected:
            print(f"The device{self._device_name} is disconnected!")
            return ""
        else:
            self._ser.timeout = self.COMPORTLONGREADTIMEOUT
            self._ser.write(cmd.encode())
            answer = self._ser.readline().strip().decode()
            self._lastcomtimestamp = time.time()
            self._ser.timeout = self.COMPORTREADTIMEOUT
            return answer
