import pyvisa
import time

class HP3488a:

    def __init__(self, gpibAddr):
        print('-- Initializing Switch --')
        self.gpibAddr = 'GPIB0::{}::INSTR'.format(gpibAddr)
        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(self.gpibAddr)
        print('-- Connected to Switch --')

    def writeCommand(self, command):
        self.instr.write(command)

    def readResponse(self):
        try:
            response = self.instr.read().strip()
            return response
        except pyvisa.VisaIOError:
            return 'Error in reading response'

    def get_cards(self):
        cards = []
        for i in range(1, 6):
            self.writeCommand('CTYPE {}'.format(i))
            response = self.readResponse()
            cards.append(response)
        return cards

    def card_monitor(self, slot):
        if 1 <= slot <= 5:
            self.writeCommand('CMON {}'.format(slot))

    def scan_list(self, list):
        self.writeCommand('SLIST {}'.format(list))

    def step(self):
        self.writeCommand('STEP')

    def display_print(self, string):
        if len(string) > 12:
            string = string[:12]
        self.writeCommand('DISP {}'.format(string.upper()))

    def display_toggle(self, enable):
        if enable == 1:
            self.writeCommand('DON')
        elif enable == 0:
            self.writeCommand('DOFF')

    def reset(self):
        self.writeCommand('CLEAR')

# Usage example
# switch = HP3488a(9)
# cards = switch.get_cards()
# print("Cards: ", cards)
# Add additional calls to other methods as needed
