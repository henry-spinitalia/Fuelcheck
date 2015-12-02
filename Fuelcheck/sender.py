# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

#  Referenze
# Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
# Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
from ControlUnit import ControlUnit


class CtrlUnitDatagramProtocol(DatagramProtocol):

    def __init__(self, options):

        ctrl_unit = ControlUnit()

        ctrl_unit.decode_ascii(options.message)
        ctrl_unit.encode_binary()

        self.packet = ctrl_unit.output_packet
        self.server_address = options.server

    def got_ip(self, ip):
        print "IP of '{}' is {}".format(self.server_address, ip)
        # All'avvio del protocollo si connette ed invia un datagramma
        self.transport.connect(ip, 9123)
        self.sendDatagram()

    def startProtocol(self):
        # Come prima cosa risolvo il nome
        reactor.resolve(self.server_address).addCallback(self.got_ip)

    def sendDatagram(self):
        self.transport.write(self.packet)

    def datagramReceived(self, datagram, host):
        # Risposta ricevuta dal server
        print 'Datagram received: ', repr(datagram)
        reactor.stop()

if __name__ == '__main__':

    # Inizializzo l'interprete dei parametri in ingresso
    parser = OptionParser()
    parser.add_option("-m", "--message", help="Messaggio MEX da consegnare al server", metavar="MEX",
                      action="store", type="string", dest="message")
    parser.add_option("-s", "--server", help="Indirizzo del server a cui inviare il messaggio", metavar="ADDR",
                      action="store", type="string", dest="server")
    (options, args) = parser.parse_args()
    if options.server is None:
        parser.error('Indirizzo del server non fornito')

    reactor.listenUDP(0, CtrlUnitDatagramProtocol(options))
    reactor.run()
