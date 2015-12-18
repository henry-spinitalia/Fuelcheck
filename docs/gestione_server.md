# Descrizione 

Dal momento che ci si connette ad un server remoto con ssh, e viene creata una console virtuale che scompare non appena la connessione termina, bisogna eseguire il server all'interno di _**screen**_. In questo modo sarà possibile scollegarsi lasciando il programma in esecuzione per poi riconnettersi in seguito.

## Controllare se siamo dentro screen

```Text
    
    mik@pritijen ~/temp_fuelcheck/Fuelcheck $ echo $STY
      
```

## Controllare il numero di screen attivi

```Text
    
    mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -ls
    
    There are screens on:
        30319.pts-1.pritijen    (12/18/15 09:46:20)     (Detached)
        30309.pts-1.pritijen    (12/18/15 09:46:17)     (Detached)
    2 Sockets in /var/run/screen/S-henry.
    
```

## Connettersi ad uno screen esistente

Se è presente un solo screen, basta:

```Text

    mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -r
    
```

Se sono presenti più screen attivi, bisogna dargli l'ID come parametro:

```Text

    mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -r

    There are several suitable screens on:
            30319.pts-1.pritijen    (12/18/15 09:46:21)     (Detached)
            30309.pts-1.pritijen    (12/18/15 09:46:18)     (Detached)
    Type "screen [-d] -r [pid.]tty.host" to resume one of them.

    mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -r 30319

```

## Avvio del server

Per avviare il server, bisogna eseguire il comando:

```Text
  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ cd temp_fuelcheck/Fuelcheck
  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -d -m -S FC_SERVER python fc_receiver.py
```

## Arresto del server

Se vogliamo interrompere l'esecuzione del server per passare al debugging, bisogna eseguire il comando:

```Text

  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ screen -r

  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ <CTRL-C>

```

oppure possiamo identificare il pid e mandargli un SIGKILL senza entrare in screen

```Text

  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ ps -ef | grep SCREEN
    mik      29323     1  0 Dec17 ?        00:00:00 SCREEN
    henry    30309     1  0 09:46 ?        00:00:00 SCREEN
    henry    30319     1  0 09:46 ?        00:00:00 SCREEN
    henry    30344 30320  0 09:54 pts/3    00:00:00 grep --color=auto SCREEN

  mik@pritijen ~/temp_fuelcheck/Fuelcheck $ kill 30309

```



