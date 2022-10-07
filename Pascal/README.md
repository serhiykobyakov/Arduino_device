# Arduino device base object (Free Pascal implementation)

ArduinoDevice.pas - implements a basic Arduino device functionality (serial communication, object initialization and destruction).

device_template.pas - a template for new device. Feel free to change the file name and the variables in it to make your new device.

unit1.pas - Lazarus application main unit.

### How To Use

1. You need [Lazarus IDE](https://www.lazarus-ide.org/) or Free Pascal on your machine. I suppose that it may work in Delphi also.
2. Make a directory for your project, put ArduinoDevice.pas and device_template.pas in it
3. Put in your directory jedi.inc, synafpc.pas, synaser.pas, synautil.pas from [Synapse repository](http://synapse.ararat.cz/doku.php/download)
4. Change device_template.pas file name to the device name, edit the code to match it to your device.


### Supported platforms
Linux (has been tested extensively)

Windows (tested once - successfully)
