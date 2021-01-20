from pymodbus.client.sync import ModbusSerialClient as ModbusClient

UNIT=0x1
regs = {'powerSwitch':0x01,
        'protectStat':0x02,
        'model': 0x03,
        'classDetail':0x04,
        'powerCal':0x14,
        'protectVoltage':0x20,
        'protectCurrent':0x21,
        'protectPower':0x22,
        'decimals':0x05,
        'ps':0x0010,
        'set':0x0030,
        'psm':0x1000,
        'm1':0x1000,
        'm2':0x1010,
        'm3':0x1020,
        'm4':0x1030,
        'm5':0x1040,
        'm6':0x1050,
        'Voltage':0x00,
        'Current':0x01,
        'Time':0x02,
        'Power':0x03,
        }

class HMReader:
    def __init__(self, device_path):
        self._client = ModbusClient(port=device_path, baudrate=9600, method='rtu', timeout=1)
        self._client.connect()
 

    def readModel(self):
        return self._client.read_holding_registers(regs['model'],
                1, unit=UNIT).registers[0]

    def read(self, register='ps'):
        ret = dict(zip(['Voltage', 'Current', 'Time', 'Power'],
            self._client.read_holding_registers(regs[register],
            4, unit=UNIT).registers))
        ret['Voltage'] = ret['Voltage'] / 100.0
        ret['Current'] = ret['Current'] / 1000.0
        ret['Power'] = ret['Power'] / 1000.0
        return ret
    
    def readVoltage(self, register='ps'):
        return self._client.read_holding_registers(regs[register] +
                regs['Voltage'], 1, unit=UNIT).registers[0]/100.0
    
    def readCurrent(self, register='ps'):
        return self._client.read_holding_registers(regs[register] +
                regs['Current'], 1, unit=UNIT).registers[0]/1000.0
    
    def readTime(self, register='ps'):
        return self._client.read_holding_registers(regs[register] +
                regs['Time'], 1, unit=UNIT).registers[0]
    
    def readPower(self, register='ps'):
        return self._client.read_holding_registers(regs[register] +
                regs['Power'], 1, unit=UNIT).registers[0]

    def setPower(self, val):
        self._client.write_register(regs['powerSwitch'], 1 if val else 0, unit=UNIT)

    def setProtectVoltage(self, val):
        self._client.write_register(regs['protectVoltage'], int(val*100.0), unit=UNIT)

    def setProtectCurrent(self, val):
        self._client.write_register(regs['protectCurrent'], int(val*1000.0), unit=UNIT)

    def setVoltage(self, val, register='set'):
        self._client.write_register(regs[register] + regs['Voltage'], int(val*100), unit=UNIT)

    def setCurrent(self, val, register='set'):
        self._client.write_register(regs[register] + regs['Current'], int(val*1000), unit=UNIT)

    def setTimeSpan(self, val, register='set'):
        self._client.write_register(regs[register] + regs['Time'], int(val*1000), unit=UNIT)

    def close(self):
        self._client.close()
