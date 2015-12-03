# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

# Qui andrebbe automatizzato:
# mkdir /usr/lib/python2.6/site-packages/zope
# touch /usr/lib/python2.6/site-packages/zope/__init__.py
# ln -s /usr/lib/python2.6/site-packages/zope.interface-3.5.1-py2.6-linux-x86_64.egg/zope/interface/
#       /usr/lib/python2.6/site-packages/zope/interface
# rsync -av --progress pritijen:/usr/lib/python2.6/optparse.py /usr/lib/python2.6/
#


#  Referenze
# Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
# Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
from ControlUnit import ControlUnit
import sys


class CtrlUnitDatagramProtocol(DatagramProtocol):

    def __init__(self, options):

        ctrl_unit = ControlUnit()

        ctrl_unit.decode_ascii(options.message)
        ctrl_unit.encode_binary()

        self.packet = ctrl_unit.output_packet
        self.server_address = options.server
        self.output_file = options.outfile

    def got_ip(self, ip):
        print "IP of '{0}' is {1}".format(self.server_address, ip)
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
        with open(self.output_file, 'w+') as f:
            f.write(datagram)
        reactor.stop()

if __name__ == '__main__':

    # Inizializzo l'interprete dei parametri in ingresso
    parser = OptionParser()
    parser.add_option("-m", "--message", help="Messaggio MEX da consegnare al server", metavar="MEX",
                      action="store", type="string", dest="message")
    parser.add_option("-s", "--server", help="Indirizzo del server a cui inviare il messaggio", metavar="ADDR",
                      action="store", type="string", dest="server")
    parser.add_option("-o", "--output_file", help="File dove salvare l'output del comando", metavar="OUT",
                      action="store", type="string", dest="outfile")
    (options, args) = parser.parse_args()
    if options.server is None:
        parser.error('Indirizzo del server non fornito')

    reactor.listenUDP(0, CtrlUnitDatagramProtocol(options))
    reactor.run()
    sys.exit(0)
