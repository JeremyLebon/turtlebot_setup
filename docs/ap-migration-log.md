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

## Statuspagina-vervolg: layout, browserterminal, launch control (2026-10-03)

Alles hieronder live getest op turtlebot09 via `docker cp` (snelle
iteratie, zie eerder), en gecommit op `raspios-migration` in
`turtlebot_docker` (incl. Dockerfile zodat een volgende image-rebuild
dit meeneemt).

- **Layout-balans gefixt**: camera/teleop-kolommen waren 1.6fr/1fr,
  camera leek te dominant tegenover de compacte teleop-kaart -> nu 50/50,
  D-pad-knoppen vergroot (60px -> 84px) zodat de teleop-kaart zijn helft
  opvult.
- **Browserterminal toegevoegd** (`ttyd`, poort 7681, basic-auth
  `turtlebot`/`TurtleBot@P<nr>` - zelfde patroon als de AP-wifi-
  wachtwoorden, 1 wachtwoord per robot i.p.v. 2). Link op de statuspagina
  ("Terminal ->"). Bedoeld voor les 2+: les 1 blijft een echte terminal
  gebruiken om te leren, dit is gemak voor nadien.
  - **Bug gevonden en gefixt**: een fout/onbestaand commando intikken in
    de browserterminal deed de hele sessie telkens reconnecten. Root
    cause: `/ros_entrypoint.sh` (standaard ROS-image-entrypoint, bevat
    `set -e`) werd in `.bashrc` **gesourced** i.p.v. enkel als
    entrypoint gebruikt - dat lekte `errexit` in elke interactieve shell,
    waardoor een "command not found" (exit 127) de hele shell deed
    afsluiten. Opgelost door die regel uit `.bashrc` te verwijderen
    (`install/setup.bash`, die er al apart in staat, sourcet via
    colcon's underlay-chain toch al `/opt/ros/humble/setup.bash` -
    niets verloren). Gereproduceerd/bevestigd via een rauwe
    `pty.fork()`-test buiten ttyd om (dus geen ttyd-specifieke bug).
- **Launch control toegevoegd**: `launch_control_node.py` (rclpy) stelt
  vaste `std_srvs/Trigger`-services bloot (`/launch/bringup`,
  `/launch/slam`, `/launch/navigation`, `/launch/stop_all`) - enkel
  voorgedefinieerde `ros2 launch`-commando's, geen vrije shell-toegang.
  Knoppen staan op `system.html` (niet de hoofdpagina, om die niet
  nog drukker te maken). `navigation` vereist `NAV_MAP_YAML` (env var)
  naar een bestaande kaart, anders duidelijke foutmelding i.p.v. een
  crash. Live getest via een echte rosbridge-service-call: bringup
  startte alle nodes correct, dubbele start wordt geweigerd ("draait
  al"), en `stop_all` stuurde SIGINT en alles sloot netjes af (geen
  achterblijvende processen).

**Beide hierboven opgeperde todo's zijn gebouwd en getest (2026-10-03):**
- **Netwerkload**: `system_info_node.py` publiceert nu `net_rx_kbps`/
  `net_tx_kbps` (delta over `/proc/net/dev` op `wlan0`, elke 2s, zelfde
  patroon als de bestaande per-core CPU-delta-berekening). Getoond op
  `system.html` naast Geheugen. Bevestigd met echte waarden
  (`rx: 2.4 kbps, tx: 5.4 kbps` tijdens idle).
- **Status-indicatoren bij de launch-knoppen**: `launch_control_node.py`
  publiceert elke seconde `/launch_status` (JSON: welke van
  bringup/slam/navigation een levend proces heeft). Groene stip op de
  knop zodra actief. Bevestigd end-to-end: status ging live van
  `false` naar `true` bij het starten van bringup, en terug naar
  `false` na `stop_all` - in stap met de effectieve proces-staat.

Geen Dockerfile-wijziging nodig voor deze twee - `system_info_node.py`,
`launch_control_node.py` en `status_page/` worden al in hun geheel
gekopieerd door bestaande `COPY`-instructies, dus een volgende
image-rebuild neemt dit automatisch mee.

## Launch-status-bug + actieve-nodes-lijst (2026-10-03)

Jeremy meldde: bringup gestart en kon rijden, maar de status-dot op
`system.html` bleef "gestopt" tonen. Oorzaak: de status hield enkel bij
wat de knoppen zélf gestart hadden (een intern Popen-lijstje in
`launch_control_node.py`) - een robot die via de terminal (les 1-stijl)
of in een vorige node-instantie gestart was, kwam daar niet in voor.

**Fix**: status + de "draait al"-check gebruiken nu `pgrep` tegen de
effectieve commandoregel per launch (bringup/slam/navigation delen
`navigation2.launch.py`, onderscheiden via `slam:=True` vs `map:=`),
i.p.v. zelf-gerapporteerde bookkeeping. `stop_all` stuurt nu ook signalen
naar alles wat `pgrep` vindt, niet enkel wat het zelf startte.

**Erbij**: `/active_nodes` (volledige `ros2 node list`, via
`get_node_names_and_namespaces()`, elke 2s) - nieuwe kaart op
`system.html` met alle actieve ROS2-nodes, ongeacht hoe gestart. Dit was
een expliciete vraag van Jeremy ("zicht op wat draait van packages"),
en lost tegelijk hetzelfde onderliggende probleem op maar dan algemeen
i.p.v. enkel voor de 3 launch-knoppen.

Getest op turtlebot09: bringup manueel gestart via een losse
`ros2 launch`-commando (niet via de knop) -> `/launch_status` toonde
meteen correct `bringup: true`. `stop_all` ruimde dat nadien samen met
een vergeten SLAM-sessie van eerdere tests netjes op (bevestigd via
`ros2 node list`, terug naar enkel de permanente services).

