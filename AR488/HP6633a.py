import time
import serial

class HP6633a:

    def __init__(self, ser, gpibAddr):
        print('-- Initializing Power Supply --')
        self.ser = ser
        self.gpibAddr = gpibAddr
        self.set_address(self.gpibAddr)
        self.ser.flush()
        print('-- Connected to Power Supply --')

    def set_address(self, addr):
        self.ser.flush()
        self.ser.write(bytearray('++addr {}\r'.format(addr), 'utf-8'))
        self.ser.flush()
        time.sleep(0.025)
        # self.ser.write(bytearray('++auto 1\r', 'utf-8'))
        # self.ser.flush()

    def writeCommand(self, command):
        self.set_address(self.gpibAddr)
        time.sleep(0.025)
        self.ser.flush()
        self.ser.write(bytearray(command + '\r', 'utf-8'))
        self.ser.flush()

    def readCommand(self, command):
        self.set_address(self.gpibAddr)
        self.ser.flush()
        time.sleep(0.025)
        self.ser.write(bytearray('++auto 1\r', 'utf-8'))
        self.ser.flush()
        self.writeCommand(command)
        self.ser.flush()
        time.sleep(0.025)
        response = self.ser.readline().decode().strip()
        return response

    def resetOP(self):
        ''' Resets OCP and OVP if tripped '''
        self.writeCommand('RST')

    def setDisplay(self, state):
        ''' state = 0: Display off, state = 1: Display on '''
        if (self.state == 0 or self.state == 1):
            self.writeCommand('DSP {}'.format(state))
        else:
            print("Invalid state: state = 0: Display off, state = 1: Display on")

    def setVoltage(self, voltage):
        ''' setVoltage(5) = 5 V '''
        if (0 <= voltage <= 50):
            self.writeCommand('VSET {}'.format(voltage))
        else:
            print("Invalid voltage: 0 <= voltage <= 50")

    def setCurrent(self, current):
        ''' setCurrent(0.5) = 0.5 A '''
        if (0 <= current <= 2):
            self.writeCommand('ISET {}'.format(current))
            self.ser.flush()
        else:
            print("Invalid current: 0 <= current <= 10")

    def OVSet(self, voltage):
        ''' OVSet(5) = 5 V '''
        self.writeCommand('OVSET {}'.format(voltage))

    def OCSet(self, state):
        ''' state = 0: OCP off, state = 1: OCP on '''
        if (state == 0 or state == 1):
            self.writeCommand('OCSET {}'.format(state))
            self.ser.flush()
        else:
            print("Invalid state: state = 0: OCP off, state = 1: OCP on")

    def setOutput(self, state):
        ''' state = 0: Output off, state = 1: Output on '''
        if (state == 0 or state == 1):
            self.writeCommand('OUT {}'.format(state))
            self.ser.flush()
        
        else:
            print("Invalid state: state = 0: Output off, state = 1: Output on")

    def getStatus(self):
        return self.readCommand('STS?')

    def getOutputVoltage(self):
        return self.readCommand('VOUT?')

    def getOutputCurrent(self):
        return self.readCommand('IOUT?')

    def getFaultRegister(self):
        return self.readCommand('FAULT')

    def getErrorRegister(self):
        return self.readCommand('ERR?')

    def getSelfTestResults(self):
        return self.readCommand('TEST?')

    def getModelNumber(self):
        return self.readCommand('ID?')

    def getROMVersion(self):
        return self.readCommand('ROM?')
    
    def clear(self):
        return self.writeCommand('CLR')
