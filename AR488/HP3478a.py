import serial
import time

class HP3478a:

    meterFunctionNames = {"DCV", "ACV", "2 Wire Ohms", "4 Wire Ohms", "DCA", "ACA", "X Ohms"}
    triggerTytpeNames = {"Internal", "External", "Single", "Hold", "Fast"}
    vRangeNames = {"30mV", "300mV", "3V", "30V", "300V"}
    ohmsRangeNames = {"30Ohm", "300Ohm", "3kOhm", "30kOhm", "300kOhm", "3MOhm", "30MOhm"}
    currentRangeNames = {"300mA", "3A", "3A"}

    def __init__(self, ser, gpibAddr):
        print('-- Initializing Multimeter --')
        self.gpibAddr = gpibAddr
        self.ser = ser
        self.set_address(self.gpibAddr)
        self.ser.write(bytearray('++auto 1\r', 'utf-8'))
        self.ser.flush()
        print('-- Connected to Multimeter --')

    def set_address(self, addr):
        self.ser.write(bytearray('++addr {}\r'.format(addr), 'utf-8'))
        self.ser.flush()
        time.sleep(0.025)
        self.ser.write(bytearray('++auto 1\r', 'utf-8'))
        self.ser.flush()


    def readCommand(self, function, range, autozero, digits, trigger):
        self.set_address(self.gpibAddr)
        self.ser.flush()
        time.sleep(0.025)
        #self.ser.reset_input_buffer()
        #self.ser.reset_output_buffer()
        command = "F{}R{}Z{}N{}T{}\r".format(function, range, autozero, digits, trigger)
        self.ser.write(bytearray(command, 'utf-8'))
        self.ser.flush()
        time.sleep(0.025)
        try:
            self.response = self.ser.readline()
            self.ser.flush()
            self.re = (float(self.response.decode('utf-8')))
            return self.re
        except ValueError:
            try:
                # self.ser.reset_input_buffer()
                # self.ser.reset_output_buffer()
                self.ser.flush()
                time.sleep(0.05)
                self.response = self.ser.readline()
                self.ser.flush()
                self.re = (float(self.response.decode('utf-8')))
                return self.re
            except ValueError:
                return '-6666'
    
    def readDCV(self, digits, range, trigger, autozero):
        self.rangeOffset = -3
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 5)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 5):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(1, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x'

    def readACV(self, digits, range, trigger, autozero):
        self.rangeOffset = -2
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 4)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 4):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(2, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x'
                    
    def read2WireOhms(self, digits, range, trigger, autozero):
        self.rangeOffset = 0
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 7)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 7):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(3, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x'                    

    def read4WireOhms(self, digits, range, trigger, autozero):
        self.rangeOffset = 0
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 7)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 7):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(4, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x'    
    def readDCA(self, digits, range, trigger, autozero):
        self.rangeOffset = -2
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 2)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 2):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(5, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x'    
    def readACA(self, digits, range, trigger, autozero):
        self.rangeOffset = -2
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    if ((range == 'A') or (1 <= int(range) <= 3)):
                        if(range == 'A'):
                            self.range = range
                        elif (1 <= int(range) <= 3):
                            self.range = int(range) + self.rangeOffset
                        
                        self.re = self.readCommand(6, self.range, autozero, digits, trigger)
                        return self.re
                    else:
                        return 'x' 

    def readXOhms(self, digits, trigger, autozero):
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                if ((autozero == 0) or (autozero == 1)):
                    self.re = self.readCommand(7, 'A', autozero, digits, trigger)
                    return self.re
    
    def readCurrentClamp(self, digits, trigger):
        if (3 <= digits <= 5):
            if (1 <= trigger <= 5):
                self.re = (float((self.readDCV(digits, 'A', trigger, 1))))/10
                return self.re
            else:
                return 'Invalid Trigger Parameter'
        else:
            return 'Invalid Digits'