#!/usr/bin/env bash

# 1. Manca GStreamer
# 2. Fw download
# 4. Devo disabilitare getty
# 5. Devo salvare l'RTC dopo l'update
# 6. Perchè viene trasmesso un evento 16 con data 08/05/2010

# -----------------------------------------------------------------------------------------------------------
# /mnt  -> Posizione della pennetta USB
# /mnt2 -> RootFS della centralina
# /mnt3 -> Repo in loop da iso
# -----------------------------------------------------------------------------------------------------------

# Constanti -------------------------------------------------------------------------------------------------
C_DEBUG=1
C_CHANGEPW=1
C_KEY=DKLVXANOWPBEQRMSTUCYZFGHIJ

C_GPRS_DEBUG=0
C_GPRS_MAX_RETRY=10
C_GPRS_DEV="/dev/ttySP4"
C_GPRS_SIM_ARCHIVE="/mnt/SIM.csv"

C_OPKG_BASE="/etc/opkg/base-feed.conf"
C_OPKG_GSTREAM="/etc/opkg/gstreamer-feed.conf"
C_OPKG_LOC="/etc/opkg/locale-en-feed.conf"
C_OPKG_NOARCH="/etc/opkg/noarch-feed.conf"
C_OPKG_PERL="/etc/opkg/perl-feed.conf"
C_OPKG_PYTHON="/etc/opkg/python-feed.conf"

# Variabili -------------------------------------------------------------------------------------------------
V_GPRS_AT_CMD=""                    # Comando inviato al modem
V_GPRS_CMD_RESP=0                   # E' stata ricevuta una risposta dal modem
V_GPRS_STATUS=0                     # Stato del modem
V_GPRS_PPPD_STATUS=0                # Stato del demone ppp
V_GPRS_MUX_STATUS=0                 # Stato del demone mux
V_GPRS_POWERUP=0                    # Indica se e' stato ricevuto il ^SYSSTART
V_GPRS_RSSI=99                      # Valore del segnale di campo
V_GPRS_SCID=""                      # SIM ID
V_GPRS_DBM=""                       # DBM del segnale ricevuto
V_GPRS_IMEI=""                      # IMEI della Control Unit
V_GPRS_IMSI=""                      # IMSI della Control Unit
V_GPRS_IPR=""                       # IPR della connessione, per la risposta
V_GPRS_PIN=""                       # PIN della sim

# -----------------------------------------------------------------------------------------------------------
# Modulo di gestione dei packages
# -----------------------------------------------------------------------------------------------------------

# Cambia repo
# - Viene eseguita senza chroot
# - Devono essere montate /mnt2 e la path fornita come parametro
# -----------------------------------------------------------------------------------------------------------
opkg_change_repo()
{

    BASE_PATH=$1

    utl_log_data "opkg_change_repo" "Cambio base"

    if [ -z "$(grep "$BASE_PATH" "$C_OPKG_BASE" 2>/dev/null)" ]; then
        echo "src/gz base $BASE_PATH/armv5te/base" > "/mnt2$C_OPKG_BASE"
        utl_log_data "opkg_change_repo" " Base repo changed"
    else
        utl_log_data "opkg_change_repo" " Base repo already configured"
    fi
    #if [ -z "$(grep /mnt2$BASE_PATH $C_OPKG_GSTREAM 2>/dev/null)" ]; then
    #  echo "src/gz gstreamer $BASE_PATH/armv5te/gstreamer" > $C_OPKG_GSTREAM
    #  utl_log_data "opkg_change_repo" " Gstream repo changed"
    #else
    #  utl_log_data "opkg_change_repo" " Gstream repo already configured"
    #fi
    if [ -z "$(grep "$BASE_PATH" "/mnt2$C_OPKG_LOC" 2>/dev/null)" ]; then
        echo "src/gz locale-en-feed $BASE_PATH/armv5te/locales/en" > "/mnt2$C_OPKG_LOC"
        utl_log_data "opkg_change_repo" " Locale repo changed"
    else
        utl_log_data "opkg_change_repo" " Locale repo already configured"
    fi
    if [ -z "$(grep "$BASE_PATH" "/mnt2$C_OPKG_NOARCH" 2>/dev/null)" ]; then
        echo "src/gz no-arch $BASE_PATH/all" > "/mnt2$C_OPKG_NOARCH"
        utl_log_data "opkg_change_repo" " Noarch repo changed"
    else
        utl_log_data "opkg_change_repo" " Noarch repo already configured"
    fi
    if [ -z "$(grep "$BASE_PATH" "/mnt2$C_OPKG_PERL" 2>/dev/null)" ]; then
        echo "src/gz perl $BASE_PATH/armv5te/perl" > "/mnt2$C_OPKG_PERL"
        utl_log_data "opkg_change_repo" " Perl repo changed"
    else
        utl_log_data "opkg_change_repo" " Perl repo already configured"
    fi
    if [ -z "$(grep "$BASE_PATH" "/mnt2$C_OPKG_PYTHON" 2>/dev/null)" ]; then
        echo "src/gz python $BASE_PATH/armv5te/python" > "/mnt2$C_OPKG_PYTHON"
        utl_log_data "opkg_change_repo" " Python repo changed"
    else
        utl_log_data "opkg_change_repo" " Python repo already configured"
    fi

}

# Aggiorna un repo
# -----------------------------------------------------------------------------------------------------------
opkg_update()
{

    utl_log_data "opkg_update" "Aggiorno l'elenco dei programmi"

    chroot /mnt2 /usr/bin/opkg update 2>&1 >/dev/null
    if [ "$?" = "0" ]; then
        utl_log_data "opkg_update" " Updating ok"
    else
        utl_log_data "opkg_update" " Updating fail probably due GStreamer..."
        # Niente exit causa ISSUE 2
    fi

}

# Installa un programma
# -----------------------------------------------------------------------------------------------------------
opkg_install()
{

    utl_log_data "opkg_install" "Installo dei programmi ($1)"

    chroot /mnt2 /usr/bin/opkg install $1 2>&1 >/dev/null
    if [ "$?" = "0" ]; then
        utl_log_data "opkg_install" " Installing $2 ok"
    else
        utl_log_error "opkg_install" " Installing $2 fail"
    fi

}

