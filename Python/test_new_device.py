#!/usr/bin/python3

import serial
import serial.tools.list_ports
from arduino_device import ArduinoDevice as ad
from new_device import NewDevice


if __name__ == "__main__":
    # Let's check the active serial devices and list them all:
    # print("\nLooking for serial devices...", end="\r")
    # ports = serial.tools.list_ports.comports()
    # if len(ports) == 0:
    #     print("No serial devices found!", " "*50, "\n")
    # else:
    #     for port in ports:
    #         print(f"{port.device}:", ad.get_device_id_str(port.device), " "*50, "\n")

    theport = ''
    ndevice = None
    old_id = id(ndevice)

    ports = serial.tools.list_ports.comports()
    for port in ports:
        if ad.get_device_id_str(port.device) == 'NewDevice':
            theport = port.device
    if len(theport) > 0:
        ndevice = NewDevice(theport)

    # print("new id:", id(shutter))

    if id(ndevice) == old_id:
        print("\nError initializing the device!\n")
        sys.exit(1)

    print("\n  Device info:\n" + ndevice.device_info)
    print("\n  Serial communication info:\n" + ndevice.serial_info)
    print("\n  COM port info:\n" + ndevice.comport_info)
