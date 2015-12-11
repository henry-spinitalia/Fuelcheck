# -*- coding: utf-8 -*-

# Questa classe rimane in ascolto su una porta, per messaggi codificati, li decomprime, li invia al MULE, riceve le
# risposte e le restituisce alle centraline
#
#        +------+                   +------------+                   +------+
#        | BBox |------------------>|     Me     |------------------>| MULE |
#        |      |<------------------|            |<------------------|      |
#        +------+                   +------------+                   +------+
# http://krondo.com/wp-content/uploads/2009/08/twisted-intro.html

from twisted.internet.protocol import DatagramProtocol
from twisted.web.client import getPage
from twisted.internet import reactor
import binascii
import calendar
import time
import os
import sys
from ControlUnit import ControlUnit


class BBoxDecoder(DatagramProtocol):
    """Riceve un messaggio compresso dalle centraline e lo spedisce al server"""

    C_TXS_URL = "http://151.1.80.42/src/api/v1?rawData="
    C_OUT_PATH = "/mnt/nas/temp/Fuelcheck/"
    C_OUT_FILE = "/mnt/nas/temp/Fuelcheck/fuelcheck_traslator.log"

    def __init__(self):

        # Istanzio il traduttore
        self.ctrl_unit = ControlUnit()

        # Controllo se sia il caso di salvare nel log ( non lo faccio se provo il programma in locale )
        if os.path.isdir(self.C_OUT_PATH):
            self.can_log = True
            print("Log path found")
        else:
            self.can_log = False
            print("Log path not found")

        # Dichiaro tutte le variabili necessarie a mantenere l'elenco delle centraline ed i totali di trasmissione
        self.report = {
            'imei': "",
            'stats': {
                'dati_tx': 0L,
                'dati_rx': 0L,
                'transazioni_corrette': 0,
                'transazioni_errate': 0
            }
        }

        print "Starting ControlUnit binary receiver v0.1a"

    def log_data(self, transaction):

        # Aggiungo le parti mancanti
        if 'imei' not in transaction:
            transaction['imei'] = 0
        if 'event_date' not in transaction:
            transaction['event_date'] = 0
        if 'event' not in transaction:
            transaction['event'] = 0x99
        if 'mule_response' not in transaction:
            transaction['mule_response'] = "5A????"
        if 'output_ascii_datagram' not in transaction:
            transaction['output_ascii_datagram'] = "A5????"
        if 'input_binary_datagram' not in transaction:
            transaction['input_binary_datagram'] = ""
        if 'host' not in transaction:
            transaction['host'] = ""
        if 'port' not in transaction:
            transaction['port'] = ""

        if 'error' in transaction:
            print "{},{}".format(
                time.strftime("%d %b %H:%M:%S", time.gmtime(transaction['time_of_arrival'])),
                transaction['error']
            )
        else:
            print "{} - {} - {:15d} - {:02X} - {} - {}".format(
                time.strftime("%d %b %H:%M:%S", time.gmtime(transaction['time_of_arrival'])),
                time.strftime("%d %b %H:%M:%S", time.gmtime(transaction['event_date'])),
                transaction['imei'],
                transaction['event'],
                transaction['mule_response'],
                transaction['output_ascii_datagram']
            )

        if 'error' not in transaction:
            transaction['error'] = ""

        if self.can_log:
            with open(self.C_OUT_FILE, 'a') as f:
                f.write(
                    "{};{:15d};{};{:02X};{};{};{};{};{};{}\n".format(
                        time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(transaction['time_of_arrival'])),
                        transaction['imei'],
                        time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(transaction['event_date'])),
                        transaction['event'],
                        transaction['mule_response'],
                        transaction['output_ascii_datagram'],
                        transaction['error'],
                        transaction['input_binary_datagram'],
                        transaction['host'],
                        transaction['port']
                    )
                )
                f.flush()

    def url_data_received(self, result, transaction):
        transaction['mule_response'] = result
        self.transport.write(result, (transaction['host'], transaction['port']))
        self.log_data(transaction)

    def url_error(self, failure, transaction):
        # TODO: Se il MULE risponde con un errore, dobbiamo riportarlo alla centralina
        transaction['error'] = "Errore di comunicazione con il MULE; ({})".format(failure)
        self.log_data(transaction)

    def datagramReceived(self, data, (host, port)):

        # Evento: mi è appena arrivato un pacchetto binario dalle centraline

        # Lo memorizzo in un dizionario
        transaction = dict()
        transaction['time_of_arrival'] = calendar.timegm(time.gmtime())
        transaction['input_binary_datagram'] = binascii.hexlify(data).upper()

        # La decodifico da binario in variabili interne
        try:
            self.ctrl_unit.decode_binary(data)
        except ValueError as e:
            transaction['error'] = "Errore di conversione binary ({}, {})".format(
                e.message,
                transaction['input_binary_datagram']
            )
            self.log_data(transaction)
            return
        except TypeError as e:
            transaction['error'] = "Errore di conversione binary ({}, {})".format(
                e.message,
                transaction['input_binary_datagram']
            )
            self.log_data(transaction)
            return

        # Se i dati sono validi
        if self.ctrl_unit.check_values():

            transaction['imei'] = self.ctrl_unit.imei
            transaction['event'] = self.ctrl_unit.event
            transaction['event_date'] = calendar.timegm(time.gmtime(self.ctrl_unit.unixtime))
            transaction['host'] = host
            transaction['port'] = port

            # Li codifico in ASCII
            try:
                self.ctrl_unit.encode_ascii()
            except ValueError as e:
                transaction['error'] = "Errore di conversione in ascii ({}, {})".format(
                    e.message,
                    transaction['input_binary_datagram']
                )
                self.log_data(transaction)
                return
            except TypeError as e:
                transaction['error'] = "Errore di conversione in ascii ({}, {})".format(
                    e.message,
                    transaction['input_binary_datagram']
                )
                self.log_data(transaction)
                return

            transaction['output_ascii_datagram'] = self.ctrl_unit.output_packet

            # Li invio al server MULE, e quando sarà pronta la risposta faccio chiamare printPage o printError
            d = getPage(self.C_TXS_URL + self.ctrl_unit.output_packet)
            d.addCallback(self.url_data_received, transaction)
            d.addErrback(self.url_error, transaction)

        else:
            transaction['error'] = "Valori errati dopo l'estrazione ({})".format(e.message)
            self.log_data(transaction)


if __name__ == '__main__':

    # Impostiamo il reattore in ascolto sulla porta 9123. L'esecuzione si blocca su run(), e l'unico evento possibile
    # sarà la ricezione di un datagramma via UDP da parte del reattore e la chiamata del metodo datagramReceived()
    reactor.listenUDP(9123, BBoxDecoder())
    reactor.run()

    # Restituisco il corretto valore
    sys.exit(0)
