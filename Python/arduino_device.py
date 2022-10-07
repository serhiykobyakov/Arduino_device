""" contains basic Arduino device class

"""

__version__ = '03.10.2022'
__author__ = 'Serhiy Kobyakov'


#import time
import serial
import serial.tools.list_ports


class ArduinoDevice:
    """Basic arduino device class"""

    __ser = None
    __comport = ""
    __device_name = ""
    __device_info = ""

    COMPORTSPEED = 115200
    COMPORTPARITY = serial.PARITY_NONE
    COMPORTSTOPBITS = serial.STOPBITS_ONE
    COMPORTBITS = serial.EIGHTBITS
    COMPORTTIMEOUT = 0.4
    COMPORTWRITETIMEOUT = 0.1
    SHORTESTTIMEBETWEENREADS = 0.46


    def __repr__(self) -> str:
        return f'{self.__device_name} at {self.__comport}'

    def __str__(self) -> str:
        return f'{self.__device_info}'


    @classmethod
    def get_device_id_str(cls, comport) -> str:
        "Returns True if the device is connected at COM port \"comport\""
        result = b''
        if not isinstance(comport, str):
            raise TypeError(f"comport: string value expected, got {type(str)} instead")

        ser = serial.Serial(port = comport,
                            baudrate = cls.COMPORTSPEED,
                            writeTimeout = cls.COMPORTWRITETIMEOUT,
                            timeout = cls.COMPORTTIMEOUT,
                            parity = cls.COMPORTPARITY,
                            stopbits = cls.COMPORTSTOPBITS,
                            bytesize = cls.COMPORTBITS)
        ser.write(b'?')
        try:
            result = ser.readline().strip()
            if len(result) == 0:
                # if the device doesn't respond immediately it may be
                # a board with non-native USB
                ser.timeout = 5 # suppose the board has not been initialized yet, give it
                                # give it 5 seonds to do it, but no more!
                                # If i'ts not an Arduino, this routine will block the main app
                                # for this amount of time (for each device!)
                result = ser.readline().strip()
                ser.write(b'?')
                ser.timeout = cls.COMPORTTIMEOUT
                result = ser.readline().strip()
        finally:
            ser.close()
        return result.decode()


    def init(self, comport):
        "Device initialization - connecting to comport"
        # gathering the device info:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == comport:
                # all strings:
                # list_of_strings = [ f'{key}: {port.__dict__[key]}' for key in port.__dict__ ]
                # self.__device_info = "\n".join(list_of_strings)
                self.__device_info = "device: " + port.__dict__["device"] + "\n" +\
                "hwid: " + port.__dict__["hwid"] + "\n" +\
                "description: " + port.__dict__["description"] + "\n" +\
                "subsystem: " + port.__dict__["subsystem"] + "\n" +\
                "manufacturer: " + port.__dict__["manufacturer"]

        # connecting to comport:
        self.__ser = serial.Serial(port = comport,
                            baudrate = self.COMPORTSPEED,
                            write_timeout = self.COMPORTWRITETIMEOUT,
                            timeout = self.COMPORTTIMEOUT,
                            parity = self.COMPORTPARITY,
                            stopbits = self.COMPORTSTOPBITS,
                            bytesize = self.COMPORTBITS)
        self.__comport = comport        
        self.__ser.write(b'?')
        result = self.__ser.readline().strip()
        if len(result) == 0:
            self.__ser.timeout = 5
            result = self.__ser.readline().strip()
            self.__ser.timeout = self.COMPORTTIMEOUT


    def __del__(self):
        self.__ser.close()