# Aggiorna i pacchetti installati
# -----------------------------------------------------------------------------------------------------------
opkg_install_all()
{

    # /mnt/Angstrom deve essere l'iso con Angstrom
    mkdir -p /mnt3
    mount -o loop /mnt/Angstrom-2011.03.iso /mnt3
    mkdir -p /mnt2/mnt3
    mount --bind /mnt3 /mnt2/mnt3

    # Configurazione di opkg in locale
    opkg_change_repo 'file:////mnt3'

    # Update di opkg
    opkg_update

    # Installazione dei programmi 1.13

    # joe
    opkg_install "ncurses-terminfo-base libtinfo5 libncurses5" "joe_prereq"
    if [ ! -e /usr/bin/joe ]; then
        tar xvzf /mnt/Packages/I/joe_3.7-2.3_armel.tgz -C /mnt2/ 2>&1 >/dev/null
        if [ "$?" = "0" ]; then
            utl_log_data "prereq" "Installing joe ok"
        else
            utl_log_data "prereq" "Installing joe fail"
        fi
    fi

    # Add 8192cu module
    #if [ ! -e /lib/firmware/8192cu.ko ]; then
    #  echo "Installing 8192cu module"
    #  tar zxvf /mnt/Packages/I/8192cu-module-2.6.35.14-bsp-abt21-1.1.0.tgz -C /
    #fi

    # Add mcs drivers
    #if [ ! -e /lib/modules/2.6.35.14-bsp-abt21-1.1.0/kernel/drivers/net/usb/mcs7830.ko ]
    #then
    #  echo "Installing mcs7830 driver"
    #  tar xvzf  /mnt/Packages/I/mcs7830-module-2.6.35.14-bsp-abt21-1.1.0.tgz -C /
    #  depmod -a 2.6.35.14-bsp-abt21-1.1.0
    #fi

    # 1.13
    opkg_install "curl git less mysql5-client ncurses ncurses-terminfo ntpdate procps pstree rsync screen" "1.13_prereq"

    # 1.14
    opkg_install "bash bc ca-certificates diffutils inotify-tools ldd nmap openssh-keygen" "1.14_prereq"
    opkg_install "postgresql-client ppp-tools sqlite3 usbutils" "1.14_prereq"

    # 1.15
    opkg_install "gnupg openssl htop" "1.15_prereq"

    # 1.16 - removed python-dev, python-debugger, non tutti insieme altrimenti OOKernel!!!
    opkg_install "python python-bzip2 python-codecs python-compile python-compiler python-configobj" "1.16_prereq_a"
    opkg_install "python-core python-crypt python-curses python-datetime python-logging python-math" "1.16_prereq_b"
    opkg_install "python-mime python-misc python-netclient python-pickle python-distutils python-fcntl" "1.16_prereq_c"
    opkg_install "python-doctest python-io python-lang python-pprint python-pydoc python-re" "1.16_prereq_d"
    opkg_install "python-pygps python-pyrtc python-pyserial python-readline python-shell" "1.16_prereq_e"
    opkg_install "python-sqlite3 python-stringold python-subprocess python-textutils python-zlib" "1.16_prereq_f"
    opkg_install "python-threading python-twisted python-twisted-bin python-twisted-conch" "1.16_prereq_g"
    opkg_install "python-twisted-core python-twisted-flow python-twisted-lore" "1.16_prereq_h"
    opkg_install "python-twisted-protocols python-twisted-runner python-twisted-web" "1.16_prereq_i"
    opkg_install "python-twisted-words python-unittest python-twisted-mail python-twisted-names" "1.16_prereq_j"
    opkg_install "python-twisted-news python-twisted-pair python-twisted-zsh python-zopeinterface" "1.16_prereq_k"

    # Configurazione di opkg in remoto
    opkg_change_repo "http://feeds.angstrom-distribution.org/feeds/2011.03/ipk/glibc"

    # Smonto l'immagine
    umount /mnt2/mnt3
    rmdir  /mnt2/mnt3

}


