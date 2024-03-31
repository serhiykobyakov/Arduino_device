# Arduino device base object implementation

Imagine you have few devices based on Arduino boards connected to PC using usb-serial. The boards are dedicated to different devices. What if you want to use them all simultaneously without managing serial port addresses? Would it be better if the devices initialize automatically when you start your main application? By the way, I haven't found a ready solution before. If you know one - please let me know.

So, there must be a way to distinguish connected boards, which means there must be a communication protocol and some base class which implement it. Also, since I plan to implement a base class - maybe it is a good idea to add a few auxiliary functions.

### The problem:
There must be a way to distinguish the Arduino boards connected to PC simultaneously

### Solution:
There must be some standard protocol of communication among all devices. Each board must have it's own unique device name (ID string) with which it responds to '?' query.

### Protocol in general
* The commands, which PC sends to board, have to be short (ideally it is a single character).
* Arduino board sends back answer to every command it receives, either sending back information (in some defined way - each situation is different) or some previously defined character just to confirm the command have been received. The answer must be a terminated string so PC software knows where is the end of the answer.
* There must be a standard command ('?') for every board on which they will respond with their individual device names.
* For the sake of communication stability the board must always respond to command in certain way, for example returning the value of parameter in question.

### Moreover
* Each device must take it's individual parameters (as well as serial port parameters) from INI file. This is a faster way to manipulate the parametes values and no code editing is necessary.

### Contact
For reporting [bugs, suggestions, patches](https://github.com/serhiykobyakov/Arduino_device_FPC/issues)

### License
The project is licensed under the [MIT license](https://github.com/serhiykobyakov/Arduino_device_FPC/blob/main/LICENSE)
