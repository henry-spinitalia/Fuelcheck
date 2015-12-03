# -*- coding: utf-8 -*-

# Questa classe rimane in ascolto su una porta, per messaggi codificati, li decomprime, li invia al MULE, riceve le
# risposte e le restituisce alle centraline
#
#        +------+                   +------------+                   +------+
#        | BBox |------------------>|     Me     |------------------>| MULE |
#        |      |<------------------|            |<------------------|      |
#        +------+                   +------------+                   +------+
#


from twisted.internet.protocol import DatagramProtocol
from twisted.web.client import getPage
from twisted.internet import reactor
import binascii
from ControlUnit import ControlUnit

class BBoxDecoder(DatagramProtocol):
    """Riceve un messaggio compresso dalle centraline e lo spedisce al server"""

    C_TXS_URL = "http://151.1.80.42/src/api/v1?rawData="

    def __init__(self):

        self.ctrl_unit = ControlUnit()

        print "Starting ControlUnit binary receiver v0.1a"

    def print_page(self, result, host, port):
        print "  MULE say {}".format(result)
        self.transport.write(result, (host, port))

    @staticmethod
    def print_error(failure):
        print "  MULE say EPIC FAIL! {} - {}".format(sys.stderr, failure)

    def datagramReceived(self, data, (host, port)):

        # Evento: mi è appena arrivato un pacchetto binario dalle centraline
        print("Received {} from {}:{}".format(binascii.hexlify(data), host, port))

        # La decodifico da binario in variabili interne
        self.ctrl_unit.decode_binary(data)

        # Se i dati sono validi
        if self.ctrl_unit.check_values():

            # Li codifico in ASCII
            self.ctrl_unit.encode_ascii()
            print("  Coded {}".format(self.ctrl_unit.output_packet))

            # Li invio al server MULE, e quando sarà pronta la risposta faccio chiamare printPage o printError
            d = getPage(self.C_TXS_URL + self.ctrl_unit.output_packet)
            d.addCallback(self.print_page, host, port)
            d.addErrback(self.print_error)
            # d.addBoth(stop)

if __name__ == '__main__':
    reactor.listenUDP(9123, BBoxDecoder())
    reactor.run()