# -----------------------------------------------------------------------------------------------------------
# Modulo di gestione del modem
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_connect()
# Descrizione: Predispone tutti i files necessari all'installazione
#   Parametri: Nessuno
#     Globali: Nessuno
# -----------------------------------------------------------------------------------------------------------
gprs_connect()
{

    utl_log_data "gprs_connect" "Avvia la connessione"

    chroot /mnt2 pon gprs
    T_OUT=30
    V_IP=$(/mnt2/sbin/ifconfig ppp0 2>/dev/null)
    while [ "$T_OUT" -gt 0 ] && [ "${#V_IP}" -eq 0 ]
    do
        V_IP=$(/mnt2/sbin/ifconfig ppp0 2>/dev/null)
        let T_OUT--
        sleep 1
    done
    if [ "${#V_IP}" -gt 0 ]; then
        utl_log_data "gprs_connect" " Connesso"
    else
        utl_log_error "gprs_connect" " Impossibile connettersi"
    fi
    sleep 10

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_update_clock()
# Descrizione: Predispone tutti i files necessari all'installazione
#   Parametri: Nessuno
#     Globali: Nessuno
# -----------------------------------------------------------------------------------------------------------
gprs_update_clock()
{

    utl_log_data "gprs_update_clock" "Aggiorna il clock di sistema"

    # 15 Dec 11:52:35 ntpdate[1769]: step time server 212.45.144.3 offset 306773.413297 sec
    # con '| cut -d' ' -f1,2,3,10' -> 15 Dec 11:53:48 0.053986
    chroot /mnt2 /usr/bin/ntpdate it.pool.ntp.org | cut -d' ' -f1,2,3,10 > /tmp/ntp_out
    if [ "$?" = "0" ]; then
        utl_log_data "gprs_connect" " Clock aggiornato ($(cat /mnt2/tmp/ntp_out))"
    else
        utl_log_error "gprs_connect" " Impossibile aggiornare il clock di sistema"
    fi

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_init_files()
# Descrizione: Predispone tutti i files necessari all'installazione
#   Parametri: Nessuno
#     Globali: Nessuno
# -----------------------------------------------------------------------------------------------------------
gprs_init_files()
{

    utl_log_data "gprs_init_files" "Initialize gprs files"

    # Controllo la presenza della directory
    mkdir -p /mnt2/home/root/.ssh
    chmod 700 /mnt2/home/root/.ssh

    # Controllo che sia presente .ssh/config
    V_MD5="db2a48ac5c424e8419877defc62bcb82"
    V_FILE="/mnt2/home/root/.ssh/config"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " ssh_config backup made"

        fi

        cat <<- 'EOF' > "$V_FILE"
LogLevel=quiet

Host Deep
  Hostname 14d48b0c29.at-band-camp.net
  HostKeyAlias deep_srv
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  CheckHostIP no
  Port 7100
  User bbox
  ConnectTimeout 10
  KeepAlive yes
  ServerAliveInterval 60

Host Magellano
  Hostname 151.1.80.57
  HostKeyAlias winger_magellano
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null
  CheckHostIP no
  Port 9100
  User root
  ConnectTimeout 10
  ServerAliveInterval 60
  ServerAliveCountMax 3
  TCPKeepAlive no
EOF

        utl_log_data "environment_init" " ssh_config writing"

    else

        utl_log_data "environment_init" " ssh_config already present"

    fi
    chmod 600 "$V_FILE"

    # Controllo che sia presente id_rsa
    V_MD5="0c6c633c786a0364bb1cff09f167656f"
    V_FILE="/mnt2/home/root/.ssh/id_rsa"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " id_rsa backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAmuChTb173ltEFPyNlrdhgowHyC5h3Bz2OI9/KMl2EuTNGiwR
DsThyjuI7rM8NftpE2lGmKi88ACApVD2wz4OQyW7rsQc03/9u2RgZ3G3ObGrgWUQ
k6dhU/dbKohqj82/gQ9rBFbZq7xqgzgmb4jsThp9fuPdkh1AlaWQkAZFo14N74JM
QvqqgZLKN4ZAwLYGVbTheFbG2+5GLX0/49W9658g2+D0QmlAEQHCnC9LbPQAp8qw
R51aTgHdIVoGO1Bssb0fNJh9BiE7+2MouhpI1RPVtDeLOrOJfNpFGiVJgqboQOXr
FFCUjxVOxTO8Qx0AatPVkeYBzSWWPlWTOu5oHwIDAQABAoIBAHYDiKYGJqbugFhF
gVZA8epZ7WwZ+7OP1gaPQWPA71nCQo8Y2P6aAzroVpUculqf8hc6dvLIUP/IQj62
DPIFDTUZQYQQJ675rkvmVpc8TVOHEJqOei0os78Zkrw8KobdTnl3WCJ8U2zLK5ZF
aPRAL1/sS4gu9Zzq8VWWTSuRu+qZBv/hvKBRWIkbdoaL4c14ac1DLpb4VjkiUkX7
Pe0E+MhYJ62kuJls45KqyztLsYkZQrAd7NZFIPD5jEtxWOyAa3DWL+/TCtZ99F0Z
e6PzZJACKF5iOOCt1UJSqpee/NSC5JohWOTRbsdGaLtKrXoYNzd+kIi0/8+y+jDi
mgGUAuECgYEAzgBugI439CiXXUBzfh5+kfj2TCDT1XvwPaTvXkA5wEAbQksk5lQT
Dom8lgfkLUATSeHsM9eC++bQBqMNFrG0lB2R+fA3vs5lFahd2IXYpcerHvALVmrx
bVrO/vWvy4qLT926HV8a29UywkVFJ3qiXdj823vJvDQqZHsg1y/nwocCgYEAwHeu
QrBFIffOkmhyGTX85Q/QNWLLhAWxohY1TGY2JDajvrYSqwhXFzEDIw3VqJU3L7o1
Z1jZmz3/LDYSboyGHu0sm5VWq+YESy1qInrcjYO2Hrc9sOKhPXF44Y0z7HR5gSEF
VyJmSm8dt5qKcGHMuMdPC9kJlBlZ9fWK8e4vW6kCgYASs9tUdJUD58OGRdm2c5JO
Mmo6EyjoUu5Gynio9+/GUounAyeAedWZFkw22tSOfyjBJm/JbSGJOTVdxOPlUZDx
eZXNOU/2VMq8oqKSi+RVeMFCd8yvtdnhccMlRq0FL7jiMWE6VW4c00hedueGZA3l
s1ORobV5DstigANFRiYmdQKBgBKK9UUDioWNRF+ipGt9YhIHhf2+uPDNQ6HkFdp4
dnrisL/s9rt3oDxhwnWcHZuSVLDKdd6xFrX4MR9nTjtMWpecLhIHP0RscrlzdKhB
wgH4UJGBAfaKvxIWXpkMa5Y6WoJwVf1hGQ3OysQnpXLSWVDsEteHX37fOmWR9IL+
eZ2RAoGAcd1KdXAjFmVcvx21tdmimlVPovgW0rTR7FCU1/LLor22L1Ovf6/8feme
Nct6nSakIccjrJ1Vd9LLHywbU7G+ANiFfiguMFq/3l4XfZ7l8yqzPO55x/vAVPKi
enXEmXHoXW3FIN4/CUmStBMlcmh3O6HNdUWQe01ICtFdB73YMfg=
-----END RSA PRIVATE KEY-----
EOF

        utl_log_data "environment_init" " id_rsa writing"

    else

        utl_log_data "environment_init" " id_rsa already present"

    fi
    chmod 600 "$V_FILE"

    # Controlla che sia presente id_rsa.pub
    V_MD5="a3161814d1cd0019c4c2b3ede3f2b354"
    V_FILE="/mnt2/home/root/.ssh/id_rsa.pub"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " key_pub backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCa4KFNvXveW0QU/I2Wt2GCjAfILmHcHPY4j38oyXYS5M0aLBEOxOHKO4juszw1+2kTaUaYqLzwAIClUPbDPg5DJbuuxBzTf/27ZGBncbc5sauBZRCTp2FT91sqiGqPzb+BD2sEVtmrvGqDOCZviOxOGn1+492SHUCVpZCQBkWjXg3vgkxC+qqBkso3hkDAtgZVtOF4Vsbb7kYtfT/j1b3rnyDb4PRCaUARAcKcL0ts9ACnyrBHnVpOAd0hWgY7UGyxvR80mH0GITv7Yyi6GkjVE9W0N4s6s4l82kUaJUmCpuhA5esUUJSPFU7FM7xDHQBq09WR5gHNJZY+VZM67mgf
EOF

        utl_log_data "environment_init" " key_pub writing"

    else

        utl_log_data "environment_init" " key_pub already present"

    fi
    chmod 600 "$V_FILE"

    # Controllo la presenza del rotatore di log ppp
    V_MD5="4983f49bdd850f68b8cf4587364657e9"
    V_FILE="/mnt2/etc/ppp/ip-down.d/09rotatelog"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " rotatelog backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
#!/usr/bin/env sh

# Change the log for the next connection
if [ -e /var/tmp/pppd_log ]; then
  rm -f /var/tmp/pppd_log
  mv -f /var/tmp/pppd_log /var/tmp/pppd_log_old
fi
EOF

        utl_log_data "environment_init" " rotatelog writing"

    else

        utl_log_data "environment_init" " rotatelog already present"

    fi

    # Controllo la configurazione del dns
    V_MD5="1227c792a03dc140d208b49a808d1f27"
    V_FILE="/mnt2/etc/ppp/ip-up.d/08setupdns"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

          cp "$V_FILE" "$V_FILE.old"

          utl_log_data "environment_init" " dns backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
#!/usr/bin/env sh

ACTUALCONF=/var/run/resolv.conf
PPPCONF=/var/run/ppp/resolv.conf
ETCCONF=/var/tmp/resolv.conf

if [ -x /sbin/resolvconf ] ; then
  cat "$PPPCONF" | resolvconf -a "$PPP_IFACE"
elif [ -f "$PPPCONF" ] ; then
  if [ -f "$ACTUALCONF" ] ; then
    if [ ! -h "$ACTUALCONF" -o ! "`readlink "$ACTUALCONF" 2>&1`" = "$PPPCONF" ] ; then
      mv -f "$ACTUALCONF" "$ACTUALCONF.ppporig"
    fi
  fi

  ln -sf "$PPPCONF" "$ACTUALCONF"
  mv -f "$ETCCONF" "$ETCCONF.old"
  ln -sf "$PPPCONF" "$ETCCONF"

fi
EOF

        utl_log_data "environment_init" " dns writing"

    else

        utl_log_data "environment_init" " dns already present"

    fi

    # Controllo la configurazione del demone ppp
    V_MD5="3fefb3a7fa367dbd33c30fa69023eb07"
    V_FILE="/mnt2/etc/ppp/peers/gprs"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " gprs backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
# Fuelcheck gprs pppd configuration file

# Most GPRS phones don't reply to LCP echo's
lcp-echo-failure 3
lcp-echo-interval 30

# Keep pppd attached to the terminal:
# Comment this to get daemon mode pppd
#nodetach

# Debug info from pppd:
# Comment this off, if you don't need more info
debug

# Show password in debug messages
show-password

# Connect script:
# scripts to initialize the GPRS modem and start the connection,
# wvdial command is for Orange SPV while other phones should work with chat
connect /etc/ppp/peers/gprs-connect-chat

# Disconnect script:
# AT commands used to 'hangup' the GPRS connection.
disconnect /etc/ppp/peers/gprs-disconnect-chat

# Serial device to which the GPRS phone is connected:
/dev/ttySP4	# serial port

# Serial port line speed
115200	# fast enough

# Hardware flow control:
#nocrtscts

# Ignore carrier detect signal from the modem:
local

# IP addresses:
# - accept peers idea of our local address and set address peer as 10.0.0.1
# (any address would do, since IPCP gives 0.0.0.0 to it)
# - if you use the 10. network at home or something and pppd rejects it,
# change the address to something else
#:10.0.0.1

# pppd must not propose any IP address to the peer!
noipdefault

# Accept peers idea of our local address
ipcp-accept-local

# Add the ppp interface as default route to the IP routing table
defaultroute

# Newer pppd's also support replacing the default route, if one is
# already present, when the GPRS connetion should be set as the default route
# to the network
replacedefaultroute

# DNS servers from the phone:
# some phones support this, some don't.
usepeerdns

# ppp compression:
# ppp compression may be used between the phone and the pppd, but the
# serial connection is usually not the bottleneck in GPRS, so the
# compression is useless (and with some phones need to disabled before
# the LCP negotiations succeed).
novj
nobsdcomp
novjccomp
nopcomp
noaccomp

# The phone is not required to authenticate:
noauth

# Username and password:
# If username and password are required by the APN, put here the username
# and put the username-password combination to the secrets file:
# /etc/ppp/pap-secrets for PAP and /etc/ppp/chap-secrets for CHAP
# authentication. See pppd man pages for details.
# Example, Radiolinja operator pap-secrets:
# "rlnet"         *       "internet"	*
#user "rlnet"
#user "wind"
user "user"

# The persist tries to reopen the connection if it is dropped. This
# is usefull for example with a Nokia 7650 which only manages to
# 'dial' with every second attempt or when the network likes to drop the
# connection every now and then. It's not fun when the over-night
# 'apt-get dist-upgrade -d -y' fails constantly...
persist
holdoff 5
maxfail 100

# Asyncmap:
# some phones may require this option.
#asyncmap 0xa0000

# No magic:
# some phones may require this option.
#nomagic

# Require PAP authentication:
# some phones may require this option.
#require-pap

# Save all the output to a logfile
logfile /tmp/pppd_log
EOF

        utl_log_data "environment_init" " gprs writing"

    else

        utl_log_data "environment_init" " gprs already present"

    fi

    # Controllo la configurazione del demone ppp
    V_MD5="a58073b7b634533fdf897bfa00b67d7f"
    V_FILE="/mnt2/etc/ppp/peers/muxedgprs"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

      if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

          cp "$V_FILE" "$V_FILE.old"

          utl_log_data "environment_init" " mgprs backup"

      fi

      cat <<- 'EOF' > "$V_FILE"
# Fuelcheck muxedgprs pppd configuration file

# Most GPRS phones don't reply to LCP echo's
lcp-echo-failure 3
lcp-echo-interval 30

# Keep pppd attached to the terminal:
# Comment this to get daemon mode pppd
#nodetach

# Debug info from pppd:
# Comment this off, if you don't need more info
debug

# Show password in debug messages
show-password

# Connect script:
# scripts to initialize the GPRS modem and start the connection,
# wvdial command is for Orange SPV while other phones should work with chat
connect /etc/ppp/peers/muxedgprs-connect-chat

# Disconnect script:
# AT commands used to 'hangup' the GPRS connection.
disconnect /etc/ppp/peers/gprs-disconnect-chat

# Serial device to which the GPRS phone is connected:
/tmp/mux1

# Serial port line speed
115200	# fast enough

# Hardware flow control:
#nocrtscts # IrDA

# Ignore carrier detect signal from the modem:
local

# IP addresses:
# - accept peers idea of our local address and set address peer as 10.0.0.1
# (any address would do, since IPCP gives 0.0.0.0 to it)
# - if you use the 10. network at home or something and pppd rejects it,
# change the address to something else
#:10.0.0.1

# pppd must not propose any IP address to the peer!
noipdefault

# Accept peers idea of our local address
ipcp-accept-local

# Add the ppp interface as default route to the IP routing table
defaultroute

# Newer pppd's also support replacing the default route, if one is
# already present, when the GPRS connetion should be set as the default route
# to the network
replacedefaultroute

# DNS servers from the phone:
# some phones support this, some don't.
usepeerdns

# ppp compression:
# ppp compression may be used between the phone and the pppd, but the
# serial connection is usually not the bottleneck in GPRS, so the
# compression is useless (and with some phones need to disabled before
# the LCP negotiations succeed).
novj
nobsdcomp
novjccomp
nopcomp
noaccomp

# The phone is not required to authenticate:
noauth

# Username and password:
# If username and password are required by the APN, put here the username
# and put the username-password combination to the secrets file:
# /etc/ppp/pap-secrets for PAP and /etc/ppp/chap-secrets for CHAP
# authentication. See pppd man pages for details.
# Example, Radiolinja operator pap-secrets:
# "rlnet"         *       "internet"	*
#user "rlnet"
#user "wind"
user "user"

# The persist tries to reopen the connection if it is dropped. This
# is usefull for example with a Nokia 7650 which only manages to
# 'dial' with every second attempt or when the network likes to drop the
# connection every now and then. It's not fun when the over-night
# 'apt-get dist-upgrade -d -y' fails constantly...
persist
holdoff 5
maxfail 100

# Asyncmap:
# some phones may require this option.
#asyncmap 0xa0000

# No magic:
# some phones may require this option.
#nomagic

# Require PAP authentication:
# some phones may require this option.

#require-pap

# Save all the output to a logfile
logfile /tmp/pppd_log
EOF

        utl_log_data "environment_init" " mgprs writing"

    else

        utl_log_data "environment_init" " mgprs already present"

    fi

    # Rendo volatili i file di uso frequente
    if [ ! -h /etc/resolv.conf ]; then
        utl_log_data "environment_init" " resolv.conf hard link"
        mv /etc/resolv.conf /tmp/resolv.conf
        ln -s /tmp/resolv.conf /etc/resolv.conf
    else
        utl_log_data "environment_init" " resolv.conf already present"
    fi
    if [ ! -h /mnt2/home/root/.ssh/known_hosts ]; then
        utl_log_data "environment_init" " known_hosts hard link"
        if [ -e /mnt2/home/root/.ssh/known_hosts ]; then
            mv /mnt2/home/root/.ssh/known_hosts /mnt2/tmp/known_hosts
        else
            touch /mnt2/tmp/known_hosts
        fi
        chroot /mnt2 ln -s /tmp/known_hosts /home/root/.ssh/known_hosts
    else
        utl_log_data "environment_init" " known_hosts already present"
    fi
}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_check_pin()
# Descrizione: Controllo la configurazione del pin
#   Parametri: Nessuno
#     Globali: V_GPRS_PIN
# -----------------------------------------------------------------------------------------------------------
gprs_check_pin()
{

    utl_log_data "gprs_check_pin" "Checking PIN"

    # Il pin deve essere presente nel file, in corrispondenza dell'ICCID
    # SIM.csv
    # <ICCID>;<PIN>;<PUK>
    # Cerco il pin nel file della pennetta
    if [ -z "$(grep "$V_GPRS_SCID" "$C_GPRS_SIM_ARCHIVE")" ]; then

        echo "$V_GPRS_SCID;<sconosciuto>;" >> "$C_GPRS_SIM_ARCHIVE"
        utl_log_error "gprs_check_pin" " Reading pin: Not present!"

    fi

    V_GPRS_PIN=$(grep "$V_GPRS_SCID" "$C_GPRS_SIM_ARCHIVE" | cut -d';' -f2)

    if [ ${#V_GPRS_PIN} -ne 4 ]; then

        utl_log_error "gprs_check_pin" " Lunghezza del pin errata"

    else

        gprs_send_cmd "AT+CPIN=$V_GPRS_PIN"
        utl_log_data "gprs_check_pin" " Pin $V_GPRS_PIN OK"

    fi

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_init()
# Descrizione: Apro la porta seriale, ed interrogo il modem chiedendo IMEI, SCID e segnale
#   Parametri: Nessuno
#     Globali: C_GPRS_DEV
# -----------------------------------------------------------------------------------------------------------
gprs_init()
{

    utl_log_data "gprs_init" "Inizializzo il modem"

    # Imposta la porta seriale e la apre
    utl_log_data "gprs_init" "  Apertura della porta"
    stty -F "$C_GPRS_DEV" 115200 -echo igncr -icanon onlcr crtscts -ixon min 0 time 10
    exec 5<"$C_GPRS_DEV"
    exec 6>"$C_GPRS_DEV"

    # Accendo il modem
    gprs_on

    utl_log_data "gprs_init" "  Caricamento dati dal modem"

    gprs_send_cmd "AT+IPR?"
    if [ "$V_GPRS_IPR" != "115200" ]
    then
        gprs_send_cmd "AT+IPR=115200"
        gprs_send_cmd "AT&W"
    fi
    gprs_send_cmd "AT+CSQ"
    gprs_send_cmd "AT^SCID"
    gprs_send_cmd "AT^MONI"
    gprs_send_cmd "AT+CGSN"

    gprs_check_pin

    gprs_send_cmd "AT+CIMI"

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_deinit()
# Descrizione: Chiudo la porta seriale
#   Parametri: Nessuno
#     Globali: C_GPRS_DEV
# -----------------------------------------------------------------------------------------------------------
gprs_deinit()
{

    utl_log_data "gprs_deinit" "Chiusura della porta"

    # Chiudo la seriale
    exec 5<&-
    exec 6>&-

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_on()
# Descrizione: Accendo il modem
#   Parametri: Nessuno
#     Globali: V_GPRS_STATUS
# -----------------------------------------------------------------------------------------------------------
gprs_on()
{

    utl_log_data "gprs_on" "Avvio del modem"

    V_GPRS_STATUS=$(dd if=/dev/gsm_status count=1 bs=1 2>/dev/null | hexdump -e '1/1 "%X\n"')

    # Se il modem e' attivo non faccio niente
    if [ "$V_GPRS_STATUS" -eq 0 ]
    then

        utl_log_data "gprs_on" " Inizializzazione dei segnali"
        echo -n 0 > /dev/gsm_on
        echo -n 0 > /dev/gsm_reset
        echo -n 0 > /dev/gsm_ignition
        sleep 1

        utl_log_data "gprs_on" " Abilitazione del segnale ON"
        echo -n 1 > /dev/gsm_on
        sleep 1

        utl_log_data "gprs_on" " Abilitazione del segnale IGNITION"
        echo -n 1 > /dev/gsm_ignition
        sleep 1
        echo -n 0 > /dev/gsm_ignition

        # Se non e' stato configurato l'IPR, non arriva alcuna risposta
        if [ "$V_GPRS_IPR" == "115200" ]
        then
                gprs_catch_response
            else
                sleep 10
        fi

    else

        utl_log_data "gprs_on" " Modem gia' attivo"

    fi

}


# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_off()
# Descrizione: Spegne il modem
#   Parametri: Nessuno
#     Globali: V_GPRS_STATUS
#              V_GPRS_PPPD_STATUS
#              V_GPRS_MUX_STATUS
# -----------------------------------------------------------------------------------------------------------
gprs_off()
{

    utl_log_data "gprs_off" "Arresto del modem"

    V_GPRS_STATUS=$(dd if=/dev/gsm_status count=1 bs=1 2>/dev/null | hexdump -e '1/1 "%X\n"')
    V_GPRS_PPPD_STATUS=$(ps | grep pppd | grep -v grep | awk '{print $1}')

    # Se il demone ppp e' attivo, lo spengo
    if [ "${#V_GPRS_PPPD_STATUS}" -ne 0 ]
    then
        utl_log_data "gprs_off" " Disattivazione demone ppp"
        chroot /mnt2 poff
    fi

    # Controllo se c'e' un errore
    T_CNT=30
    while [ "$T_CNT" -gt 0 ] && [ "${#V_GPRS_PPPD_STATUS}" -ne 0 ]
    do
        V_GPRS_PPPD_STATUS=$(ps | grep pppd | grep -v grep | awk '{print $1}')
        let T_CNT--
        sleep 1
    done
    if [ "${#V_GPRS_PPPD_STATUS}" -ne 0 ]; then
        utl_log_error "gprs_off" " Errore durante la disattivazione del demone pppd"
        return 1
    else
        utl_log_data "gprs_off" " Demone ppp disconnesso"
    fi

    # Se il modem e' attivo non faccio niente
    if [ "$V_GPRS_STATUS" -eq 1 ]; then

        utl_log_data "gprs_off" " Spegnimento del modem"

        # Non basta spegnere l'alimentazione ?!?!?!?
        gprs_send_cmd "AT^SMSO"


        # TODO: Se non arriva ^SHUTDOWN?

    else

        utl_log_data "gprs_off" " Modem gia' disattivo"

    fi

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_reset()
# Descrizione: Riavvia il modem
#   Parametri: Nessuno
# -----------------------------------------------------------------------------------------------------------
gprs_reset()
{
    utl_log_data "Resetting the modem"
    echo -n 1 > /dev/gsm_reset
    usleep 200000
    echo -n 0 > /dev/gsm_reset
}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_send_cmd()
# Descrizione: Invia un comando AT
#   Parametri: Nessuno
#     Globali: &6 input della seriale del modem
#              V_GPRS_AT_CMD
# -----------------------------------------------------------------------------------------------------------
gprs_send_cmd()
{

    V_GPRS_AT_CMD="$1"

    echo -e -n "${V_GPRS_AT_CMD}\015" >&6

    # Solo per logging
    if [ "$C_GPRS_DEBUG" -eq 1 ]
    then
        echo "> '$V_GPRS_AT_CMD'"
    fi

    # Fino a quando non ricevo OK o ERROR o +CME non smetto
    gprs_catch_response

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: gprs_catch_response()
# Descrizione: Riceve la risposta ad un comando
#   Parametri: Nessuno
#     Globali: &5 output della seriale del modem
#              V_GPRS_CMD_RESP -> Risposta ricevuta
# -----------------------------------------------------------------------------------------------------------
gprs_catch_response()
{

    local T_RESP_HDR="\015"
    local T_SEARCHING=1               # Sto attendendo una risposta valida dal modem
    local T_RESP=""                   # Dati letti dal modem
    local T_RESP_LINE=0               # Numero di linea ricevuta dal modem
    local T_RETRY=0

    # Finche' ricevo OK / ERROR / +CME ERROR oppure provo per 20 volte...
    while [ "$T_SEARCHING" -eq 1 ]
    do

        # Provo a leggere
        read T_RESP <&5
        let T_RESP_LINE++

        # Se la linea contiene qualcosa di valido...
        if [ "${#T_RESP}" -gt 1 ]
        then

            # Solo per logging
            if [ "$C_GPRS_DEBUG" -eq 1 ]
            then
                echo "<$T_RESP_LINE: $T_RESP"
	    fi

            # Prendo l'header della risposta
            utl_parse "$T_RESP" "\(OK\|ERROR\|[^:]*\).*" T_RESP_HDR

            # Per prima cosa controllo OK, ERROR, e tutto quanto finisce con :
            case "$T_RESP_HDR" in

                "OK")

                    # Se sto spegnendo il modem, attendo ^SHUTDOWN
                    if [ "$V_GPRS_AT_CMD" != "AT^SMSO" ]
                    then
                        V_GPRS_CMD_RESP=1;
                        T_SEARCHING=0;
                    else
                        utl_log_data "gprs_catch_response" " Attendo il termine dello shutdown"
                    fi
                    ;;

                "ERROR"|"+CME ERROR"|"NO CARRIER")

                    utl_log_data "gprs_catch_response" " ERR"
                    V_GPRS_CMD_RESP=0
                    return 1
                    ;;

                "^SYSSTART" )

                    utl_log_data "gprs_catch_response" " STARTED!"
                    V_GPRS_POWERUP=1
                    # Se stavo attendendo la risposta ad un altro comando continuo
                    if [ "${#V_GPRS_AT_CMD}" -eq 0 ]
                    then
                      T_SEARCHING=0
                    fi
                    ;;

                "^SHUTDOWN" )

                    utl_log_data "gprs_cathc_response" " Disabilitazione del segnale ON"
                    echo -n 0 > /dev/gsm_on
                    sleep 1
                    V_GPRS_SHUTDOWN=1
                    T_SEARCHING=0
                    ;;

                #">" )
                #  echo -e -n "Test da ABT21\015" >&6

                "+IPR" )

                    utl_parse "$T_RESP" "+IPR: \([0-9]*\)" V_GPRS_IPR
                    utl_log_data "gprs_catch_response" "  GPRS IPR = '$V_GPRS_IPR'"
                    ;;


                "+CSQ" )

                    # +CSQ: (<rssi>), (<ber>)
                    # <rssi>
                    #   0 -113 dBm or less
                    #   1 -111 dBm
                    #   2..30 -109... -53 dBm
                    #   31 -51 dBm or greater
                    #   99 not known or not detectable
                    utl_parse "$T_RESP" "+CSQ: \([0-9]*\),[0-9]*.*" V_GPRS_RSSI
                    utl_log_data "gprs_catch_response" " GPRS RSSI = '$V_GPRS_RSSI'"
                    ;;

                "^SCID" )

                    utl_parse "$T_RESP" "\^SCID: \([0-9]*\)" V_GPRS_SCID
                    utl_log_data "gprs_catch_response" "    SIM ID = '$V_GPRS_SCID'"
                    ;;


            esac

            # Alcuni comandi inseriscono risposte prima dell'OK
            case "$V_GPRS_AT_CMD" in

                "AT^MONI" )

                    # La quarta linea contiene i dati
                    if [ "$T_RESP_LINE" -eq 4 ]
                    then
                        V_GPRS_DBM=$(echo "$T_RESP" | awk '{ print $3 }')
                        #utl_parse "$T_RESP" "\^SCID: \([0-9]*\)" V_GPRS_DBM
                        utl_log_data "gprs_catch_response" "       DBM = '$V_GPRS_DBM'"
                    fi
                    ;;

                "AT+CGSN" )

                    # La seconda linea contiene l'IMEI
                    if [ "$T_RESP_LINE" -eq 2 ]
                    then
                        V_GPRS_IMEI="$T_RESP"
                        utl_log_data "gprs_catch_response" "      IMEI = '$V_GPRS_IMEI'"
                    fi
                    ;;

                "AT+CIMI" )

                    # La seconda linea contiene l'IMEI
                    if [ "$T_RESP_LINE" -eq 2 ]
                    then
                        V_GPRS_IMSI="$T_RESP"
                        utl_log_data "gprs_catch_response" "      IMSI = '$V_GPRS_IMSI'"
                    fi
                    ;;

            esac

        else

            let T_RETRY+=1
            if [ "$T_RETRY" -gt "$C_GPRS_MAX_RETRY" ]
            then
                utl_log_data "gprs_catch_response" "Numero massimo di tentativi di ricezione dati raggiunto."
                T_SEARCHING=0
            fi

        fi

    done

}

