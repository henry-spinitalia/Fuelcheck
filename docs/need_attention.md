# Alimentazione insufficiente

In presenza di un'alimentazione insufficiente e di una batteria interna scarica, il sistema continua ad inviare in rapida successione i seguenti messaggi:

```Text
5▒▒▒ɊjJ▒▒▒▒ѱ▒▒͵▒r▒r▒R▒J▒▒S&$R$U▒▒▒Z▒K▒▒▒▒▒▒▒▒R▒▒j▒Ҧ&H&LLL▒▒43:30
Memory type is mDDR
Wait for DDR ready...
Start change cpu freq...
Start test memory access...
Finish simple test...
PowerPrep start initialize power...

Boot from battery, 5V input not detected.
5▒▒▒ɊjJ▒▒▒▒ѱ▒▒͵▒r▒r▒R▒J▒▒S&$R$U▒▒▒Z▒K▒▒▒▒▒▒▒▒R▒▒j▒Ҧ&&LL▒L▒▒43:30
Memory type is mDDR
Wait for DDR ready...
Start change cpu freq...
Start test memory access...
Finish simple test...
PowerPrep start initialize power...
```

# Non c'e' sincronizzazione dell'HW clock????

Sembra che il comando hwclock -w su rtc ed rtc1 non venga mai dato.

Questo produce strani fenomeni come l'invio di eventi 16 del 2010