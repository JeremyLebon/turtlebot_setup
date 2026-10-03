# Uitvoeringslogboek - ap-migration

Logboek van de effectieve uitvoering, per unit. Volgorde volgt
`ap-migration.md`. Enkel echt uitgevoerde stappen staan hier - voor de
generieke instructies/het netwerkplan zie `ap-migration.md`.

## turtlebot09 - eerste unit (2026-10-03)

**Robot:** turtlebot09, RPi5, was bereikbaar op `192.168.60.249`
(gedeeld `Wifi_turtlebots`-net), nu op `10.0.9.10` (eigen AP).

### AP configureren

Fabrieks-SSID bij opstarten: `TP-Link_090A` (2,4GHz) /
`TP-Link_090A_5G` (5GHz), beveiligd met het sticker-wachtwoord. AP stond
fysiek op ~1m van de robot, ethernetpoort al aangesloten op de gedeelde
switch (bevestigd: voor de LAN-IP-wijziging was de AP via zijn WAN-kant
al bereikbaar op het gedeelde `192.168.60.0/24`-net - duidt erop dat de
unit uit de doos al automatisch in router-modus staat zodra WAN
aangesloten is, nog te bevestigen of dit op elke unit zo is).

Configuratie via de browser-wizard op `tplinkwifi.net`/`192.168.0.1`
(JS/RSA-based login, niet scriptbaar via curl - bewust niet geprobeerd,
zie `ap-migration.md`):
- Router-modus, WAN: Dynamic IP.
- SSID `TB-AP-09`, wachtwoord `TurtleBot@P09` (per-robot wachtwoord,
  i.p.v. het in `ap-migration.md` voorgestelde gedeelde wachtwoord - zie
  bijgewerkte tabel/toelichting in dat document).
- Kanaal 5GHz vast op 36, 2,4GHz vast op 11.
- LAN-IP gewijzigd naar `10.0.9.1`, DHCP-range `10.0.9.100-200`.
- DHCP-reservatie toegevoegd: MAC `88:A2:9E:2C:EA:4D` (turtlebot09) ->
  `10.0.9.10`.

### Robot overschakelen (via SSH)

Robot bleef bereikbaar op zijn oude adres (`192.168.60.249`) tijdens de
hele AP-configuratie, via de AP's WAN-NAT-route (extra hop, ttl -1) -
handig om te blijven verbinden terwijl de AP herconfigureerd werd.

Overschakelen bleek niet mogelijk als gewone SSH-user:
```
nmcli device wifi connect "TB-AP-09" password "TurtleBot@P09" ifname wlan0
Error: Failed to add/activate new connection: Not authorized to control networking.
```
Ook `nmcli device wifi rescan` en `nmcli radio wifi off/on` gaven
`Not authorized` zonder sudo. **Nog te onderzoeken voor de fleet-uitrol**:
de `turtlebot`-user hoort blijkbaar niet bij de polkit-groep die
NetworkManager-acties (scan/connect/radio) mag doen - met `sudo` werkt
het direct wel. Voor 8 herhalingen is dit geen probleem (sudo-wachtwoord
gekend), maar als dit ooit via een onbemand script moet (bv.
`setup_turtlebot.sh`-achtige automatisering), moet de polkit-regel of
groepslidmaatschap aangepast worden.

Met `sudo` (wachtwoord: zie eigen wachtwoordbeheer) werkte de omschakeling
meteen. **Let op**: het `nmcli ... connect`-commando via SSH uitgevoerd
verbreekt de eigen SSH-sessie zodra wlan0 effectief overschakelt (het pad
waarover de SSH-sessie loopt verdwijnt) - commando blijft op de achtergrond
hangen/timeout, maar de omschakeling zelf lukt wel. Nieuwe SSH-sessie
openen naar het nieuwe IP om verder te gaan.

### Resultaat: jitter-test

```
ping -c 20 10.0.9.10
rtt min/avg/max/mdev = 1.117/5.214/6.436/1.368 ms
```

Tegenover de eerder gemeten ~55ms mdev op het gedeelde net (zie
`raspios-migration-log.md`, "WSL-test + netwerkdiagnose") - **bevestigt
de AP-isolatie lost het jitter-probleem op.**

### Volledige stack-test (statuspagina + rosbridge)

Container `turtlebot_99` was na de netwerkwissel gestopt
(`docker ps -a` toonde `Exited (255)`, vermoedelijk omdat het
onderliggende netwerk-pad even helemaal weg was tijdens de omschakeling
en een proces binnen de container daar niet tegen bestand was - niet
verder onderzocht, wel genoteerd als aandachtspunt). `docker start
turtlebot_99` volstond om hem terug op te starten.

**Rosbridge/statuspagina startten niet automatisch** na `docker start`
(ze hangen aan een `.bashrc`-hook via `status_page_start.sh`, die enkel
afgaat bij een interactieve shell-login in de container, niet bij een
kale container-restart zonder entrypoint-wijziging). Handmatig gestart:
```bash
docker exec turtlebot_99 bash -c "source /opt/ros/humble/setup.bash; bash /usr/local/bin/status_page_start.sh"
```
`ros-humble-rosbridge-server` bleek al geïnstalleerd in de
`raspios-zenoh`-image (eerder al toegevoegd, niet expliciet
gedocumenteerd in `raspios-migration-log.md`).

Resultaat (getest vanaf een laptop op `10.0.9.0/24`):
- `http://10.0.9.10:8080/` -> HTTP 200, `index.html` correct geserveerd.
- Rosbridge-websocket (`ws://10.0.9.10:9090`) -> handshake OK (`101
  Switching Protocols`), en een echte `/system_info`-abonnering leverde
  live data: `hostname: turtlebot09, ip: 10.0.9.10, mac:
  88:A2:9E:2C:EA:4D, cpu_load_1min: 0.18, mem_percent: 8.9`.
- Internet/WAN-uplink: `ping 8.8.8.8` vanuit de container -> ~19ms,
  bevestigt de switch-uplink werkt.

**Niet getest**: de eigenlijke Zenoh-clienttest (`ros2 topic list` vanaf
een externe laptop via `ZENOH_CONFIG_OVERRIDE`) - de gebruikte laptop
had geen lokale ROS2-installatie. De zenoh-router zelf draait wel
(proces `rmw_zenohd` bevestigd actief in de container, `network_mode:
host` zou dit op `10.0.9.10:7447` moeten blootstellen) - enkel de
effectieve externe-clientverbinding is nog niet end-to-end bevestigd op
dit nieuwe netwerk.

**Nog open voor de fleet-uitrol:**
- Robot-services (zenoh-router, camera, rosbridge/statuspagina) moeten
  robuust opstarten na een reboot/netwerkwissel zonder handmatige
  shell-login - huidige `.bashrc`-hook-aanpak is daar niet voor gemaakt.
  Overwegen: een systemd-unit of een entrypoint-aanpassing die deze
  scripts bij container-start uitvoert i.p.v. bij shell-login.
- Polkit/NetworkManager-rechten voor de `turtlebot`-user (zie hierboven).
- Bevestigen of elke AP uit de doos al in router-modus start zodra WAN
  aangesloten is (gezien bij deze unit), of dat dit toeval/al een vorige
  configuratie was.
