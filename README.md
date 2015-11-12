# Fuelcheck

Primo esperimento di utilizzo di GitHub. Vediamo di partire con il piede giusto.

## Installazione del virtualenv

Per tener traccia dei package installati per l'applicazione, e per separarla da altre installazioni, utilizzeremo il
`virtualenv`. In questo modo verra' creato un file `requirements.txt` che consente ad un altro utente di installarsi
con un solo comando tutte le librerie necessarie.

Attualmente siamo alla vesione 1.1.15; sono stati segnalati dei problemi durante la fase di rifornimento, per cui o la quantità di carburante immessa non coincide, o quando termina il rifornimento l'autista trova il tablet alla pagina principale e non può inserire i dati del rifornimento.

I difetti non sono riproducibili in laboratorio. Sono state fatte delle analisi, che hanno portato alla scoperta di alcuni problemi nel codice:

  - INVNUM: sh restituisce invalid number se si una printf %d con 08, 09, essendo viene interpretato come ottale
  - USBDIS: Se il tablet veniva staccato durante il rifornimento ripartiva dalla pagina iniziale
  - BACKON:Nella pagina del rifornimento era rimasto attivo il tasto back che portava alla pagina main
  - PPPREBOOT: Se non si riesce a spegnere il demone pppd se attivo, il sistema si riavvia cancellando il rifornimento
  - MDMREBOOT: Se non riesce a spegnere il modem, il sistema si riavvia cancellando il rifornimento
  - EMERGMEX: Il messaggio con riavvio con veniva inviato
  - WAITRST: Dopo lo shutdown il sistema continuava a funzionare
  - CNTMUL: Possono essere avviate istanze multiple del contatore di impulsi, invalidando il risultato
  - EVTNUM: Il numero di evento veniva considerato certe volte ottale

Al momento queste sono state le cose corrette, ma non sappiamo se siano risolutive. I punti del firmware modificati, che devono essere quindi ricontrollati sono:

  - Il calcolo della distanza percorsa per il controllo del numero di satelliti e la stampa delle info (INVNUM)
  - Il calcolo del checksum NMEA
  - La lettura di un valore ADC
  - La lettura dei valori dal canale V_ADC_AN2
  - Il contatore di impulsi (INVNUM, CNTMUL)
  - Il gestore del servizio GPS (INVNUM)
  - Il gestore di IO (INVNUM)
  - Il processo principale (INVNUM, PPPREBOOT, MDMREBOOT, EMERMEX, WAITRST)
  - 
  
