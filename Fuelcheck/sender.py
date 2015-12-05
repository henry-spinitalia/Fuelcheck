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

# UDP
#   - A client can loose it's transport -> client.transport, None

# Referenze
#   Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
#   Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-
#   right-way/
#
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
from ControlUnit import ControlUnit
import sys


class CtrlUnitDatagramProtocol(DatagramProtocol):

    def __init__(self, parameters):

        ctrl_unit = ControlUnit()

        try:
            ctrl_unit.decode_ascii(options.message)
        except (ValueError, TypeError):
            self.stop_try(1)

        try:
            ctrl_unit.encode_binary()
        except (ValueError, TypeError):
            self.stop_try(2)

        # Prendo i parametri
        self.packet = ctrl_unit.output_packet
        self.server_address = parameters.server

        if parameters.outfile:
            self.output_enabled = True
            self.output_file = parameters.outfile
        else:
            self.output_enabled = False
            self.output_file = ""

        self.exit_code = 0           # Diciamo che va tutto bene
        self.timeout = 5             # Per qualsiasi operazione c'è un timeout di 20s
        self.timeout_id = None       # id del timeout

    def start_tout(self, resp, mex):

        print "Start tout {0}".format(mex)
        self.timeout_id = reactor.callLater(self.timeout, self.stop_try, resp)

    def clear_tout(self):

        print "Clear tout"
        try:
            if self.timeout_id.active():
                self.timeout_id.cancel()
        except Exception, e:
            print("Got {0} in datagramReceived().".format(e.message))
            pass

    def got_ip(self, ip):

        print "Got IP"

        # Per prima cosa elimino il timeout se presente
        self.clear_tout()

        print "IP of '{0}' is {1}".format(self.server_address, ip)
        # All'avvio del protocollo si connette ed invia un datagramma
        # Non è possibile sapere se c'e' un problema finchè non invio qls ( non è connesso!)
        # Ci pensa sendDatagradm ad impostare il timeout
        self.transport.connect(ip, 9123)
        self.send_datagram()
        self.start_tout(3, "Connection and datagram send")

    def no_ip(self, failure):

        print "Unable to resolve server {0}".format(failure)
        self.stop_try(1)

    def connectionRefused(self):

        print "Unable to connect"
        self.stop_try(4)

    def connectionLost(self):

        print "Connection lost"
        self.stop_try(4)

    def startProtocol(self):

        print "Start protocol"

        # Come prima cosa risolvo il nome
        # TODO: devo unserire una cache nella risoluzione
        reactor.resolve(self.server_address).addCallbacks(self.got_ip, self.no_ip)
        self.start_tout(5, "IP resolution")

    def send_datagram(self):

        print "Send datagram"

        try:
            self.transport.write(self.packet)
        except Exception, e:
            print("Got {0} in send_datagram()".format(e.message))
            self.stop_try(3)

    def stop_try(self, exit_code):

        print "Stop try"

        self.exit_code = exit_code
        if self.transport:
            if self.transport.connected:
                self.transport.stopListening()

        if reactor.running:
            reactor.stop()

    def datagramReceived(self, datagram, host):

        print 'Datagram received: ', repr(datagram)

        # Per prima cosa elimino il timeout se presente
        self.clear_tout()

        # Risposta ricevuta dal server
        if self.output_enabled:
            with open(self.output_file, 'w+') as f:
                f.write(datagram)
        self.stop_try(0)

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
    elif options.message is None:
        parser.error('Messaggio non fornito')

    # Creo il protocollo
    udp_proto = CtrlUnitDatagramProtocol(options)

    # TODO: Possono essere restituiti errori?
    reactor.listenUDP(0, udp_proto)
    reactor.run()

    # Restituisco il corretto valore
    sys.exit(udp_proto.exit_code)
