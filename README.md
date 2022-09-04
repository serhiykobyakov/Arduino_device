# Arduino_device_FPC
Free Pascal Arduino device base object implementation

### What is it
What if you have few devices based on Arduino boards and want to use them each time without pain? By the pain I mean managing the COM port address each time before use. Would it be better if the devices initialize automatically when you start your main application?

The problems:
1. There must be a way to distinguish the boards
2. Some boards have non-native USB port and they initialize in about 2 seconds after serial communication have been established. The other boards are ready to work right away. There must be some way to deal with both types.

Solution:
1. Each board has it's own unique ID string with which it responds to '?' query.
2. Non-native USB boards must say 'Ready!' at the end of their setup process (or say nothing at all). Application which use the devices must be capable to deal with this during device's initialization process.


ArduinoDevice.pas - implements a basic Arduino device functionality (serial communication, object initialization and destruction).

device_template.pas - a template for new device. Feel free to change the file name and the variables in it to make your new device.

unit1.pas - Lazarus application main unit.


### How To Use

1. You need [Lazarus IDE](https://www.lazarus-ide.org/) or Free Pascal on your machine. I suppose that it may work in Delphi also.
2. MAke a directory for your project, put ArduinoDevice.pas and device_template.pas in it
3. Put in your directory jedi.inc, synafpc.pas, synaser.pas, synautil.pas from [Synapse repository](http://synapse.ararat.cz/doku.php/download)
4. Change device_template.pas file name to the device name, edit the code to match it to your device.


### Supported platforms
Linux (has been tested extensively)

Windows (tested once - successfully)


### Contact
For reporting [bugs, suggestions, patches](https://github.com/serhiykobyakov/Arduino_device_FPC/issues)


### License
The project is licensed under the [MIT license](https://github.com/serhiykobyakov/Arduino_device_FPC/blob/main/LICENSE)