# -----------------------------------------------------------------------------------------------------------
# Modulo di utilita
# -----------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_log_data()
# Descrizione: Formatta i messaggi di logging
#   Parametri: $1, Funzione
#              $2, Messaggio da inviare
#    Costanti: C_DEBUG, se pari ad 0 cripta il messaggio
# -----------------------------------------------------------------------------------------------------------
utl_log_data()
{
    local T_AON="\033[37;44m"
    local T_AOFF="\033[0m"
    #local V_TMP_TIMESTAMP=$(date +"%d/%m/%y %H:%M:%S")

    if [ -z "$C_DEBUG" ]
    then
       if [ "${2:0:1}" == " " ]
       then
           printf "%020s(): %s\n" "$1" "$2" | tr "a-z" "A-Z" | tr "A-Z" "$C_KEY"
       else
           printf "${T_AON}%020s(): %s${T_AOFF}\n" "$1" "$2" | tr "a-z" "A-Z" | tr "A-Z" "$C_KEY"
       fi
    else
       if [ "${2:0:1}" == " " ]
       then
           printf "%020s(): %s\n" "$1" "$2"
       else
           printf "${T_AON}%020s(): %s${T_AOFF}\n" "$1" "$2"
       fi
    fi
}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_log_error()
# Descrizione: Formatta i messaggi di errore nel logging
#   Parametri: $1, Funzione
#              $2, Messaggio da inviare
#    Costanti: C_DEBUG, se pari ad 0 cripta il messaggio
# -----------------------------------------------------------------------------------------------------------
utl_log_error()
{
    local T_AON="\033[49;91m"
    local T_AOFF="\033[0m"
    #local V_TMP_TIMESTAMP=$(date +"%d/%m/%y %H:%M:%S")

    if [ -z "$C_DEBUG" ]; then
        printf "${T_AON}%020s(): %s%s${T_AOFF}\n" "$1" "$2" | tr "a-z" "A-Z" | tr "A-Z" "$C_KEY"
    else
        printf "${T_AON}%020s(): %s%s${T_AOFF}\n" "$1" "$2"
    fi

    # TODO: Se non in debug, salva l'errore sulla pen ed esce
    printf "%020s(): %s%s" "$1" "$2" > "/mnt/error_$V_GPRS_SCID"
    utl_change_led 1 0
    exit
    utl_wait_and_shutdown
}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_change_led()
# Descrizione: Cambia lo stato dei led
#   Parametri: $1: 1 o 0, stato del LED rosso
#              $2: 1 o 0, stato del LED verde
#    Costanti: Nessuna
# -----------------------------------------------------------------------------------------------------------
utl_change_led()
{
    if [ "$#" -eq 2 ]; then
        if [ "$1" -eq 1 ]; then
            echo -n 1 > /dev/red_led
        else
            echo -n 0 > /dev/red_led
        fi
        if [ "$2" -eq 1 ]; then
            echo -n 1 > /dev/green_led
        else
            echo -n 0 > /dev/green_led
        fi
    else
        utl_log_error "utl_change_led" "Errore, numero di parametri errati"
    fi
}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_parse()
# Descrizione: Regular expression parser
#   Parametri: $1: Stringa da analizzare
#              $2: Espressione regolare
#              $3: Variabile in cui memorizzare il risultato
#    Costanti: Nessuna
# -----------------------------------------------------------------------------------------------------------
utl_parse()
{

    local T_UTL_CMD_EXEC="echo '$1' | sed -n 's/$2/\\1/p'"
    local T_UTL_PARSED=""

    # Cerco la stringa
    T_UTL_PARSED=$(eval $T_UTL_CMD_EXEC)

    # Se ho trovato qualcosa...
    if [ "${#T_UTL_PARSED}" -gt 0 ]
    then
        eval "$3=\"$T_UTL_PARSED\""
    else
        eval "$3=\"\""
    fi

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_wait_and_reboot()
# Descrizione: Attende il disinserimento della pennetta e riavvia la centralina
#   Parametri: $1: Stringa da analizzare
#              $2: Espressione regolare
#              $3: Variabile in cui memorizzare il risultato
#    Costanti: Nessuna
# -----------------------------------------------------------------------------------------------------------
utl_wait_and_reboot()
{

    sync

    utl_log_data "utl_wait_and_reboot" "Attendo il disinserimento della pennetta e riavvio"

    utl_log_data "utl_wait_and_reboot" " Attendo il disinserimento della pennetta"
    USB_PEN=$(cat /proc/bus/usb/devices | grep Cls=08)
    while [ "${#USB_PEN}" -gt 0 ]
    do
        usleep 250000
        USB_PEN=$(cat /proc/bus/usb/devices | grep Cls=08)
    done
    utl_log_data "utl_wait_and_reboot" " Pennetta disinserita"
    utl_log_data "utl_wait_and_reboot" " Riavvio"
    sleep 2
    trap - TERM INT
    reboot
    exit 1

}

# -----------------------------------------------------------------------------------------------------------
#    Funzione: utl_wait_and_shutdown()
# Descrizione: Attende il disinserimento della pennetta e riavvia la centralina
#   Parametri: $1: Stringa da analizzare
#              $2: Espressione regolare
#              $3: Variabile in cui memorizzare il risultato
#    Costanti: Nessuna
# -----------------------------------------------------------------------------------------------------------
utl_wait_and_shutdown()
{

    sync

    utl_log_data "utl_wait_and_shutdown" "Attendo il disinserimento della pennetta e spengo"

    utl_log_data "utl_wait_and_shutdown" " Attendo il disinserimento della pennetta"
    USB_PEN=$(cat /proc/bus/usb/devices | grep Cls=08)
    while [ "${#USB_PEN}" -gt 0 ]
    do
        usleep 250000
        USB_PEN=$(cat /proc/bus/usb/devices | grep Cls=08)
    done
    utl_log_data "utl_wait_and_shutdown" " Pennetta disinserita"
    utl_log_data "utl_wait_and_shutdown" " Spengo"
    sleep 2
    trap - TERM INT
    poweroff
    exit 1

}

# Esegue il backup dei dati presenti prima del riavvio, che avviene unicamente al termine dello script
#   - Carico i dati in delle variabili
#   - TODO Eseguo il backup nella pennetta, nella directory ***
#   - L'ID me lo da il nuovo DB
#   - Il pin deve essere corretto perche' verra' controllato
# -----------------------------------------------------------------------------------------------------------
backup_data()
{

    utl_log_data "backup_data" "Controllo i files presenti"
    mkdir -p "/mnt/tmp/$V_GPRS_IMEI"

    if [ -e /mnt2/etc/sysconfig/prodinfo.d ]; then
        utl_log_data "backup_data" " PROD: $(cat /mnt2/etc/sysconfig/prodinfo.d)"
        cp /mnt2/etc/sysconfig/prodinfo.d "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_prodinfo.d"
    else
        utl_log_data "backup_data" " PROD: no-files"
    fi

    if [ -e /mnt2/etc/sysconfig/errinfo.d ]; then
        utl_log_data "backup_data" " ERR: $(cat /mnt2/etc/sysconfig/errinfo.d)"
        cp /mnt2/etc/sysconfig/errinfo.d "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_errinfo.d"
    else
        utl_log_data "backup_data" " ERR: no-files"
    fi

    sync

}

# Rimette a posto i files
# -----------------------------------------------------------------------------------------------------------
restore_data()
{

    utl_log_data "restore_data" "Ricopio i files"

    if [ -e "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_prodinfo.d" ]; then
        cp "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_prodinfo.d" /mnt2/etc/sysconfig/prodinfo.d
        utl_log_data "restore_data" " PROD: $(cat /mnt2/etc/sysconfig/prodinfo.d)"
    else
        utl_log_data "restore_data" " PROD: no-files"
    fi

    if [ -e "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_errinfo.d" ]; then
        cp "/mnt/tmp/$V_GPRS_IMEI/etc_sysconfig_errinfo.d" /mnt2/etc/sysconfig/errinfo.d
        utl_log_data "restore_data" " ERR: $(cat /mnt2/etc/sysconfig/errinfo.d)"
    else
        utl_log_data "restore_data" " ERR: no-files"
    fi

    mkdir -p /mnt2/etc/fuelcheck

    echo "$V_GPRS_PIN;$V_GPRS_SCID" > /mnt2/etc/fuelcheck/pin
    utl_log_data "restore_data" " PIN: $(cat /mnt2/etc/fuelcheck/pin)"

    echo "$V_GPRS_IMEI" > /mnt2/etc/fuelcheck/imei
    utl_log_data "restore_data" " IMEI: $(cat /mnt2/etc/fuelcheck/imei)"

    sync

}


# Monta la root partition in /mnt2
# -----------------------------------------------------------------------------------------------------------
mount_root()
{

    V_MNT=$(cat /proc/mounts | grep /mnt2)

    utl_log_data "mount_root" "Monto la root partition"

    if [ "${#V_MNT}" -gt 0 ]; then
        utl_log_data "mount_root" " Gia' montata"
        return
    fi

    mkdir -p /mnt2
    /usr/bin/ubiattach /dev/ubi_ctrl -m 3 >/dev/null 2>&1
    if [ "$?" = "0" ]; then
        utl_log_data "mount_root" " ubiattach ok"
    else
        utl_log_error "mount_root" " ubiattach fail"
    fi
    usleep 100000

    mount -t ubifs ubi0_0 /mnt2 >/dev/null 2>&1
    if [ "$?" = "0" ]; then
        utl_log_data "mount_root" " mount ok"
    else
        utl_log_error "mount_root" " mount fail"
    fi
    usleep 100000

    # Preparo per chroot
    mount --bind /proc /mnt2/proc
    mount --bind /var  /mnt2/var
    mount --bind /mnt  /mnt2/mnt

}

# Smonta la root partition
# -----------------------------------------------------------------------------------------------------------
umount_root()
{

    V_MNT=$(cat /proc/mounts | grep /mnt2)

    utl_log_data "umount_root" "Smonto la root partition"

    umount /mnt2/mnt
    umount /mnt2/proc
    umount /mnt2/var

    if [ "${#V_MNT}" -le 0 ]; then
        utl_log_data "umount_root" " Gia' smontata"
        return
    fi

    sync
    sleep 2
    umount /mnt2 >/dev/null 2>&1
    if [ "$?" = "0" ]; then
        utl_log_data "umount_root" " umount ok"
    else
        utl_log_error "umount_root" " umount fail"
    fi
    sleep 1

    /usr/bin/ubidetach /dev/ubi_ctrl -m 3 >/dev/null 2>&1
    if [ "$?" = "0" ]; then
        utl_log_data "umount_root" " ubidetach ok"
    else
        utl_log_error "umount_root" " ubidetach fail"
    fi
    sleep 1

}


# Installa la BSP01
# -----------------------------------------------------------------------------------------------------------
install_bsp01()
{

    utl_log_data "install_bsp01" "Installazione BSP 01"

    # Inizio l'installazione partendo da 0
    if [ -f "/mnt/abt21-ubifs.img" -a -f  "/mnt/abt21-uImage" -a -f "/mnt/abt21_ivt_uboot.sb" ]
    then

        # Mi copio gli unici files che sono diversi per ogni centralina
        mount_root
        backup_data
        umount_root

        # Formatto ed installo la root partition
        utl_log_data "install_bsp01" " Installo la root partition mtd3"
        /usr/bin/flash_eraseall /dev/mtd3 >/dev/null 2>&1
        if [ "$?" = "0" ]; then
            utl_log_data "install_bsp01" " flash_eraseall ok"
        else
            utl_log_error "install_bsp01" " flash_eraseall fail"
        fi
        /usr/bin/ubiformat /dev/mtd3 -s 2048 -f /mnt/abt21-ubifs.img >/dev/null 2>&1
        if [ "$?" = "0" ]; then
            utl_log_data "install_bsp01" " ubiformat ok"
        else
            utl_log_error "install_bsp01" " ubiformat fail"
        fi

        # Ricopio i files che sono diversi per ogni centralina
        mount_root
        restore_data
        umount_root

        # Cancello mtd1
        /usr/bin/flash_eraseall /dev/mtd1 >/dev/null 2>&1
        if [ "$?" = "0" ]; then
            utl_log_data "install_bsp01" " flash_eraseall_mtd1 ok"
        else
            utl_log_error "install_bsp01" " flash_eraseall_mtd1 fail"
        fi

        # Formatto ed installo mtd0
        /usr/bin/flash_eraseall /dev/mtd0 >/dev/null 2>&1
        if [ "$?" = "0" ]; then
            utl_log_data "install_bsp01" " flash_eraseall_mtd0 ok"
        else
            utl_log_error "install_bsp01" " flash_eraseall_mtd0 fail"
        fi

        /usr/bin/kobs-ng init -v /mnt/abt21_ivt_uboot.sb >/dev/null 2>&1
        if [ "$?" = "0" ]; then
            utl_log_data "install_bsp01" " kobs-ng ok"
        else
            utl_log_error "install_bsp01" " kobs-ng fail"
        fi

        sync

        sleep 1

    else

        utl_log_error "install_bsp01" " La pennetta non contiene tutti i files necessari!"

    fi

}

# Installa la BSP03
# -----------------------------------------------------------------------------------------------------------
install_bsp03()
{

    # Inizio l'installazione partendo da 0
    if [ -f "/mnt/ABT21-BSP-01-update-03-data.tgz" ]; then

        # Eseguo l'aggiornamento della nuova root alla 03

        utl_log_data "install_bsp03" "Aggiornamento alla 03"

        mount_root

        tar xvzf /mnt/ABT21-BSP-01-update-03-data.tgz -C /mnt2 >/dev/null 2>&1
        if [ "$?" = "0" ]; then

            utl_log_data "install_bsp03" " Decomprimo l'aggiornamento ok"

            /usr/bin/flash_eraseall /dev/mtd2 >/dev/null 2>&1
            if [ "$?" = "0" ]; then
                utl_log_data "install_bsp03" " flash_eraseall_mtd2 ok"
            else
                utl_log_error "install_bsp03" " flash_eraseall_mtd2 fail"
            fi

            /usr/bin/nandwrite -p -m /dev/mtd2 /mnt2/var/tmp/abt21-uImage >/dev/null 2>&1
            if [ "$?" = "0" ]; then
                utl_log_data "install_bsp03" " nandwrite_mtd2 ok"
            else
                utl_log_error "install_bsp03" " nandwrite_mtd2 fail"
            fi

            /usr/bin/flash_eraseall /dev/mtd0 >/dev/null 2>&1
            if [ "$?" = "0" ]; then
                utl_log_data "install_bsp03" " flash_eraseall_mtd0 ok"
            else
                utl_log_error "install_bsp03" " flash_eraseall_mtd0 fail"
            fi

            /usr/bin/kobs-ng init -v /mnt2/var/tmp/abt21_ivt_uboot.sb >/dev/null 2>&1
            if [ "$?" = "0" ]; then
                utl_log_data "install_bsp03" " kobs-ng ok"
            else
                utl_log_error "install_bsp03" " kobs-ng fail"
            fi

            echo "ABT21-BSP-01-update-03" >> /mnt2/etc/sysconfig/bspinfo.d

        else

            utl_log_error "install_bsp03" " tar fail"

        fi

        umount_root

    else

        utl_log_error "install_bsp03" " File ABT21-BSP-01-update-03-data.tgz non trovato!"

    fi

}


# Controlla la presenza di tutto quanto richiesto per il funzionamento del programma
# -----------------------------------------------------------------------------------------------------------
environment_init()
{

    utl_log_data "environment_init" "Initialize environment"

    # TODO: dovrebbe aggiungere le linee in un punto preciso
    # TODO: dovrebbe sostituire getty con un REPL Read Evaluate Print Loop

    # Installo l'avvio del firmware
    V_MD5="dde346d1eed122888c8423987a640100"
    V_FILE="/mnt2/etc/inittab"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " inittab backup"

        fi

    cat <<- 'EOF' >> "$V_FILE"
2:2345:respawn:/usr/bin/screen -D -m /opt/fuelcheck_fw/fc_mcp.sh
3:2345:respawn:/usr/bin/screen -D -m /opt/fuelcheck_fw/fc_autorestart.sh
EOF

        utl_log_data "environment_init" " inittab writing"

    else

        utl_log_data "environment_init" " inittab already present"

    fi

    # Controllo la presenza dello script di avvio
    V_MD5="6bd4ab5bf13be6f04aabc4e11bea0b0e"
    V_FILE="/mnt2/etc/init.d/local.sh"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " local.sh backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
#!/bin/sh

#echo "Mounting roots RO"
#mount -o remount,ro /

## Here you can add the user applications launch ##

# Inizializzo i file temporanei
touch /tmp/known_hosts
touch /tmp/resolv.conf

# Creo l'interfaccia di loopback
ifup lo

# Avvio il server ssh
dropbear
EOF

        utl_log_data "environment_init" " local.sh writing"

    else

        utl_log_data "environment_init" " local.sh already present"

    fi

    # Controllo la presenza del workaround per i rimorchi a 12V
    V_MD5="3646da9daa9a2b3669d4d9574f3527e1"
    V_FILE="/mnt2/etc/init.d/halt"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " halt backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
#!/usr/bin/env sh
#
# halt          Execute the halt command.
#
# Version:      @(#)halt  2.84-2  07-Jan-2002  miquels@cistron.nl
#
PATH=/sbin:/bin:/usr/sbin:/usr/bin

# See if we need to cut the power.
if test -x /etc/init.d/ups-monitor
then
  /etc/init.d/ups-monitor poweroff
fi

# Don't shut down drives if we're using RAID.
hddown="-h"
if grep -qs '^md.*active' /proc/mdstat
then
  hddown=""
fi

if [ ! -f /real_halt ]
then
  /sbin/close_devices
  sleep 1
  echo -ne '\0001\0100\0000\0000' > /dev/sleep_mask
  echo -ne '\0000\0000\0000\0000' > /dev/sleep_mask_level
  echo -ne '\0001\0000\0000\0000' > /dev/sleep_mask_pol
  echo "System halted."
  usleep 100000
  echo -n 0 > /dev/com1_dxen
  echo -n 0 > /dev/com1_enable
  umount -f -a -r > /dev/null 2>&1
  dd if=/dev/sleep_mask bs=4 count=1 > /dev/null 2>&1
  sleep 3
  echo -ne '\0001\0100\0000\0000' > /dev/sleep_mask_level
  dd if=/dev/sleep_mask bs=4 count=1 > /dev/null 2>&1
  echo -n 1 > /dev/com1_enable
  echo -n 1 > /dev/com1_dxen
  echo "Rebooting..."
  reboot -d -f -i
else
  halt -d -f -i -p $hddown
fi

: exit 0
EOF

        utl_log_data "environment_init" " halt writing"

    else

        utl_log_data "environment_init" " halt already present"

    fi

    # Controllo la configurazione della shell
    V_MD5="7c8fdd2632f32e0c5ece87da6a9c5e80"
    V_FILE="/mnt2/home/root/.profile"
    if [ "$(md5sum "$V_FILE" 2>/dev/null | awk '{print $1}')" != "$V_MD5" ]; then

        if [ -e "$V_FILE" ] && [ ! -e "$V_FILE.old" ]; then

            cp "$V_FILE" "$V_FILE.old"

            utl_log_data "environment_init" " profile backup"

        fi

        cat <<- 'EOF' > "$V_FILE"
alias ls='ls -l --color=auto'
alias pstree='pstree -p -h'
stty rows 40 2>/dev/null
stty cols 136 2>/dev/null
PATH="/opt/fuelcheck_fw/binutils:/opt/fuelcheck_fw:/opt/fuelcheck_bt:/home/root/fuelcheck/fw:/home/root/fuelcheck/fw/binutils:/home/root/fuelcheck/fw/admin:$PATH"
EOF

        utl_log_data "environment_init" " profile writing"

    else

        utl_log_data "environment_init" " profile already present"

    fi

    # Salva l'SN
    echo "abt21-${V_GPRS_IMEI:8:6}" > /mnt2/etc/hostname
    echo "${V_GPRS_IMEI:8:6}" > /mnt2/etc/fuelcheck/id

    # Cambio la password di root KIkd2k9QubiAA76bF9ZZI3Xo
    if [ ! -z "$C_CHANGEPW" ] >/dev/null; then
      chroot /mnt2 touch /etc/shadow
      chroot /mnt2 echo "root:KIkd2k9QubiAA76bF9ZZI3Xo" | chroot /mnt2 /usr/sbin/chpasswd 2>&1 >/dev/null
      if [ "$?" = "0" ]; then
        utl_log_data "environment_init" " Changing pwd ok"
      else
        utl_log_error "environment_init" " Changing pwd fail"
      fi
    fi

}

# ----------------------------------------------------------------------------------------------------------
# Funzione:    installer_cleanup()
# Descrizione: Chiude il programma
# Parametri:   Nessuno
# Restituisce: Nessuno
# ----------------------------------------------------------------------------------------------------------
installer_cleanup()
{

    installer_deinit
    utl_change_led 0 0
    exit 255

}

# ----------------------------------------------------------------------------------------------------------
# Funzione:    installer_deinit()
# Descrizione: Predispone l'installazione
# Parametri:   Nessuno
# Restituisce: Nessuno
# ----------------------------------------------------------------------------------------------------------
installer_deinit()
{

    gprs_off
    gprs_deinit
    umount_root

}

main_loop()
{

    # Inizio dell'installazione
    utl_log_data "main_loop" "Avvio installazione"

    # Accendo il led verde, carico il modulo del watchdog
    utl_change_led 0 1
    modprobe pindog

    # Monto var
    mount -t tmpfs tmpfs /var
    mkdir /var/tmp
    mkdir /var/lock

    # Elimino i messaggi di sistema a console
    echo "1" > /proc/sys/kernel/printk

    # Inizializza il modem
    gprs_init

    # Forse potrei annullarlo, ma preferisco partire da una versione nota...
    install_bsp01
    install_bsp03

    # Ora possiedo una root partition completa, posso installare i files
    mount_root

    # Aggiorno tutti i files per le connessioni ssh
    gprs_init_files

    # Ora aggiorno i pacchetti
    opkg_install_all

    # Solo ora c'e' ntpdate...
    gprs_connect
    gprs_update_clock

    # Correggo il python
    mkdir /mnt2/usr/lib/python2.6/site-packages/zope
    touch /mnt2/usr/lib/python2.6/site-packages/zope/__init__.py
    chroot /mnt2 ln -s /usr/lib/python2.6/site-packages/zope.interface-3.5.1-py2.6-linux-x86_64.egg/zope/interface/ /usr/lib/python2.6/site-packages/zope/interface

    # TODO aggiungerlo
    #rsync -av --progress pritijen.webhop.org:/usr/lib/python2.6/optparse.py /usr/lib/python2.6/

    environment_init

    # TODO da remoto!
    mkdir /mnt2/opt/fuelcheck_fw
    tar xzvf /mnt/fw_v1.1.15-16-g0ecee93.tar.gz -C /mnt2/opt/fuelcheck_fw/
    mv /mnt2/opt/fuelcheck_fw/VERSION /mnt2/etc/fuelcheck/version
    mv /mnt2/opt/fuelcheck_fw/etc_fuelcheck_config /mnt2/etc/fuelcheck/config
    mv /mnt2/opt/fuelcheck_fw/abaa21 /mnt2/usr/bin/

    installer_deinit

    utl_change_led 0 1
    utl_wait_and_reboot

}

# -----------------------------------------------------------------------------------------------------------
# Inizio della procedura
# -----------------------------------------------------------------------------------------------------------

# Nessuna variabile orfana
set -u

# Esci con CTRL-C
trap installer_cleanup TERM INT

main_loop
