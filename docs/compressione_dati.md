# Introduzione alle definizioni di una struct

Il primo carattere indica se presente l'ordine dei bytes come little-endian, tra i vari disponibili:

   Character  | Byte order               | Size      | Alignment
  ------------|--------------------------|-----------|------------
       @      |  native                  | native    | native
       =      |  native                  | standard  | none
       <      |  little-endian           | standard  | none
       >      |  big-endian              | standard  | none
       !      |  network (= big-endian)  | standard  | none

Poi vengono specificate le codifiche dei campi, tra le possibili del python, tramite un singolo carattere di formato:

	 Format  | C Type         | Python type         | Standard size
  -----------|----------------|---------------------|---------------
	    x    | pad byte       | no value            |
		c    | char           | string of length 1  | 1
		b    | signed char    | integer             | 1
		B    | unsigned char  | integer             | 1
		?    | _Bool          | bool                | 1
		h    | short          | integer	            | 2
		H    | unsigned short | integer             | 2
		i    | int            | integer             | 4
		I    | unsigned int   | integer             | 4
		l    | long           | integer             | 4
		L    | unsigned       | long integer        | 4
		q    | long long      | integer             | 8
		Q    | unsigned long  | long integer        | 8
		f    | float          | float               | 4
		d    | double         | float               | 8
		s    | char[]         | string              |
		p    | char[]         | string              |
		P    | void *         | integer             |

# Formato della struttura dati

I dati andranno codificati in una struttura al fine di diminuirne il peso. Premesso il documento originale che elenca
il protocollo finora utilizzato, vengono applicate le seguenti considerazioni:

	* La dimensione minima di un pacchetto non frammentato su internet è di 576bytes. A questi vanno sottratti l'header
	  IP che puo' raggiungere 60 bytes. Questo è particolarmente importante per l'UDP, al fine di non dover riordinare
	  i pacchetti in ingresso.
	* Il campo HDR, che ha un valore fisso pari a A5, non ha motivo di esistere, e viene eliminato.
	* La lunghezza LEN è un controllo, e al momento va bene che sia al massimo di 1 byte (1 byte - B)
	* La versione VER al momento non è molto utilizzato, ma servirà per differenziare il tipo di informazioni inviate;
	  anche questo campo va bene che sia lungo un byte senza segno (1 byte - B)
	* L'IMEI viene comunemente spezzato in tre interi senza segno da 2 bytes (0-65535), quindi 353681048805535 diventa
	  35368, 10488, 05535 (6 bytes - HHH)
	* Il numero di autisti DRVN massimo è di 9999, quindi anche questo diventa un intero senza segno a 2 bytes
	  (2 bytes - H)
	* Il codice dell'evento EVTN è un byte senza segno. Al momento non tutti i pacchetti contengono le stesse
	  informazioni. Possiamo in futuro migliorare inviando per ciascun evento solo le informazioni cambiate o quelle di
	  interesse per l'evento stesso (1 byte - B).
	* Per la data dei campi DATE e TIME, conviene trasmettere lo UNIXTIME in UTC, ovvero i secondi dal 1 gennaio 1970,
	  in UTC. Per noi basta un intero senza segno da 4 bytes ( 4 bytes - I )
	* Il numero dei satelliti GSAT, al momento è un byte senza segno (1 byte - B)
	* Il campo LAT lo memorizziamo come float a 4byte, con una precisione di 10mm, vedi appendice A (4 bytes - f)
	* Il campo LON lo memorizziamo come float a 4byte, con una precisione di 10mm, vedi appendice A (4 bytes - f)
	* La velocità SPD, la rappresentiamo moltiplicata per 10, e salvata in due bytes senza segno (2 bytes - H)
	* I campi che indicano i litri presenti nei serbatoi, FTR, FTL, FTF, vengono moltiplicati per 10 e salvati in 2
	  bytes senza segno ciascuno (6 bytes - HHH)
	* Le tensione del mezzo MBAT, è moltiplicata per 10, e salvata in due bytes senza segno ciascuna (2 bytes - HH)
	* Le tensione della batteria interna BBAT, è moltiplicate per 100, e salvata in due bytes senza segno ciascuna
	  (2 bytes - HH)
	* I litri immessi nei serbatoi, FCRM, FCLM, FCFM, vengono moltiplicati per 10 e salvati in 2 bytes senza segno
	  ciascuno (6 bytes - HHH)
	* I litri di carburante immesso dichiarati, sono salvati come interi in 2 bytes senza segno (2 bytes - HH)
	* Lo stato degli ingressi viene rappresentato con un byte, codificato a bit (1 byte - B). Ogni ingresso occupa due
	  bit, il primo è lo stato 0-1, il secondo l'eventuale Fail.
	* Lo stato delle uscite viene rappresentato con un byte, codificato a bit (1 byte - B)
	* La distanza percorsa HSZZ, la rappresentiamo moltiplicata per 10, e salvata in due bytes senza segno (2 bytes - H)
	* Se il messaggio è un rifornimento (EVTN = 13), allora viene accodato DIST, un byte che indica il distributore
	  (1 byte - B)
	* Se viene inviato un messaggio di testo (EVTN = 14), viene accodato il messaggio come stringa di lunghezza
	  variabile terminata con $. La rappresentiamo come stringa (? bytes - s).

