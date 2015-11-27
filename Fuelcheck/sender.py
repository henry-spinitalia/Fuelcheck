# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

#  Referenze
# Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
# Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
import BinaryProtocol

class CtrlUnitDatagramProtocol(DatagramProtocol, BinaryProtocol):

    def __init__(self):

        self.parser = OptionParser()
        self.parser.add_option("-m", "--message", dest="filename", help="send the message MSG", metavar="MSG")
        self.parser.add_option("-s", "--server", dest="server", help="send the message to server ADDR", metavar="ADDR")
        self.Packets = 10
        self.server_address = 127.0.0.1

    def startProtocol(self):
        # All'avvio del protocollo si connette ed invia un datagramma
        self.transport.connect(self.server_address, 8000)
        self.sendDatagram()

    def sendDatagram(self):
        # Al decimo invio spegne il reattore
        if self.Packets >= 0:
            self.transport.write(self.pack_data())
            self.Packets -= 1
        else:
            reactor.stop()

    def datagramReceived(self, datagram, host):
        # Risposta ricevuta dal server
        print 'Datagram received: ', repr(datagram)
        self.sendDatagram()

if __name__ == '__main__':
    reactor.listenUDP(0, CtrlUnitDatagramProtocol())
    reactor.run()
