import serial
import time

class HP3488a:

    def __init__(self, ser, gpibAddr):
        print('-- Initializing Switch --')
        self.gpibAddr = gpibAddr
        self.ser = ser
        self.set_address()
        self.ser.flush()
        print('-- Connected to Switch --')

    def set_address(self):
        self.ser.flush()
        self.ser.write(bytearray('++addr {}\r\n'.format(self.gpibAddr), 'utf-8'))
        self.ser.flush()
        time.sleep(0.5)
        
    def get_cards(self):
        self.cards = []
        self.ser.write(bytearray('++auto 1\r\n', 'utf-8'))
        self.ser.flush()
        time.sleep(0.1)
        for i in range(1,6):
            self.ser.write(bytearray('CTYPE {}\r\n'.format(i), 'utf-8'))
            self.ser.flush()
            time.sleep(0.1)
            self.response = self.ser.readline().decode('utf-8')
            self.ser.flush()
            self.card = self.response.strip('\r\n')
            self.cards.append(self.card)
            time.sleep(0.1)
        return self.cards

    def card_monitor(self, slot):
        self.set_address()
        if (1 <= slot <= 5):
            self.ser.write(bytearray('CMON {}\r\n'.format(slot), 'utf-8'))
            self.ser.flush()
            time.sleep(0.05)

    def scan_list(self, list):
        self.set_address()
        self.ser.write(bytearray('SLIST {}\r\n'.format(list), 'utf-8'))
        self.ser.flush()
        time.sleep(0.05)

    def step(self):
        self.set_address()
        self.ser.write(bytearray('STEP\r\n', 'utf-8'))
        self.ser.flush()
        time.sleep(0.05)

    def display_print(self, string):
        if (len(string) > 12):
            string = string[:12]
        self.ser.write(bytearray('DISP {}\r\n'.format(string.upper()), 'utf-8'))
        self.ser.flush()
        time.sleep(0.1)

    def display_toggle(self, enable):
        if (enable == 1):
            self.ser.write(bytearray('DON\r\n', 'utf-8'))
            self.ser.flush()
            time.sleep(0.05)
        elif (enable == 0):
            self.ser.write(bytearray('DOFF\r\n', 'utf-8'))
            self.ser.flush()
            time.sleep(0.05)

    def reset(self):
        self.ser.write(bytearray('CLEAR\r\n', 'utf-8'))
        self.ser.flush()
        time.sleep(0.05)


def initialize_serial_connection(port, baud):
    ser = serial.Serial(port, baud)
    ser.timeout = 1
    return ser