## Losse stop-knoppen + kaart tonen/opslaan (2026-10-03)

Drie vragen van Jeremy in één keer: (1) launches ook apart kunnen
stoppen, niet enkel allemaal samen, (2) een kaart kunnen opslaan, (3)
een kaart kunnen zien op de pagina.

- **Apart stoppen**: `/launch/stop_bringup`, `/launch/stop_slam`,
  `/launch/stop_navigation` toegevoegd naast `/launch/stop_all` -
  dezelfde `pgrep`-aanpak, enkel het proces van die ene launch krijgt
  SIGINT. Getest: SLAM apart gestopt terwijl bringup bleef draaien
  (bevestigd via `ros2 node list`).
- **Kaart tonen**: nieuwe kaart "Kaart (/map)" op `system.html` -
  abonneert op `/map` (`nav_msgs/OccupancyGrid`) en tekent die
  rechtstreeks op een canvas (grijswaarden: onbekend=grijs, vrij=wit,
  bezet=zwart, verticaal gespiegeld om de bottom-left-origin van de
  grid te matchen met canvas' top-left). Getest: live 87x106-grid
  (0.05m/cel) kwam binnen tijdens een SLAM-sessie.
- **Kaart opslaan**: knop roept nav2's eigen `/map_saver/save_map`
  (`nav2_msgs/srv/SaveMap`) rechtstreeks aan via rosbridge vanuit de
  browser - geen nieuwe backend-code nodig, `map_saver` draait al mee
  in de SLAM/navigation-launch. Pad: `/root/turtlebot3_ws/maps/map`
  (zelfde als de `NAV_MAP_YAML`-fallback in `launch_control_node.py`).
  Getest: `map.pgm` + `map.yaml` effectief op schijf bevestigd.
- **Dockerfile aangepast**: `RUN mkdir -p /root/turtlebot3_ws/maps`
  toegevoegd - `map_saver` maakt de map niet zelf aan als die ontbreekt.

**Nieuwe todo (geopperd door Jeremy, nog niet gebouwd):** een pad/
waypoint uitzetten via de webpagina (klikken op de kaart om een
doelpositie of route te geven aan Nav2, zoals rviz2's "set goal pose"),
i.p.v. enkel de kaart passief tonen. Zou gebruik maken van Nav2's
`navigate_to_pose`-actie of `/goal_pose`-topic, met de klik-coördinaten
op het canvas omgerekend naar map-coördinaten via `msg.info.resolution`/
`msg.info.origin`.

Sessie gestopt op 2026-10-03 - volgende sessie: deze todo, en/of verder
met de AP-uitrol voor turtlebot01-08.

## Services automatisch starten bij container-start (2026-10-04)

Opgelost: de open follow-up "robot-services moeten robuust opstarten na
een reboot/netwerkwissel" (zie "Nog open voor de fleet-uitrol" hierboven).

**Probleem**: alle achtergrondservices (zenoh-router, camera,
rosbridge/statuspagina/system_info, ttyd, launch control) werden enkel
via `/root/.bashrc` gestart, dus pas bij een interactieve shell in de
container. Daarnaast had geen enkele `docker-compose.yaml` een
restart-policy: na een reboot van de Pi bleef de container gewoon
`Exited`. Vandaag zo aangetroffen na een reboot (`turtlebot_99 Exited (255)`).

**Fix** (`turtlebot_docker` + `turtlebot_setup`, branch `raspios-migration`):
- Nieuw `docker/services_start.sh` als `ENTRYPOINT` van de image: sourcet
  ROS + workspace, roept de vijf `*_start.sh`-scripts aan (zenoh eerst),
  daarna `exec "$@"` (`CMD ["bash"]`). De vijf `.bashrc`-regels zijn uit
  de Dockerfile verwijderd. De scripts zijn idempotent (`pgrep`-check).
- `restart: unless-stopped` in beide `docker-compose.yaml`'s.
- Bug onderweg gevonden: `TURTLEBOT_NR` werd niet aan de container
  doorgegeven, waardoor het ttyd-wachtwoord terugviel op `TurtleBot@P00`.
  Nu als env-variabele toegevoegd in `turtlebot_setup/docker-compose.yaml`.

**Getest op turtlebot09** (image `55e13c894c8c`):
- `docker compose up -d`: alle 7 processen draaien zonder login, poorten
  8080 (200), 9090 (400 = websocket verwacht) en 7681 (401 = auth) OK
  vanaf de laptop.
- `sudo reboot`: container en alle services kwamen zelf terug binnen
  ~30s na boot, zelfde poortresultaten.

**Gotchas bij het bouwen:**
- De `rpi5`-buildx-builder verwees nog naar het oude IP
  (`192.168.60.249`); opnieuw aangemaakt op `ssh://turtlebot@10.0.9.10`
  met dezelfde naam, zodat de bestaande `buildx_buildkit_rpi50`-container
  hergebruikt werd.
- `--load` met een remote builder laadt de image in de Docker van de
  **client** (laptop), niet in die van de robot. Overgezet met
  `docker save | ssh ... docker load` (~12 min over de AP).
- SD-kaart turtlebot09 is 32 GB (`SD32G`); een eerste build faalde op
  "No space left on device". Oude images opgeruimd (2 dangling
  `raspios-zenoh`-builds + `:raspios`). Bouwen op de robot zelf blijft
  krap: oude image + nieuwe image + buildkit-cache passen er nauwelijks
  naast elkaar.

**Nog te doen**: `.env` op turtlebot09 staat nog op `TURTLEBOT_NR=99`
(ttyd-wachtwoord dus `TurtleBot@P99`), gelijkzetten naar 09.
