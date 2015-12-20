# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

# Qui andrebbe automatizzato:
# mkdir /usr/lib/python2.6/site-packages/zope
# touch /usr/lib/python2.6/site-packages/zope/__init__.py
# ln -s /usr/lib/python2.6/site-packages/zope.interface-3.5.1-py2.6-linux-x86_64.egg/zope/interface/
#       /usr/lib/python2.6/site-packages/zope/interface
# rsync -av --progress pritijen.webhop.org:/usr/lib/python2.6/optparse.py /usr/lib/python2.6/
#

# UDP
#   - A client can loose it's transport -> client.transport, None

# Referenze
#   Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
#   Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-
#   right-way/

# Debolezze di questa implementazione
#   - Necessaria una risoluzione DNS ad ogni invio
#     - Risolvo una volta al giorno
#     - In caso di errore annullo la cache
#   - Esiste un delay ed un carico CPU associato all'avvio dell'interprete Python
#   - Non è criptato
#   - Siamo indicativamente a 115 in RX e 143 in TX, ovvero 258, * 60 * 180 + * 550, ovvero 2.79MB/mese
#   - Da misure effettuate abbiamo:
#     - 71bytes DNS query
#     - 87bytes DNS response
#     - 84bytes UDP send
#     - 40bytes UDP response
#     - 282Bytes a transazione, 3.52MB/mese
#     - A questo si aggiunge il ping, pari a 28 * 60 * 180 + 550 * 30 * 28 = 0.72MB/mese
#     - Si puo' eliminare la risoluzione pari a 158 -> 1.71MB
#     - Questo porterebbe i consumi a 1.34MB/mese!!!


from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
from ControlUnit import ControlUnit
import sys
import binascii


class CtrlUnitDatagramProtocol(DatagramProtocol):

    ERR_NO_DNS_RESOLUTION = 1
    ERR_NO_SERVER_FOUND = 2
    ERR_UNABLE_TO_CONN = 3
    ERR_UNABLE_TO_SEND = 4
    ERR_UNABLE_DEC_ASCII = 5
    ERR_UNABLE_ENC_BINARY = 6
    ERR_UNABLE_TO_RESOLVE = 7
    ERR_UNABLE_TO_CONNECT = 8
    ERR_CONNECTION_LOST = 9

    def __init__(self, parameters):

        ctrl_unit = ControlUnit()
        self.fallback = False

        print "0. Decoding '{0}'".format(parameters.message)

        try:
            ctrl_unit.decode_ascii(parameters.message)
            print "  Decoded"
        except (ValueError, TypeError):
            print "  Error decoding"
            self.fallback = True

        try:
            ctrl_unit.encode_binary()
            print "  Encoding"
        except (ValueError, TypeError):
            print "  Error encoding"
            self.fallback = True

        # Prendo i parametri
        self.packet = ctrl_unit.output_packet
        self.input_data = parameters.message
        self.server_address = parameters.server

        print "  Encoded form '{0}'".format(binascii.hexlify(self.packet).upper())
        print "  Server {0}:9123".format(parameters.server)

        if parameters.outfile:
            self.output_enabled = True
            self.output_file = parameters.outfile
        else:
            self.output_enabled = False
            self.output_file = ""

        self.exit_code = 0           # Diciamo che va tutto bene
        self.timeout = 30            # Per qualsiasi operazione c'è un timeout di 20s
        self.timeout_id = None       # id del timeout

    def start_tout(self, resp, mex):

        print "  start tout '{0} / {1}'".format(mex, resp)
        self.timeout_id = reactor.callLater(self.timeout, self.stop_try, resp)

    def clear_tout(self):

        print "  clear tout"
        try:
            if self.timeout_id.active():
                self.timeout_id.cancel()
        except Exception, e:
            print("Error in clear_tout(): {0}".format(e.message))
            raise

    def got_ip(self, ip):

        # Per prima cosa elimino il timeout se presente
        self.clear_tout()

        print "2. Got IP"

        print "  IP of '{0}' is {1}".format(self.server_address, ip)
        # All'avvio del protocollo si connette ed invia un datagramma
        # Non è possibile sapere se c'e' un problema finchè non invio qls ( non è connesso!)
        # Ci pensa sendDatagradm ad impostare il timeout

        try:
            self.transport.connect(ip, 9123)
            print "  Connect to IP {0}".format(ip)
        except Exception, e:
            print("  Error, got {0} in got_ip()".format(e.message))
            self.stop_try(CtrlUnitDatagramProtocol.ERR_UNABLE_TO_CONN)
            raise

        try:
            if self.fallback:
                self.transport.write(self.input_data)
                print "  Send ascii '{0}'".format(binascii.hexlify(self.input_data).upper())
            else:
                self.transport.write(self.packet)
                print "  Send binary '{0}'".format(binascii.hexlify(self.packet).upper())
        except Exception, e:
            print("  Error, got {0} in got_ip()".format(e.message))
            self.stop_try(CtrlUnitDatagramProtocol.ERR_UNABLE_TO_SEND)
            raise

        self.start_tout(CtrlUnitDatagramProtocol.ERR_NO_SERVER_FOUND, "Connection and datagram send")

    def no_ip(self, failure):

        print "2. Unable to resolve server {0}".format(failure)
        self.stop_try(CtrlUnitDatagramProtocol.ERR_UNABLE_TO_RESOLVE)

    def connectionRefused(self):

        print "3. Unable to connect"
        self.stop_try(CtrlUnitDatagramProtocol.ERR_UNABLE_TO_CONNECT)

    def connectionLost(self):

        print "3. Connection lost"
        self.stop_try(CtrlUnitDatagramProtocol.ERR_CONNECTION_LOST)

    def startProtocol(self):

        print "1. Start protocol"

        # Come prima cosa risolvo il nome
        # TODO: devo unserire una cache nella risoluzione
        reactor.resolve(self.server_address).addCallbacks(self.got_ip, self.no_ip)
        self.start_tout(CtrlUnitDatagramProtocol.ERR_NO_DNS_RESOLUTION, "IP resolution")

    def stop_try(self, exit_code):

        print "  stop try ({0})".format(exit_code)

        self.exit_code = exit_code
        if self.transport:
            if self.transport.connected:
                self.transport.stopListening()

        if reactor.running:
            reactor.stop()

    def datagramReceived(self, datagram, host):

        # Per prima cosa elimino il timeout se presente
        self.clear_tout()

        print '5. Datagram received: ', repr(datagram)

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
