# Free Pascal Arduino device base object implementation

### What is it
What if you have few devices based on Arduino boards and want to use them each time without pain? By the pain I mean managing the COM port address each time before use. Would it be better if the devices initialize automatically when you start your main application? By the way, I haven't found the solution before. If you know one - please let me know.

The problems:
1. There must be a way to distinguish the boards
2. Some boards have non-native USB port and they initialize in about 2 seconds after serial communication have been established. The other boards are ready to work right away. There must be some way to deal with both types.

Solution:
1. Each board has it's own unique ID string with which it responds to '?' query.
2. Non-native USB boards must say 'Ready!' at the end of their setup process (or say nothing at all). Application which use the devices must be capable to deal with this during device's initialization process.


### Contact
For reporting [bugs, suggestions, patches](https://github.com/serhiykobyakov/Arduino_device_FPC/issues)


### License
The project is licensed under the [MIT license](https://github.com/serhiykobyakov/Arduino_device_FPC/blob/main/LICENSE)
