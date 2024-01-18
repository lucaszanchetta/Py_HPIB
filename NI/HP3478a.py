import pyvisa
import time

class HP3478a:
    # Class variables for function, trigger, and range names can remain as in your original code

    def __init__(self, gpibAddr):
        print('-- Initializing Multimeter --')
        self.gpibAddr = 'GPIB0::{}::INSTR'.format(gpibAddr)
        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(self.gpibAddr)
        print('-- Connected to Multimeter --')

    def send_command(self, command):
        self.instr.write(command)

    def read_response(self):
        try:
            response = self.instr.read()
            return response.strip()
        except pyvisa.VisaIOError:
            return '-6666'

    def readCommand(self, function, range, autozero, digits, trigger):
        command = "F{}R{}Z{}N{}T{}".format(function, range, autozero, digits, trigger)
        self.send_command(command)
        response = self.read_response()
        try:
            return float(response)
        except ValueError:
            return '-6666'

    def readDCV(self, digits, range, trigger, autozero):
        self.send_command("F1R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def readACV(self, digits, range, trigger, autozero):
        self.send_command("F2R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def read2WireOhms(self, digits, range, trigger, autozero):
        self.send_command("F3R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def read4WireOhms(self, digits, range, trigger, autozero):
        self.send_command("F4R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def readDCA(self, digits, range, trigger, autozero):
        self.send_command("F5R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def readACA(self, digits, range, trigger, autozero):
        self.send_command("F6R{}Z{}N{}T{}".format(range, autozero, digits, trigger))
        return self.read_response()

    def readXOhms(self, digits, trigger, autozero):
        self.send_command("F7RAZ{}N{}T{}".format(autozero, digits, trigger))
        return self.read_response()

    def readCurrentClamp(self, digits, trigger):
        response = float(self.readDCV(digits, 'A', trigger, 1))
        return response / 10

# Usage example
# meter = HP3478a(22)
# print("DC Voltage: ", meter.readDCV(5, 'A', 1, 1))
# Add additional print statements for other methods as needed
