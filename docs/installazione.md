# 1. Descrizione generale

# 1.1 Dispositivi supportati

Alcuni dispositivi di archiviazione USB, nonostante funzionino perfettamente, non vengono rilevati correttamente all'avvio e quindi non possono essere utilizzati per la prima installazione dei dispositivi:

  - Kingston DataTraveler 2.0 Micro 8GB (0951:1665)
  - Verbatim Store N Go 4GB Avio (18A5:0302)
  - TDK LoR TF10 8GB (0718:0619)
  
Altri invece risultano pienamente compatibili, e viene qui di seguito riportato l'elenco di quanti finora utilizzati con successo:

  - Sandisk U3 Cruzer Micro 8GB (0781:5406)
  - Maxell 4GB (0B27:0167)
  - Verbatim Store N Go 8GB Dark (18A5:0302)
  - Kingston DT 101 G2 8GB (0951:1642)
  - Trascend Jatflash 4GB (8564:1000)
  
# 1.2 Organizzazione dei files

Per effettuare l'aggiornamento delle unità di controllo è necessario copiare all'interno del dispositivo di archiviazione USB i seguenti files:

  - _abt21-ubifs.img_: immagine di boot di installazione
  - *SIM.csv*: Archivio in formato csv contenente ICCID, PIN e PUK
  - ABT21-BSP-01-update-03-data.tgz
Angstrom-2011.03.iso
SIM.csv
System Volume Information
Utility
abt21-uImage
abt21-uImageUPGRD
abt21-ubifs.img
abt21-upgrade.sh
abt21-upgrade.sh~
abt21_ivt_uboot.sb
ignite
pkg_update.sh

# A Boot successiful

