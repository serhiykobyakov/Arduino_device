"""Base Arduino device class"""

__version__ = '09.10.2022'
__author__ = 'Serhiy Kobyakov'

# import time
import configparser
import serial
import serial.tools.list_ports


class ArduinoDevice:
    """Basic arduino device class"""
    device_name = "ArduinoDevice"
    device_info = ""
    ser = None
    comport = ""

    COMPORTSPEED = 115200
    COMPORTPARITY = serial.PARITY_NONE
    COMPORTSTOPBITS = serial.STOPBITS_ONE
    COMPORTBITS = serial.EIGHTBITS
    COMPORTTIMEOUT = 0.4
    COMPORTWRITETIMEOUT = 0.1
    # the longest time which device may need to finish the task
    COMPORTLONGREADTIMEOUT = 5
    SHORTESTTIMEBETWEENREADS = 0.46

    def __repr__(self) -> str:
        return f'{self.device_name} at {self.comport}'

    def __str__(self) -> str:
        return f'{self.device_info}'

    @classmethod
    def get_device_id_str(cls, comport) -> str:
        """Returns True if the device is connected at COM port \"comport\""""
        result = b''
        if not isinstance(comport, str):
            raise TypeError(f"comport: string value expected, got {type(str)} instead")

        ser = serial.Serial(port=comport,
                            baudrate=cls.COMPORTSPEED,
                            writeTimeout=cls.COMPORTWRITETIMEOUT,
                            timeout=cls.COMPORTTIMEOUT,
                            parity=cls.COMPORTPARITY,
                            stopbits=cls.COMPORTSTOPBITS,
                            bytesize=cls.COMPORTBITS)
        try:
            ser.write(b'?')
            result = ser.readline().strip()
            if len(result) == 0:
                # if the device doesn't respond immediately it may be
                # a board with non-native USB
                ser.timeout = 5  # suppose the board has not been initialized yet.
                # give it 5 seonds to do it, but no more!
                # If i'ts not an Arduino, this routine will block the main app
                # for this amount of time (for each device!)
                result = ser.readline().strip()
                # ser.write(b'?')
                # ser.timeout = cls.COMPORTTIMEOUT
                # result = ser.readline().strip()
        finally:
            ser.close()
        return result.decode()

    # def __init__(self):
    #     pass

    def start_serial_communication(self, comport):
        """Device initialization - connecting to comport"""
        # getting the device info:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if port.device == comport:
                # save all comport parameters to info:
                list_of_strings = [f'{key}: {port.__dict__[key]}' for key in port.__dict__]
                self.device_info = "\n".join(list_of_strings)

        # connecting to comport:
        self.ser = serial.Serial(port=comport,
                                   baudrate=self.COMPORTSPEED,
                                   write_timeout=self.COMPORTWRITETIMEOUT,
                                   timeout=self.COMPORTTIMEOUT,
                                   parity=self.COMPORTPARITY,
                                   stopbits=self.COMPORTSTOPBITS,
                                   bytesize=self.COMPORTBITS)
        self.comport = comport
        self.ser.write(b'?')
        result = self.ser.readline().strip()
        if len(result) == 0:
            self.ser.timeout = 5
            result = self.ser.readline().strip()
            self.ser.timeout = self.COMPORTTIMEOUT
        if self.device_name != result.decode('UTF-8'):
            print(f"Error: got {result.decode('UTF-8')}, but expected {self.device_name} \
while establishing serial communication!")

    def read_basic_parameters(self, inifname):
        """ read the device parameters from INI file """
        config = configparser.ConfigParser()
        config.read(inifname)
        self.COMPORTSPEED = int(config['serial']['COMPORTSPEED'])
        self.COMPORTTIMEOUT = float(config['serial']['TIMEOUT'])
        self.COMPORTWRITETIMEOUT = float(config['serial']['WRITETIMEOUT'])
        self.COMPORTLONGREADTIMEOUT = float(config['serial']['LONGREADTIMEOUT'])
        self.SHORTESTTIMEBETWEENREADS = float(config['serial']['SHORTESTTIMEBETWEENREADS'])

    def __del__(self):
        self.ser.close()

    def send_and_get_answer(self, cmd) -> str:
        """ send command and get answer, short timeout """
        self.ser.write(cmd.encode())
        return self.ser.readline().strip().decode()

    def send_and_get_late_answer(self, cmd) -> str:
        """ send command and get answer, long timeout """
        self.ser.timeout = self.COMPORTLONGREADTIMEOUT
        self.ser.write(cmd.encode())
        answer = self.ser.readline().strip().decode()
        self.ser.timeout = self.COMPORTTIMEOUT
        return answer
