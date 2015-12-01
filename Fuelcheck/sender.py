# -*- coding: utf-8 -*-

# Questa classe al momento riceve in ingresso come parametro a linea di comando una stringa codificata secondo l'attuale
# protocollo, la comprime, la invia al server.

#  Referenze
# Unittest - https://twistedmatrix.com/documents/current/core/howto/trial.html
# Opensourcing in the right way - https://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from optparse import OptionParser
from BinaryProtocol import BinaryProtocol
from AsciiProtocol import AsciiProtocol


class CtrlUnitDatagramProtocol(DatagramProtocol):

    def __init__(self, options):

        b_proto = BinaryProtocol()
        a_proto = AsciiProtocol()

        a_proto.decode(options.message)

        # Al momento non ho alternative
        b_proto.imei = a_proto.imei
        b_proto.driver = a_proto.driver
        b_proto.event = a_proto.event
        b_proto.unixtime = a_proto.unixtime
        b_proto.sat = a_proto.sat
        b_proto.lat = a_proto.lat
        b_proto.lon = a_proto.lon
        b_proto.speed = a_proto.speed
        b_proto.gasoline_r = a_proto.gasoline_r
        b_proto.gasoline_l = a_proto.gasoline_l
        b_proto.gasoline_f = a_proto.gasoline_f
        b_proto.vin = a_proto.vin
        b_proto.vbatt = a_proto.vbatt
        b_proto.input_gasoline_r = a_proto.input_gasoline_r
        b_proto.input_gasoline_l = a_proto.input_gasoline_l
        b_proto.input_gasoline_f = a_proto.input_gasoline_f
        b_proto.input_gasoline_tot = a_proto.input_gasoline_tot
        b_proto.cup_r = a_proto.cup_r
        b_proto.cup_l = a_proto.cup_l
        b_proto.cup_f = a_proto.cup_f
        b_proto.engine = a_proto.engine
        b_proto.alarm = a_proto.alarm
        b_proto.cup_lock = a_proto.cup_lock
        b_proto.distance_travelled = a_proto.distance_travelled

        b_proto.encode()
        self.packet = b_proto.output_packet
        self.server_address = options.server

    def gotIP(self, ip):
        print "IP of '{}' is {}".format(self.server_address, ip)
        # All'avvio del protocollo si connette ed invia un datagramma
        self.transport.connect(ip, 9123)
        self.sendDatagram()

    def startProtocol(self):
        # Come prima cosa risolvo il nome
        reactor.resolve(self.server_address).addCallback(self.gotIP)

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