```Text
abt21-imx-bootlets-1.0.2
ABT21 HW Version: 00000000
Oct 31 201410:43:30
Memory type is mDDR
Wait for DDR ready...
Start change cpu freq...
Start test memory access...
Finish simple test...
PowerPrep start initialize power...


U-Boot 2009.08-00003-g4036536 (ott 17 2013 - 08:51:53)

Freescale i.MX28 family
CPU:   454 MHz
BUS:   151 MHz
EMI:   196 MHz
GPMI:   24 MHz
DRAM:  128 MB
NAND:  Manufacturer      : Micron (0x2c)
Device Code       : 0xf1
Cell Technology   : SLC
Chip Size         : 128 MiB
Pages per Block   : 64
Page Geometry     : 2048+64
ECC Strength      : 4 bits
ECC Size          : 512 B
Data Setup Time   : 30 ns
Data Hold Time    : 20 ns
Address Setup Time: 10 ns
GPMI Sample Delay : 6 ns
tREA              : Unknown
tRLOH             : Unknown
tRHOH             : Unknown
Description       : <None>
128 MiB
*** Warning - bad CRC or NAND, using default environment

In:    serial
Out:   serial
Err:   serial
Net:   got MAC address from IIM: 00:04:00:00:00:00
FEC0
Type "abt" to stop autoboot:  0
(Re)start USB...
USB:   ABT21 e401fa05(00000000) init hccr 80090100 and hcor 80090140 hc_length 64 phy1 status 00000100(00000000) ver 04020000(00000000), clock 80060000(00020000), clock via clock 2020c000(00000000), digctl 00000004, mode 00000000
Register 10011 NbrPorts 1
USB EHCI 1.00
scanning bus for devices... 2 USB Device(s) found
       scanning bus for storage devices... 1 Storage Device(s) found
reading abt21-uImageUPGRD
......
................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................

5907740 bytes read
stopping USB..
## Booting kernel from Legacy Image at 42000000 ...
   Image Name:   Linux-2.6.35.14-bsp-abt21-1.0
   Image Type:   ARM Linux Kernel Image (uncompressed)
   Data Size:    5907676 Bytes =  5.6 MB
   Load Address: 40008000
   Entry Point:  40008000
   Verifying Checksum ... OK
   Loading Kernel Image ... OK
OK

Starting kernel ...

Linux version 2.6.35.14-bsp-abt21-1.0 (abt03@Cl-abt03) (gcc version 4.3.3 (Sourcery G++ Lite 2009q1-203) ) #10 PREEMPT Thu May 16 12:26:41 CEST 2013
CPU: ARM926EJ-S [41069265] revision 5 (ARMv5TEJ), cr=00053177
CPU: VIVT data cache, VIVT instruction cache
Machine: ABtrack MX28ABT board
Memory policy: ECC disabled, Data cache writeback
Built 1 zonelists in Zone order, mobility grouping on.  Total pages: 16256
Kernel command line: mtdparts=gpmi-nfc-main:2M(bootloader),128K(env),3M(kernel),-(rootfs) console=ttySP0,115200n8 rdinit=/sbin/init mem=64M gpmi=1
PID hash table entries: 256 (order: -2, 1024 bytes)
Dentry cache hash table entries: 8192 (order: 3, 32768 bytes)
Inode-cache hash table entries: 4096 (order: 2, 16384 bytes)
Memory: 64MB = 64MB total
Memory: 51652k/51652k available, 13884k reserved, 0K highmem
Virtual kernel memory layout:
    vector  : 0xffff0000 - 0xffff1000   (   4 kB)
    fixmap  : 0xfff00000 - 0xfffe0000   ( 896 kB)
    DMA     : 0xfde00000 - 0xffe00000   (  32 MB)
    vmalloc : 0xc4800000 - 0xf0000000   ( 696 MB)
    lowmem  : 0xc0000000 - 0xc4000000   (  64 MB)
    modules : 0xbf000000 - 0xc0000000   (  16 MB)
      .init : 0xc0008000 - 0xc0871000   (8612 kB)
      .text : 0xc0871000 - 0xc0c8b000   (4200 kB)
      .data : 0xc0c8c000 - 0xc0cbc780   ( 194 kB)
SLUB: Genslabs=11, HWalign=32, Order=0-3, MinObjects=0, CPUs=1, Nodes=1
Hierarchical RCU implementation.
        RCU-based detection of stalled CPUs is disabled.
        Verbose stalled-CPUs detection is disabled.
NR_IRQS:288
Console: colour dummy device 80x30
console [ttySP0] enabled
Calibrating delay loop... 226.09 BogoMIPS (lpj=1130496)
pid_max: default: 32768 minimum: 301
Security Framework initialized
Mount-cache hash table entries: 512
CPU: Testing write buffer coherency: ok
regulator: core version 0.5
NET: Registered protocol family 16
regulator: vddd: 800 <--> 1575 mV at 1500 mV fast normal
regulator: vdddbo: 800 <--> 1575 mV fast normal
regulator: vdda: 1500 <--> 2275 mV at 1800 mV fast normal
vddio = 3380000, val=10
regulator: vddio: 2880 <--> 3680 mV at 3380 mV fast normal
regulator: overall_current: fast normal
regulator: vbus5v:
regulator: mxs-duart-1: fast normal
regulator: mxs-bl-1: fast normal
regulator: mxs-i2c-1: fast normal
regulator: mmc_ssp-1: fast normal
regulator: mmc_ssp-2: fast normal
regulator: charger-1: fast normal
regulator: power-test-1: fast normal
regulator: cpufreq-1: fast normal
i.MX IRAM pool: 124 KB@0xc4820000
Initializing GPMI pins
usb DR wakeup device is registered
IMX usb wakeup probe
bio: create slab <bio-0> at 0
SCSI subsystem initialized
usbcore: registered new interface driver usbfs
usbcore: registered new interface driver hub
usbcore: registered new device driver usb
Switching to clocksource mxs clock source
NET: Registered protocol family 2
IP route cache hash table entries: 1024 (order: 0, 4096 bytes)
TCP established hash table entries: 2048 (order: 2, 16384 bytes)
TCP bind hash table entries: 2048 (order: 1, 8192 bytes)
TCP: Hash tables configured (established 2048 bind 2048)
TCP reno registered
UDP hash table entries: 256 (order: 0, 4096 bytes)
UDP-Lite hash table entries: 256 (order: 0, 4096 bytes)
NET: Registered protocol family 1
RPC: Registered udp transport module.
RPC: Registered tcp transport module.
RPC: Registered tcp NFSv4.1 backchannel transport module.
Bus freq driver module loaded
IMX usb wakeup probe
usb h1 wakeup device is registered
mxs_cpu_init: cpufreq init finished
VFS: Disk quotas dquot_6.5.2
Dquot-cache hash table entries: 1024 (order 0, 4096 bytes)
JFFS2 version 2.2. (NAND) © 2001-2006 Red Hat, Inc.
msgmni has been set to 100
alg: No test for stdrng (krng)
cryptodev: driver loaded.
Block layer SCSI generic (bsg) driver version 0.4 loaded (major 253)
io scheduler noop registered
io scheduler deadline registered
io scheduler cfq registered (default)
mxs-auart.0: ttySP0 at MMIO 0x8006a000 (irq = 112) is a mxs-auart.0
Found APPUART 3.1.0
mxs-auart.3: ttySP3 at MMIO 0x80070000 (irq = 115) is a mxs-auart.3
Found APPUART 3.1.0
mxs-auart.4: ttySP4 at MMIO 0x80072000 (irq = 116) is a mxs-auart.4
Found APPUART 3.1.0
brd: module loaded
loop: module loaded
i.MX GPMI NFC
NFC: Version 1, 8-chip GPMI and BCH
Boot ROM: Version 1, Single-chip boot area, block mark swapping supported
Scanning for NAND Flash chips...
NAND device: Manufacturer ID: 0x2c, Chip ID: 0xf1 (Micron NAND 128MiB 3,3V 8-bit)
-----------------------------
NAND Flash Device Information
-----------------------------
Manufacturer      : Micron (0x2c)
Device Code       : 0xf1
Cell Technology   : SLC
Chip Size         : 128 MiB
Pages per Block   : 64
Page Geometry     : 2048+64
ECC Strength      : 4 bits
ECC Size          : 512 B
Data Setup Time   : 30 ns
Data Hold Time    : 20 ns
Address Setup Time: 10 ns
GPMI Sample Delay : 6 ns
tREA              : Unknown
tRLOH             : Unknown
tRHOH             : Unknown
Description       : <None>
-----------------
Physical Geometry
-----------------
Chip Count             : 1
Page Data Size in Bytes: 2048 (0x800)
Page OOB Size in Bytes : 64
Block Size in Bytes    : 131072 (0x20000)
Block Size in Pages    : 64 (0x40)
Chip Size in Bytes     : 134217728 (0x8000000)
Chip Size in Pages     : 65536 (0x10000)
Chip Size in Blocks    : 1024 (0x400)
Medium Size in Bytes   : 134217728 (0x8000000)
------------
NFC Geometry
------------
ECC Algorithm          : BCH
ECC Strength           : 8
Page Size in Bytes     : 2112
Metadata Size in Bytes : 10
ECC Chunk Size in Bytes: 512
ECC Chunk Count        : 4
Payload Size in Bytes  : 2048
Auxiliary Size in Bytes: 16
Auxiliary Status Offset: 12
Block Mark Byte Offset : 1999
Block Mark Bit Offset  : 0
-----------------
Boot ROM Geometry
-----------------
Boot Area Count            : 0
Boot Area Size in Bytes    : 0 (0x0)
Stride Size in Pages       : 64
Search Area Stride Exponent: 2
Scanning device for bad blocks
4 cmdlinepart partitions found on MTD device gpmi-nfc-main
Creating 4 MTD partitions on "gpmi-nfc-main":
0x000000000000-0x000000200000 : "bootloader"
0x000000200000-0x000000220000 : "env"
0x000000220000-0x000000520000 : "kernel"
0x000000520000-0x000008000000 : "rootfs"
mxs-spi mxs-spi.0: Max possible speed 24000 = 24000000/2 kHz
mxs-spi mxs-spi.0: at 0x80014000 mapped to 0xF0014000, irq=84, bus 1, DMA ver_major 4
rtl8150: v0.6.2 (2004/08/27):rtl8150 based usb-ethernet driver
usbcore: registered new interface driver rtl8150
usbcore: registered new interface driver asix
usbcore: registered new interface driver cdc_ether
usbcore: registered new interface driver net1080
usbcore: registered new interface driver cdc_subset
usbcore: registered new interface driver zaurus
ehci_hcd: USB 2.0 'Enhanced' Host Controller (EHCI) Driver
fsl-ehci fsl-ehci: Freescale On-Chip EHCI Host Controller
fsl-ehci fsl-ehci: new USB bus registered, assigned bus number 1
fsl-ehci fsl-ehci: irq 93, io base 0x80080000
fsl-ehci fsl-ehci: USB 2.0 started, EHCI 1.00
hub 1-0:1.0: USB hub found
hub 1-0:1.0: 1 port detected
fsl-ehci fsl-ehci.0: Freescale On-Chip EHCI Host Controller
fsl-ehci fsl-ehci.0: new USB bus registered, assigned bus number 2
fsl-ehci fsl-ehci.0: irq 92, io base 0x80090000
fsl-ehci fsl-ehci.0: USB 2.0 started, EHCI 1.00
hub 2-0:1.0: USB hub found
hub 2-0:1.0: 1 port detected
Initializing USB Mass Storage driver...
usbcore: registered new interface driver usb-storage
USB Mass Storage support registered.
mice: PS/2 mouse device common for all mice
MXS RTC driver v1.0 hardware v2.3.0
mxs-rtc mxs-rtc.0: rtc core: registered mxs-rtc as rtc0
i2c /dev entries driver
cpuidle: using governor ladder
cpuidle: using governor menu
dcp dcp.0: DCP crypto enabled.!
usbcore: registered new interface driver hiddev
usbcore: registered new interface driver usbhid
usbhid: USB HID core driver
TCP cubic registered
NET: Registered protocol family 17
can: controller area network core (rev 20090105 abi 8)
NET: Registered protocol family 29
can: raw protocol (rev 20090105)
mxs-rtc mxs-rtc.0: setting system clock to 2010-05-05 16:25:03 UTC (1273076703)
Freeing init memory: 8612K
INIT: version 2.86 booting
Please wait: booting...
usb 2-1: new high speed USB device using fsl-ehci and address 2
Root filesystem already rw, not remounting
scsi0 : usb-storage 2-1:1.0
Mon Mar  7 11:14:00 UTC 2011
INIT: Entering runlevel: 5
scsi 0:0:0:0: Direct-Access     Kingston DT 101 G2        1.00 PQ: 0 ANSI: 4
sd 0:0:0:0: [sda] 15131636 512-byte logical blocks: (7.74 GB/7.21 GiB)
sd 0:0:0:0: [sda] Write Protect is off
sd 0:0:0:0: [sda] Assuming drive cache: write through
sd 0:0:0:0: [sda] Assuming drive cache: write through
 sda: sda1
sd 0:0:0:0: [sda] Assuming drive cache: write through
ABT21 IO Driver v.gpio-abt21-1.0, (Compiled on May  7 2013 14:50:48)
sd 0:0:0:0: [sda] Attached SCSI removable disk

THE SYSTEM UPGRADING WILL START SOON...

Pindog Watchdog Timer, (c) 2008 EVOL Srl, time period: 60 - 180 sec
pindog pindog.0: watchdog service ready
           gprs_init(): Apertura della porta
             gprs_on(): Avvio del modem
             gprs_on():  Inizializzazione dei segnali
             gprs_on():  Abilitazione del segnale ON
             gprs_on():  Abilitazione del segnale IGNITION
   gprs_check_config(): Caricamento dati dal modem
 gprs_catch_response():  STARTED!
 gprs_catch_response():   GPRS IPR = '115200'
 gprs_catch_response():  GPRS RSSI = '14'
 gprs_catch_response():     SIM ID = '8939883263100041505'
 gprs_catch_response():        DBM = ''
 gprs_catch_response():       IMEI = '351535057285439'
      gprs_check_pin(): Checking PIN
      gprs_check_pin():  Pin 1554 OK
install_fuelcheck_fw(): Avvio installazione
       install_bsp01(): Installazione BSP 01
          mount_root(): Monto la root partition
UBI: attaching mtd3 to ubi0
UBI: physical eraseblock size:   131072 bytes (128 KiB)
UBI: logical eraseblock size:    126976 bytes
UBI: smallest flash I/O unit:    2048
UBI: VID header offset:          2048 (aligned 2048)
UBI: data offset:                4096
UBI: attached mtd3 to ubi0
UBI: MTD device name:            "rootfs"
UBI: MTD device size:            122 MiB
UBI: number of good PEBs:        983
UBI: number of bad PEBs:         0
UBI: max. allowed volumes:       128
UBI: wear-leveling threshold:    4096
UBI: number of internal volumes: 1
UBI: number of user volumes:     1
UBI: available PEBs:             0
UBI: total number of reserved PEBs: 983
UBI: number of PEBs reserved for bad PEB handling: 9
UBI: max/mean erase counter: 1/0
UBI: image sequence number: 1778981308
UBI: background thread "ubi_bgt0d" started, PID 1245
 ubiblka: unknown partition table
          mount_root():  ubiattach ok
UBIFS: mounted UBI device 0, volume 0, name "rootfs"
UBIFS: file system size:   121769984 bytes (118916 KiB, 116 MiB, 959 LEBs)
UBIFS: journal size:       9023488 bytes (8812 KiB, 8 MiB, 72 LEBs)
UBIFS: media format:       w4/r0 (latest is w4/r0)
UBIFS: default compressor: zlib
UBIFS: reserved for root:  0 bytes (0 KiB)
          mount_root():  mount ok
         backup_data(): Controllo i files presenti
         backup_data():  PROD: ABT21-B-00-200049***432013***testsw:v1.0.1***testbrd:v1.0
         backup_data():  ERR: no-files
          mount_root(): Smonto la root partition
UBIFS: un-mount UBI device 0, volume 0
         umount_root():  umount ok
UBI: mtd3 is detached from ubi0
         umount_root():  ubidetach ok
       install_bsp01():  Installo la root partition mtd3
       install_bsp01():  flash_eraseall ok
       install_bsp01():  ubiformat ok
          mount_root(): Monto la root partition
UBI: attaching mtd3 to ubi0
UBI: physical eraseblock size:   131072 bytes (128 KiB)
UBI: logical eraseblock size:    126976 bytes
UBI: smallest flash I/O unit:    2048
UBI: VID header offset:          2048 (aligned 2048)
UBI: data offset:                4096
UBI: volume 0 ("rootfs") re-sized from 967 to 970 LEBs
UBI: attached mtd3 to ubi0
UBI: MTD device name:            "rootfs"
UBI: MTD device size:            122 MiB
UBI: number of good PEBs:        983
UBI: number of bad PEBs:         0
UBI: max. allowed volumes:       128
UBI: wear-leveling threshold:    4096
UBI: number of internal volumes: 1
UBI: number of user volumes:     1
UBI: available PEBs:             0
UBI: total number of reserved PEBs: 983
UBI: number of PEBs reserved for bad PEB handling: 9
UBI: max/mean erase counter: 0/0
UBI: image sequence number: 1152295975
UBI: background thread "ubi_bgt0d" started, PID 1281
 ubiblka: unknown partition table
          mount_root():  ubiattach ok
UBIFS: mounted UBI device 0, volume 0, name "rootfs"
UBIFS: file system size:   121769984 bytes (118916 KiB, 116 MiB, 959 LEBs)
UBIFS: journal size:       9023488 bytes (8812 KiB, 8 MiB, 72 LEBs)
UBIFS: media format:       w4/r0 (latest is w4/r0)
UBIFS: default compressor: zlib
UBIFS: reserved for root:  0 bytes (0 KiB)
          mount_root():  mount ok
        restore_data(): Ricopio i files
        restore_data():  PROD: ABT21-B-00-200049***432013***testsw:v1.0.1***testbrd:v1.0
        restore_data():  ERR: no-files
        restore_data():  PIN: 1554;8939883263100041505
        restore_data():  IMEI: 351535057285439
       install_bsp01():  flash_eraseall_mtd1 ok
       install_bsp01():  flash_eraseall_mtd0 ok
       install_bsp01():  kobs-ng ok
       install_bsp03(): Aggiornamento alla 03
       install_bsp03():  Decomprimo l'aggiornamento ok
       install_bsp03():  flash_eraseall_mtd2 ok
       install_bsp03():  nandwrite_mtd2 ok
       install_bsp03():  flash_eraseall_mtd0 ok
       install_bsp03():  kobs-ng ok
install_fuelcheck_fw(): Aggiorno il software
         change_repo(): Cambio base
         change_repo():  Base repo changed
         change_repo():  Locale repo changed
         change_repo():  Noarch repo changed
         change_repo():  Perl repo changed
         change_repo():  Python repo changed
         opkg_update(): Aggiorno l'elenco dei programmi
wget: cannot connect to remote host (10.0.0.2): Network is unreachable
         change_repo():  Updating fail probably due GStreamer...
        opkg_install(): Installo dei programmi (ncurses-terminfo-base libtinfo5 libncurses5)
         change_repo():  Installing joe_prereq ok
              prereq(): Installing joe ok
        opkg_install(): Installo dei programmi (curl git less mysql5-client ncurses ncurses-terminfo ntpdate procps pstree rsync screen)
         change_repo():  Installing 1.13_prereq ok
        opkg_install(): Installo dei programmi (bash bc ca-certificates diffutils inotify-tools ldd nmap openssh-keygen postgresql-client ppp-tools sqlite3 usbutils)
         change_repo():  Installing 1.14_prereq ok
        opkg_install(): Installo dei programmi (gnupg openssl)
         change_repo():  Installing 1.15_prereq ok
        opkg_install(): Installo dei programmi (python python-bzip2 python-codecs python-compile python-compiler python-configobj python-core python-crypt python-curses python-datetime)
         change_repo():  Installing 1.16_prereq_a ok
        opkg_install(): Installo dei programmi (python-logging python-math python-mime python-misc python-netclient python-pickle python-distutils python-doctest python-fcntl python-io)
         change_repo():  Installing 1.16_prereq_b ok
        opkg_install(): Installo dei programmi (python-lang python-pprint python-pydoc python-pygps python-pyrtc python-pyserial python-re python-readline python-shell python-sqlite3 python-stringold)
         change_repo():  Installing 1.16_prereq_c ok
        opkg_install(): Installo dei programmi (python-subprocess python-textutils python-threading python-twisted python-zlib python-twisted-bin python-twisted-conch python-twisted-core)
         change_repo():  Installing 1.16_prereq_d ok
        opkg_install(): Installo dei programmi (python-twisted-flow python-twisted-lore python-twisted-protocols python-twisted-runner python-twisted-web python-twisted-words python-unittest)
         change_repo():  Installing 1.16_prereq_e ok
        opkg_install(): Installo dei programmi (python-twisted-mail python-twisted-names python-twisted-news python-twisted-pair python-twisted-zsh python-zopeinterface)
         change_repo():  Installing 1.16_prereq_f ok
         change_repo(): Cambio base
         change_repo():  Base repo changed
         change_repo():  Locale repo changed
         change_repo():  Noarch repo changed
         change_repo():  Perl repo changed
         change_repo():  Python repo changed
          change_pwd(): Changing pwd
          change_pwd():  Changing pwd ok
      Adding init ok():
cp: cannot stat '/mnt/ignite': No such file or directory
  Saving ignite fail():
          mount_root(): Smonto la root partition
UBIFS: un-mount UBI device 0, volume 0
         umount_root():  umount ok
UBI: mtd3 is detached from ubi0
         umount_root():  ubidetach ok
            gprs_off(): Arresto del modem
            gprs_off():  Spegnimento del modem
 gprs_catch_response():  Attendo il termine dello shutdown
 gprs_cathc_response():  Disabilitazione del segnale ON
         gprs_deinit(): Chiusura della porta
 utl_wait_and_reboot(): Attendo il disinserimento della pennetta e riavvio
 utl_wait_and_reboot():  Attendo il disinserimento della pennetta
usb 2-1: USB disconnect, address 2
 utl_wait_and_reboot():  Pennetta disinserita
 utl_wait_and_reboot():  Riavvio
INIT: Switching to runlevel: 6
INIT: Sending processes the TERM signal
Sending all processes the TERM signal...
ehci_fsl_bus_suspend, Host 1
Sending all processes the KILL signal...
Unmounting remote filesystems...
Deactivating swap...
Unmounting local filesystems...
Rebooting... Restarting system.
```