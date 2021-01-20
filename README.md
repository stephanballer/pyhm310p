# pyhm310p

Python library to use with the Hanmatek HP310P

Dependencies:
 - pymodbus

Files:
 - hm310p.py: Actual library
 - serial_reader.py: Simple command line interface for monitoring with the option to save data to file and plot afterwards

Example:
```
from hm310p import HMReader
from time import sleep

reader = HMReader('/dev/ttyUSB0')
while True:
    print(reader.readVoltage())
    sleep(1)
```