In risposta all'invio dell'evento, il MULE-ESB ci comunica l'avventa ricezione, ci segnala un errore nel formato dei
dati inviati, oppure ci aggiunge altre informazioni. Le nostre note circa la risposta che andrà anch'essa compressa
sono le seguenti:

	* Il campo HDR che è fisso non serve quindi lo eliminiamo.
	* Il campo LEN è un controllo, e al momento va bene che sia al massimo di 1 byte (1 byte - B)
	* Il campo di risposta RSP è lungo 1 byte (1 byte - B)
	* Il campo opzionale che indica dove è stato riscontrato un errore nei dati inviati OEFL è lungo 1 byte (1 byte - B)
	* Il campo opzionale che descrive le informazioni accodate ONDT è lungo 1 byte (1 byte - B)
	* Il campo opzionale contente le informazioni aggiuntive OPLD dipende dal tipo di informazioni inviate
	  * Se si tratta del fattore di conversione Litri/Volt del serbatoio sinistro (ONDT=1), è un float (4 bytes - f)
	  * Se si tratta del fattore di conversione Litri/Volt del serbatoio destro (ONDT=2), è un float (4 bytes - f)
	  * Se si tratta del fattore di conversione Litri/Volt del serbatoio frigo (ONDT=3), è un float (4 bytes - f)
	  * Se si tratta del fattore di conversione Impulsi/Litro del serbatoio sinistro (ONDT=4), è un float (4 bytes - f)
	  * Se si tratta del fattore di conversione Impulsi/Litro del serbatoio destro (ONDT=5), è un float (4 bytes - f)
	  * Se si tratta del fattore di conversione Impulsi/Litro del serbatoio frigo (ONDT=6), è un float (4 bytes - f)
	  * Se si tratta del nome dell'autista (ONDT=7), è un intero senza segno ed una stringa (2+? bytes - Hs)
	  * Se si tratta di un codice antifurto (ONDT=8), è un long senza segno (4 bytes - L)
	  * Se si tratta di un codice manutentore (ONDT=9), è un long senza segno (4 bytes - L)
	  * Se si tratta di un codice amministratore (ONDT=10), è un long senza segno (4 bytes - L)
	  * Se si tratta di un codice pin (ONDT=11), è un long senza segno (4 bytes - L)
	  * Se si tratta della quantità di carburante presente in sede (ONDT=12), è un long senza segno (4 bytes - L)
	  * Se si tratta di un messaggio di risposta alla chat (ONDT=13), è una stringa (? bytes - s)

# Codifica dei pacchetti

## Pacchetto normale

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ VER               (    1 byte  - B  )
	|||+++--------------------- IMEI              (3 x 2 bytes - HHH)
	||||||+-------------------- DRVN              (    2 bytes - H  )
	|||||||+------------------- EVTN              (    1 byte  - B  )
	||||||||+------------------ UTC_Unixtime      (    4 bytes - I  )
	|||||||||+----------------- GSAT              (    1 byte  - B  )
	||||||||||+---------------- LAT               (    4 bytes - f  )
	|||||||||||+--------------- LON               (    4 bytes - f  )
	||||||||||||+-------------- SPD               (    2 bytes - H  )
	|||||||||||||+++----------- Gasoline LRF      (3 x 2 bytes - HHH)
	||||||||||||||||+---------- MBAT              (    2 bytes - H  )
	|||||||||||||||||+--------- BBAT              (    2 bytes - H  )
	||||||||||||||||||+++------ In gasoline LRF   (3 x 2 bytes - HHH)
	|||||||||||||||||||||+----- In gasoline TOT   (    2 bytes - H  )
	||||||||||||||||||||||+---- Inputs Bitpacked  (    1 byte  - B  )
	|||||||||||||||||||||||+--- Outputs Bitpacked (    1 byte  - B  )
	||||||||||||||||||||||||+-- HSZZ              (    2 bytes - H  )
	|||||||||||||||||||||||||
	<BBHHHHBIBffHHHHHHHHHHBBH

