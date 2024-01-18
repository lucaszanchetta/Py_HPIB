import pyvisa
import time

class HP6633a:

    def __init__(self, gpibAddr):
        print('-- Initializing Power Supply --')
        self.gpibAddr = 'GPIB0::{}::INSTR'.format(gpibAddr)
        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(self.gpibAddr)
        print('-- Connected to Power Supply --')

    def writeCommand(self, command):
        self.instr.write(command)

    def readCommand(self, command):
        self.writeCommand(command)
        try:
            response = self.instr.read().strip()
            return response
        except pyvisa.VisaIOError:
            return 'Error in reading response'

    def resetOP(self):
        self.writeCommand('RST')

    def setDisplay(self, state):
        if state in [0, 1]:
            self.writeCommand('DSP {}'.format(state))
        else:
            print("Invalid state: state = 0: Display off, state = 1: Display on")

    def setVoltage(self, voltage):
        if 0 <= voltage <= 50:
            self.writeCommand('VSET {}'.format(voltage))
        else:
            print("Invalid voltage: 0 <= voltage <= 50")

    def setCurrent(self, current):
        if 0 <= current <= 2:
            self.writeCommand('ISET {}'.format(current))
        else:
            print("Invalid current: 0 <= current <= 2")

    def OVSet(self, voltage):
        self.writeCommand('OVSET {}'.format(voltage))

    def OCSet(self, state):
        if state in [0, 1]:
            self.writeCommand('OCSET {}'.format(state))
        else:
            print("Invalid state: state = 0: OCP off, state = 1: OCP on")

    def setOutput(self, state):
        if state in [0, 1]:
            self.writeCommand
            self.writeCommand('OUT {}'.format(state))
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
        self.writeCommand('CLR')

# Usage example
# psu = HP6633a(25)
# psu.setVoltage(0)
# print("Output Voltage: ", psu.getOutputVoltage())
# Add additional calls to other methods as needed
