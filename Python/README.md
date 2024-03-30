
Software had been tested thoroughly under Linux. It might work under Windows as well, but it hadn't been tested yet.


### Install:
1. You must have Python installed in your system. It's better be version 3.10 or higher
2. Install pyserial package: https://pyserial.readthedocs.io/en/latest/pyserial.html#installation
3. Put into your working folder all files except README.md.
4. Choose the name of your device (I'll refer to it as NewDevice everywhere): it must be string with no spaces, only letters and digits, maybe minus sign or underscore if you like it. You'll need it later practically everywhere.
5. Rename NewDevice.INI using your device name. Also, edit the section name inside the file if you plan to set some parameters for your device.
6. Rename new_device_template.py to the name of your device using snake_case naming convention. Edit the file using hints in comments. Add new code according to your device functionality.

