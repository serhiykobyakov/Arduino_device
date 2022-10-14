# Arduino device base object implementation

What if you have few devices based on Arduino boards and want to use them simultaneously without managing serial port addresses? Would it be better if the devices initialize automatically when you start your main application? By the way, I haven't found the solution before. If you know one - please let me know.

So, there must be a way to distinguish the boards, which means there must be a communication protocol and some base class which implement it. And since I plan to make a base class - maybe it is a good idea to implement few auxiliary functions.

### The problems:
1. There must be a way to distinguish the boards
2. Some boards have non-native USB port and they initialize in about 2 seconds after serial communication have been established. The other boards are ready to work right away. There must be some way to deal with both types.

### Solutions:
1. Each board has it's own unique ID string with which it responds to '?' query.
2. Non-native USB boards must say 'Ready!' at the end of their setup process (or say nothing at all). Application which use the devices must be capable to deal with this during device's initialization process.

### Protocol in general
* Commands which a PC sends to Arduino have to be short (ideally it is a single character) without terminator(s). 
* Arduino sends back answer to every command it receives, either sending back information (in some defined way - each situation is different) or some previously defined character just to confirm the command have been received. The answer must be a terminated string so PC software knows where is the end of the answer.
* There will be a standard command('?') for every board on which they will respond with their individual device names - this is the way to differ boards. Moreover, the boards with non-native USB port (Arduino UNO etc.) will send their name right after the serial communication is initialized.
* Send '?' command when starting communication with a board, and if it responds immidiately (boards with native USB port) - OK, if not - wait few seconds since it may be a board with non-native USB port and try to read the serial port again. If the device name has been obtained - OK, if not - it may be some other serial device which doesn't understand our protocol.

### Moreover
* Each device must take it's individual parameters (as well as serial port parameters) from INI file. This way it would be faster to mnipulate the parametes values while testing devices.

### Contact
For reporting [bugs, suggestions, patches](https://github.com/serhiykobyakov/Arduino_device_FPC/issues)


### License
The project is licensed under the [MIT license](https://github.com/serhiykobyakov/Arduino_device_FPC/blob/main/LICENSE)
