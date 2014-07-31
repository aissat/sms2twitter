from __future__ import print_function
import threading
import serial
from messaging.sms import SmsDeliver
import settings


class MessageReader(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.message_received = False
        self.init_modem()

    def sendcmd(self, command):
        self.dongle.write('AT' + command + '\r')

    def init_modem(self):
        self.dongle = serial.Serial(settings.gsmmodem, 115200)
        self.sendcmd('^HS=0,0')  # HandShake
        self.sendcmd('^BOOT=88572452,0')  # TODO: the ID should come from the response to the HS
        self.sendcmd('+CNMI=1,2,0,1,1')  # do not store text messages

    def process(self, data):
        if self.message_received:
            message = data.decode('utf-8').strip()
            sms = SmsDeliver(message)
            if sms.number in settings.whitelist:
                self.queue.put(sms.text)
            else:
                print("Got sms from: " + sms.number + "\n" + sms.text + '\n')
            self.message_received = False
        else:
            line = data.decode('utf-8').strip().split()
            if len(line) > 1 and 'CMT' in line[0].upper():
                self.message_received = True

    def run(self):
        while True:
            data = self.dongle.readline()
            self.process(data)
