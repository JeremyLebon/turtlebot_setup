# Migratie: gedeeld wifi -> per-robot access point (TP-Link TL-WR902AC)

Doel: elke turtlebot krijgt een eigen, geïsoleerd wifi-subnet via een eigen
TP-Link TL-WR902AC (travel-router, AC750, 1x ethernetpoort, geen VLAN-
ondersteuning), i.p.v. alle 9 robots + alle studenten-laptops op één
gedeeld `Wifi_turtlebots`-netwerk. Dit is de fix voor het congestie-/
jitter-probleem van vorig jaar, en recent nog bevestigd tijdens de
Zenoh-WSL-test (ping-jitter 4-226ms op het gedeelde net, geen bandbreedte-
of Zenoh-probleem - zie `raspios-migration-log.md`, sectie "WSL-test +
netwerkdiagnose").

**Status:** de 9 TP-Link TL-WR902AC's + een switch zijn binnen (2026-10-03).
Eerste unit (turtlebot09) is geconfigureerd en getest, zie tabel onder
"Netwerkplan" en de kolom "Status". Overige 8 nog te doen. Uitvoerings-
details komen in een apart `ap-migration-log.md` (zelfde patroon als
`raspios-migration-log.md`), dit document blijft het generieke plan.

Deze migratie staat los van de RaspiOS-/Zenoh-migratie (`raspios-migration`-
branch) - werkt even goed op de huidige Ubuntu-fleet. Zenoh wordt er wel
relevanter door: zonder gedeeld multicast-net heeft elke robot sowieso een
vaste router-endpoint nodig voor de client-connectie vanaf een laptop (zie
`zenoh-migration.md`).

## Waarom router-modus, niet AP-modus

De TL-WR902AC kent geen VLAN's. In **AP-modus** hangt de wifi-radio aan
dezelfde bridge als de ethernetpoort -> alle 9 units zouden gewoon één
plat, gedeeld netwerk vormen (het probleem van vorig jaar, maar dan met
extra hardware ertussen - geen winst).

In **router-modus** doet elke unit NAT tussen WAN (ethernetpoort) en LAN
(wifi-radio): de wifi-kant is een eigen, geïsoleerd subnet per unit, en de
units zien elkaar enkel nog via de gedeelde switch op WAN-niveau (gewoon
voor internet-uplink, niet voor robot-naar-robot-verkeer). Dit is de
aanpak die we gebruiken.

**Consequentie:** de robot heeft geen eigen RPi5-hotspot meer nodig (zoals
in een vroegere testopzet, zie de `10.42.0.1`-voorbeelden in
`zenoh-migration.md` - dat was de default-gateway van een nmcli-hotspot
*op de robot zelf*). Nu is de robot gewoon een gewone wifi-**client** van
zijn eigen AP, net als de studenten-laptop.

## Netwerkplan

SSID- en wachtwoordpatroon vastgelegd op basis van de effectieve
configuratie van turtlebot09 (eerste unit, uitgevoerd op 2026-10-03):
SSID `TB-AP-<nr>`, wachtwoord `TurtleBot@P<nr>` (per robot verschillend,
geen gedeeld wachtwoord - zie toelichting onder de tabel). Robot-MAC's uit
`turtlebot_config.csv`.

| Robot | MAC | AP LAN-subnet | Gateway | Robot-IP (DHCP-reservatie) | SSID | Wachtwoord | Kanaal 5GHz | Kanaal 2.4GHz | Status |
|---|---|---|---|---|---|---|---|---|---|
| turtlebot01 | 88:A2:9E:2C:D6:D6 | 10.0.1.0/24 | 10.0.1.1 | 10.0.1.10 | `TB-AP-01` | `TurtleBot@P01` | 36 | 1 | open |
| turtlebot02 | 88:A2:9E:2C:D5:70 | 10.0.2.0/24 | 10.0.2.1 | 10.0.2.10 | `TB-AP-02` | `TurtleBot@P02` | 40 | 6 | open |
| turtlebot03 | 2C:CF:67:75:70:6F | 10.0.3.0/24 | 10.0.3.1 | 10.0.3.10 | `TB-AP-03` | `TurtleBot@P03` | 44 | 11 | open |
| turtlebot04 | 88:A2:9E:2C:ED:33 | 10.0.4.0/24 | 10.0.4.1 | 10.0.4.10 | `TB-AP-04` | `TurtleBot@P04` | 48 | 1 | open |
| turtlebot05 | 88:A2:9E:2C:D3:8A | 10.0.5.0/24 | 10.0.5.1 | 10.0.5.10 | `TB-AP-05` | `TurtleBot@P05` | 36 | 6 | **gedaan** (2026-10-08, golden V0.1.0.2) |
| turtlebot06 | 88:A2:9E:2C:D8:25 | 10.0.6.0/24 | 10.0.6.1 | 10.0.6.10 | `TB-AP-06` | `TurtleBot@P06` | 40 | 11 | **gedaan** (2026-10-08, golden V0.1.0.2) |
| turtlebot07 | 88:A2:9E:2C:D5:07 | 10.0.7.0/24 | 10.0.7.1 | 10.0.7.10 | `TB-AP-07` | `TurtleBot@P07` | 44 | 1 | **gedaan** (2026-10-08, golden V0.1.0.2) |
| turtlebot08 | 88:A2:9E:2C:D6:67 | 10.0.8.0/24 | 10.0.8.1 | 10.0.8.10 | `TB-AP-08` | `TurtleBot@P08` | 48 | 6 | open |
| turtlebot09 | 88:A2:9E:2C:EA:4D | 10.0.9.0/24 | 10.0.9.1 | 10.0.9.10 | `TB-AP-09` | `TurtleBot@P09` | 36 | 11 | **gedaan** (2026-10-03, jitter 1.4ms mdev, was ~55ms) |

Nummering volgt gewoon `turtlebot_config.csv` (kolom `nr`), zodat SSID,
wachtwoord en subnet meteen herkenbaar zijn. DHCP-range per unit:
`10.0.<nr>.100` t/m `10.0.<nr>.200` (robot zelf krijgt een vaste
reservatie op `.10`, buiten die range).

- **5GHz als primaire band**: meer niet-overlappende kanalen beschikbaar
  dan op 2.4GHz (3 bruikbare: 1/6/11), en de units staan in de les
  fysiek dicht bij elkaar op de werktafels - minder kans op interferentie.
  2.4GHz blijft aan als fallback-band voor het geval een laptop/robot geen
  5GHz heeft (round-robin over 1/6/11, zodat buren nooit hetzelfde
  2.4GHz-kanaal delen).
- **Isolatie komt van de aparte subnets, niet van de kanalen** - de
  kanaaltoewijzing hierboven is puur om radio-interferentie (snelheid) te
  beperken, niet voor beveiliging/scheiding. Pas de volgorde gerust aan
  de effectieve tafelschikking in het lokaal aan (buren = verschillend
  kanaal binnen dezelfde band) i.p.v. blind deze tabel te volgen.
- **DHCP-reservatie aanbevolen** voor het robot-MAC-adres op elke AP (zie
  `turtlebot_config.csv` voor de MAC's), bv. vast op `10.0.<nr>.10` - zodat
  de robot altijd hetzelfde IP heeft voor de Zenoh-client-config en de
  statuspagina-link, i.p.v. af te wachten wat DHCP toekent.
- **Wachtwoord per robot** (`TurtleBot@P<nr>`), niet gedeeld: zo weet een
  groepje studenten enkel het wachtwoord van hun eigen robot, i.p.v. van
  heel de fleet. Isolatie zit toch al in de aparte subnets/NAT, maar dit
  geeft een extra drempel tegen per ongeluk (of bewust) op een andere
  robot inloggen. Eenvoudig patroon (robotnummer in het wachtwoord) houdt
  het toch nog overzichtelijk om aan 9 groepjes te communiceren.

## Robot bereiken: hostname of IP

Elke robot is binnen zijn eigen AP-netwerk op twee manieren bereikbaar:

- **Hostname via mDNS**: `turtlebot<XX>.local` (bv. `turtlebot09.local`).
  `avahi-daemon` draait op de robot (ingesteld door `setup_turtlebot.sh`).
  Getest op turtlebot09 (2026-10-04): `turtlebot09.local` -> `10.0.9.10`,
  statuspagina bereikbaar via `http://turtlebot09.local:8080`.
- **Vast IP**: robot N zit altijd op `10.0.N.10` (DHCP-reservatie, zie
  tabel hierboven).

**Afspraak - wat gebruik je waar:**

| Gebruik | Adres | Voorbeeld |
|---|---|---|
| Statuspagina in de browser (Windows) | hostname | `http://turtlebot09.local:8080` |
| Browserterminal | hostname | `http://turtlebot09.local:7681` |
| SSH | hostname | `ssh turtlebot@turtlebot09.local` |
| Zenoh/ROS2-client in WSL | **vast IP** | `tcp/10.0.9.10:7447` |

**Beperkingen van de hostname:**
- Enkel met het `.local`-suffix - gewoon `turtlebot09` resolvet niet (de
  TP-Link-router publiceert DHCP-hostnames niet via DNS).
- Enkel binnen het eigen AP-netwerk (mDNS = multicast op het lokale
  segment) - niet vanaf de WAN-/campuskant. Past bij de opzet: studenten
  zitten op de wifi van hun eigen robot.
- **WSL2 in de standaard NAT-netwerkmodus resolvet `.local` meestal
  niet** - daarom het vaste IP voor de Zenoh-config in WSL. Alternatief
  (nog niet getest): WSL in *mirrored networking mode*
  (`networkingMode=mirrored` in `.wslconfig`). Nog te testen op een
  studentenlaptop.

## WAN-kant (switch-uplink)

Alle 9 ethernetpoorten -> gedeelde switch -> 1 uplink naar het
campusnetwerk (enkel voor internet: `apt`, `docker pull`/`push`, niet voor
robot-naar-robot of robot-naar-laptop-verkeer - dat loopt via de wifi-kant
van elke AP). WAN-verbindingstype op elke unit: **Dynamic IP** (DHCP vanaf
het campusnetwerk), te bevestigen bij de netwerkbeheerder of het
campus-DHCP genoeg leases/een apart VLAN voor dit poortensegment aankan
voor 9+ apparaten.

Labels op elke unit + ethernetkabel (bv. `AP-01` t/m `AP-09`) zodat een
kapotte/verwisselde kabel niet tot verwarring leidt over welke AP bij
welke robot hoort.

## Configuratieprocedure (per unit, herhalen x9)

Elke unit moet je via zijn eigen (tijdelijke) wifi configureren - eenmaal
in router-modus is er geen apart LAN-ethernetpoortje meer om op aan te
sluiten (de ene poort wordt dan WAN).

1. **Fabrieksreset** (indien niet nieuw/al eens gebruikt): pinhole-knop
   ~10s ingedrukt houden.
2. **Verbinden met de unit** via zijn eigen out-of-the-box SSID (sticker
   onderaan het toestel), browsen naar `tplinkwifi.net` of `192.168.0.1`.
3. **Quick setup wizard -> Router-modus** (niet Range Extender/AP-modus)
   kiezen.
4. **WAN**: verbindingstype "Dynamic IP" (of volgens campus-netwerkbeheer).
5. **Wireless settings**: SSID + wachtwoord instellen volgens de tabel
   hierboven (eerst 5GHz-radio, dan 2.4GHz-radio apart - dit zijn twee
   losse secties in de admin-UI). Band steering/"Smart Connect" **uit**
   zetten als die optie bestaat - we willen net voorspelbaar welke band/
   kanaal gebruikt wordt, niet dat het apparaat zelf kiest.
6. **LAN-instellingen**: LAN-IP wijzigen naar de gateway uit de tabel (bv.
   `10.0.1.1` voor turtlebot01), DHCP-range aanpassen naar de tabelwaarde.
   **Let op**: na deze stap verbreekt de admin-sessie (je IP in dat
   subnet verandert) - opnieuw verbinden met de nieuwe SSID om verder te
   gaan.
7. **DHCP-reservatie** toevoegen voor het robot-MAC-adres (zie
   `turtlebot_config.csv`) -> vast IP zoals hierboven beschreven.
8. Unit + kabel labelen, aansluiten op de switch.

## Testen (per unit)

1. Robot (RPi5) verbinden met de nieuwe SSID i.p.v. het oude gedeelde
   `Wifi_turtlebots`-net (`nmcli` of raspi-config netwerkinstellingen).
   Controleren dat de robot het verwachte vaste IP krijgt
   (`ip -4 addr show wlan0`).
2. Een laptop verbinden met dezelfde SSID, en vanaf daar:
   ```bash
   ping 10.0.<nr>.10         # robot bereikbaar?
   ping -c 20 10.0.<nr>.10   # jitter-check, vergelijk met de oude ~55ms mdev
   ```
3. Zenoh-client-test vanaf de laptop (zie `zenoh-migration.md` voor de
   volledige uitleg):
   ```bash
   export RMW_IMPLEMENTATION=rmw_zenoh_cpp
   export ZENOH_CONFIG_OVERRIDE='mode="client";connect/endpoints=["tcp/10.0.<nr>.10:7447"]'
   ros2 topic list
   ```
4. Statuspagina (`turtlebot_docker`, poort 8080) openen vanaf de laptop op
   `http://10.0.<nr>.10:8080` - bevestigt zowel netwerk als de
   rosbridge-service.
5. Internetconnectiviteit op de robot zelf controleren (via de WAN-kant):
   `docker compose pull`/`ping 8.8.8.8` vanop de robot.

Pas na deze 5 stappen op **1 unit** overgaan naar de volgende - niet alle
9 blind na elkaar configureren zonder tussentijds te testen (zelfde
aanpak als bij de RaspiOS-/Zenoh-migratie: eerst 1 testen, dan pas
uitrollen).

## Nog open / te beslissen

- Campus-netwerkbeheerder bevestigen dat het WAN-segment (9 apparaten op
  1 switch-uplink) geen probleem is (DHCP-leases, eventueel apart VLAN).
- Fysieke tafelschikking in het lokaal nog niet gekend op moment van
  schrijven - kanaaltoewijzing in de tabel hierboven is een eerste
  voorstel, aanpassen zodra de opstelling vastligt.
- `setup_turtlebot.sh`/`turtlebot_config.csv` hoeven voor deze migratie op
  zich niet aangepast (die regelen ROS_DOMAIN_ID/LIDAR/camera, niet het
  wifi-netwerk) - robot verbindt gewoon met een andere SSID, verder
  ongewijzigd.
