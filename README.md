# pyhm310p - HM310P Python Library

Python library to use with the Hanmatek HM310P

Dependencies:
 - pymodbus
 - matplotlib (optional for plotting)

Files:
 - hm310p.py: Actual library
 - serial_reader.py: Simple command line interface for monitoring with the option to save data to file and plot afterwards

Examples:
```
#!/usr/bin/python

from hm310p import HMReader
from time import sleep

reader = HMReader('/dev/ttyUSB0')
while True:
    print(reader.readVoltage())
    sleep(1)
```

```
#!/bin/sh

./serial_reader.py monitor /dev/ttyUSB0 -l -f data.txt
```