'''

## Pacchetto di rifornimento

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ VER               (    1 byte  - B  )
	|||+++--------------------- IMEI              (3 x 2 bytes - HHH)
	||||||+-------------------- DRVN              (    2 bytes - H  )
	|||||||+------------------- EVTN              (    1 byte  - B  )
	||||||||+------------------ UTC_Unixtime      (    4 bytes - I  )
	|||||||||+----------------- GSAT              (    1 byte  - B  )
	||||||||||+---------------- LAT               (    4 bytes - f  )
	|||||||||||+--------------- LON               (    4 bytes - f  )
	||||||||||||+-------------- SPD               (    2 bytes - H  )
	|||||||||||||+++----------- Gasoline LRF      (3 x 2 bytes - HHH)
	||||||||||||||||+---------- MBAT              (    2 bytes - H  )
	|||||||||||||||||+--------- BBAT              (    2 bytes - H  )
	||||||||||||||||||+++------ In gasoline LRF   (3 x 2 bytes - HHH)
	|||||||||||||||||||||+----- In gasoline TOT   (    2 bytes - H  )
	||||||||||||||||||||||+---- Inputs Bitpacked  (    1 byte  - B  )
	|||||||||||||||||||||||+--- Outputs Bitpacked (    1 byte  - B  )
	||||||||||||||||||||||||+-- HSZZ              (    2 bytes - H  )
	|||||||||||||||||||||||||+- DIST              (    1 byte  - B  )
	||||||||||||||||||||||||||
	<BBHHHHBIBffHHHHHHHHHHBBHB

'''

## Pacchetto con messaggio chat

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ VER               (    1 byte  - B  )
	|||+++--------------------- IMEI              (3 x 2 bytes - HHH)
	||||||+-------------------- DRVN              (    2 bytes - H  )
	|||||||+------------------- EVTN              (    1 byte  - B  )
	||||||||+------------------ UTC_Unixtime      (    4 bytes - I  )
	|||||||||+----------------- GSAT              (    1 byte  - B  )
	||||||||||+---------------- LAT               (    4 bytes - f  )
	|||||||||||+--------------- LON               (    4 bytes - f  )
	||||||||||||+-------------- SPD               (    2 bytes - H  )
	|||||||||||||+++----------- Gasoline LRF      (3 x 2 bytes - HHH)
	||||||||||||||||+---------- MBAT              (    2 bytes - H  )
	|||||||||||||||||+--------- BBAT              (    2 bytes - H  )
	||||||||||||||||||+++------ In gasoline LRF   (3 x 2 bytes - HHH)
	|||||||||||||||||||||+----- In gasoline TOT   (    2 bytes - H  )
	||||||||||||||||||||||+---- Inputs Bitpacked  (    1 byte  - B  )
	|||||||||||||||||||||||+--- Outputs Bitpacked (    1 byte  - B  )
	||||||||||||||||||||||||+-- HSZZ              (    2 bytes - H  )
	|||||||||||||||||||||||||+- CHAT              (    n byte  - s  )
	||||||||||||||||||||||||||
	<BBHHHHBIBffHHHHHHHHHHBBHs

'''

## Pacchetto di risposta normale

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
    |||
	<BB

'''

## Pacchetto di risposta con errori

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
	|||+----------------------- OEFL              (    1 byte  - B  )
    ||||
	<BBB

'''

## Pacchetto di risposta con parametri di conversione

Valido se ONDT è compreso tra 1 e 6.

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
	|||+----------------------- ONDT              (    1 byte  - B  )
    ||||+---------------------- OPLD              (    4 byte  - f  )
    |||||
	<BBBf

'''

