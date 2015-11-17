# Fuelcheck

Primo esperimento di utilizzo di GitHub. Vediamo di partire con il piede giusto.

## Installazione del virtualenv

Per tener traccia dei package installati per l'applicazione, e per separarla da altre installazioni, utilizzeremo il
`virtualenv`. In questo modo verra' creato un file `requirements.txt` che consente ad un altro utente di installarsi
con un solo comando tutte le librerie necessarie.

## Organizzazione delle classi

Il sistema al momento si compone di:

  * Un sistema di acquisizione dati mobile (rdq - remote data aquisition) dotato di batteria, gps, gsm, ed una serie di
    I/O digitali ed analogici
  * Un sistema di raccolta dati provenienti da diversi sensori (cds - centralized data storage)

Per quanto riguarda l'organizzazione delle classi, ci sono alcune parti in comune, come la codifica e decodifica delle
informazioni, e la traduzione da e verso il MULE-ESB. Altra parti invece sono assolutamente specifiche:

  * fuelcheck/BinaryProtocol: rappresenta la codifica e decodifica dell'informazione binaria
  * fuelcheck/AsciiProtocol: rappresenta la codifica e decodifica dell'informazione ascii
  * fuelcheck/CdsServer: avviandola si mette in ascolto per ricevere messaggi
  * fuelcheck/RqdFirmware: avviandola prende come parametro un messaggio, lo codifica e lo invia