## Pacchetto di risposta con nome dell'autista

Valido se ONDT è pari a 7.

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
	|||+----------------------- ONDT              (    1 byte  - B  )
    ||||+---------------------- num               (    2 byte  - H  )
    |||||+--------------------- name              (    ? bytes - s  )
	||||||
	<BBBHs

'''

## Pacchetto di risposta con un codice o il carburante in sede

Valido se ONDT è compreso tra 8 e 12.

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
	|||+----------------------- ONDT              (    1 byte  - B  )
    ||||+---------------------- CODE or CARB      (    4 byte  - L  )
	|||||
	<BBBL

'''

## Pacchetto di risposta con un messaggio

Valido se ONDT è pari a 13.

'''

    +-------------------------- Little endian
    |+------------------------- LEN               (    1 byte  - B  )
 	||+------------------------ RSP               (    1 byte  - B  )
	|||+----------------------- ONDT              (    1 byte  - B  )
    ||||+---------------------- MSG               (    ? byte  - s  )
	|||||
	<BBBs

'''

# Precisione in gradi rispetto ai punti decimali

Per determinare la precisione in gradi o metri a partire dalla precisione dell'angolo di Latitudine o Longitudine,
basta seguire la seguente tabella:

    decimal | decimal    |    DMS           | Qualitative scale that  |  N/S-E/W   |   E/W at  |  E/W at  |  E/W at
    places  | degrees    |                  |   can be identified     | at equator |   23N/S   |  45N/S   |  67N/S
   ---------+------------+------------------+-------------------------+------------+-----------+----------+----------
      0     | 1.0        | 1° 00' 0"        | country or large region | 111.32 km  | 102.47 km | 78.71 km | 43.496 km
      1     | 0.1        | 0° 06' 0"        | large city or district  | 11.132 km  | 10.247 km | 7.871 km | 4.3496 km
      2     | 0.01       | 0° 00' 36"       | town or village         | 1.1132 km  | 1.0247 km | 787.1 m  | 434.96 m
      3     | 0.001      | 0° 00' 3.6"      | neighborhood, street    | 111.32 m   | 102.47 m  | 78.71 m  | 43.496 m
      4     | 0.0001     | 0° 00' 0.36"     | individual street       | 11.132 m   | 10.247 m  | 7.871 m  | 4.3496 m
      5     | 0.00001    | 0° 00' 0.036"    | individual trees        | 1.1132 m   | 1.0247 m  | 787.1 mm | 434.96 mm
      6     | 0.000001   | 0° 00' 0.0036"   | individual humans       | 111.32 mm  | 102.47 mm | 78.71 mm | 43.496 mm
      7     | 0.0000001  | 0° 00' 0.00036"  | commercial surveying    | 11.132 mm  | 10.247 mm | 7.871 mm | 4.3496 mm
      8     | 0.00000001 | 0° 00' 0.000036" | specialized surveying   | 1.1132 mm  | 1.0247 mm | 787.1 µm | 434.96 µm

La precisione dei tipi di dati float e double, partendo dalla loro definizione IEEE 754, è la seguente:

  * Single precision (float) gives you 23 bits of significand, 8 bits of exponent, and 1 sign bit (0.0000001 = 10mm)
  * Double precision (double) gives you 52 bits of significand, 11 bits of exponent, and 1 sign bit (0.000000000000001 = um)

Il seguente schema indica la precisione e la codifica di alcuni formati comunemente usati:

             Type          | Sign | Exponent | Significand | Total | Exponent | Bits      | Number of
                           |      |          |    field    | bits  |   bias   | precision | decimal digits
    -----------------------+------+----------+-------------+-------+----------+-----------+-----------------
    Half (IEEE 754-2008)   | 1    |    5     |     10      |  16   |    15    |    11     | ~3.3
    Single	               | 1    |    8     |     23      |  32   |   127    |    24     | ~7.2
    Double	               | 1    |   11     |     52      |  64   |  1023    |    53     | ~15.9
    x86 extended precision | 1    |   15     |     64      |  80   | 16383    |    64     | ~19.2
    Quad                   | 1    |   15     |    112      | 128   | 16383    |   113     | ~34.0

# Referenze

  * UNIX Network Programming 1st Edition, by W. Richard Stevens
  * Programming Pearls (2nd Edition) 2nd Edition, by Jon Bentley
