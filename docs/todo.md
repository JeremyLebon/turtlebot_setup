# Todo / featurelijst - RaspiOS + Zenoh + per-robot AP migratie

Centrale lijst van open punten (branch `raspios-migration`). Details en
achtergrond staan in de migratielogs (`raspios-migration-log.md`,
`ap-migration-log.md`); deze lijst verwijst ernaar i.p.v. alles te
herhalen. Laatst bijgewerkt: 2026-10-09.

## Voor de fleet-uitrol

- [x] **Polkit/NetworkManager-rechten** voor de `turtlebot`-user, zodat
      `nmcli device wifi connect` geen `sudo` meer vraagt (zie
      `ap-migration-log.md`, gotchas turtlebot09).
      **2026-10-07**: `polkit/50-turtlebot-networkmanager.rules` (groep
      `netdev`), op turtlebot09 geinstalleerd: `nmcli` zonder sudo OK over SSH.
- [ ] **AP router-modus uit de doos bevestigen**: start elke TL-WR902AC
      automatisch in router-modus zodra WAN aangesloten is, of was dat bij
      turtlebot09 toeval?
- [ ] **Image-grootte onderzoeken**: `raspios-zenoh` is gegroeid van
      5,17 GB naar 7,64 GB. Uitzoeken met `docker history` (apt-cache,
      libcamera/colcon build-artefacten in lagen?). Relevant voor 8 robots
      die over wifi pullen op SD-kaarten van 32 GB.
- [x] **Image herbouwen + pushen** (2026-10-06, digest
      `sha256:74c5692b...`, turtlebot09 draait erop; herstart-test OK:
      alle services binnen ~1 min terug) met de wifi-signaalweergave
      (2026-10-04, nu enkel via `docker cp` live in `turtlebot_9` - verdwijnt
      bij het opnieuw aanmaken van de container). Idem voor de no-cache-
      webserver (`status_page_server.py`, i.p.v. `python3 -m http.server`).
      Let op: na `docker cp` het execute-bit controleren - op 2026-10-06
      startte de statuspagina niet na een reboot omdat
      `status_page_start.sh` via `docker cp` als 644 binnenkwam
      (`Permission denied`). Scripts staan nu als 755 in git
      (turtlebot_docker `4c33649`).
- [x] **Wifi-vakje op smartphone nakijken** na de no-cache-fix
      (2026-10-06: OK op smartphone en laptop).
- [ ] **Bij elke wijziging aan `common.js`** het versienummer in de
      `<script src="common.js?v=N">`-tags ophogen (index.html + system.html).
- [x] **Buildkit-cache NIET meer opruimen** op turtlebot09 (afspraak
      2026-10-06): opruimen maakte van een build van ~3 min een volledige
      rebuild + push van ~20 min. Plaats vrijmaken via oude images
      (`docker image prune`), niet via `docker buildx prune`.
- [x] **Hostname in `/etc/hosts`** op de robot: `sudo` meldt
      `kan computernaam turtlebot09 niet herleiden` (en wacht telkens op een
      DNS-timeout). Oorzaak: hostname is `turtlebot09`, maar `/etc/hosts`
      bevat nog `127.0.1.1 raspberrypi` (hostname gewijzigd zonder hosts bij
      te werken). Fix in de setup: die regel vervangen door
      `127.0.1.1 turtlebot<nr>` (of `raspi-config`/`hostnamectl` + hosts).
      **2026-10-07**: op turtlebot09 met de hand gefixt (backup
      `/etc/hosts.bak`), sudo nu direct. Moet nog in `setup_turtlebot.sh`
      (zie uitrolmethode).

- [x] **Uitschakel-knop nakijken**: op 2026-10-06 voor het eerst gebruikt
      (Jeremy sloot turtlebot09 zo af). Bij de volgende opstart controleren
      dat het een nette shutdown was (`journalctl -b -1 | tail`, geen
      fsck/dirty-meldingen) en of het uit-melodietje klonk.
      **2026-10-07**: boot erna schoon (geen `recovering journal`, enkel een
      normale `orphan cleanup`). Vorige-boot-log niet te bekijken: geen
      persistente journal (`/var/log/journal` bestaat niet). Melodie niet
      nagevraagd.
- [ ] **"error"-melodie testen**: bv. tijdelijk een service laten falen
      (poort 9090 bezet) en nagaan dat na 90 s de error-melodie klinkt.

- [x] **Robot blijft op een ander wifi-netwerk hangen** (opgelost in setup_turtlebot.sh, 2026-10-09) (2026-10-09:
      turtlebot09 niet te vinden op `TB-AP-09` en ook niet op `RobotWifi`).
      NetworkManager gebruikt de prioriteit (100 voor `TB-AP-<nr>`) enkel bij
      het kiezen van een netwerk, en schakelt niet over van een verbonden
      netwerk. Start de robot voor zijn AP (TP-Link start trager op), dan
      neemt hij een ander bekend netwerk of blokkeert hij het profiel ~5 min.
      **Aangepast in `setup_turtlebot.sh`**: `autoconnect-retries 0` op
      `TB-AP-<nr>`, en alle andere wifi-profielen verwijderen - enkel als de
      eigen AP zichtbaar is (anders zit een robot zonder geconfigureerde AP
      nergens meer op). Logica droog getest op de laptop; nog te testen op een
      robot (na "Software bijwerken" of reboot).
      **Getest op turtlebot09 2026-10-09**: oorzaak bevestigd - het met de hand
      aangemaakte `TB-AP-09` had prioriteit 0, gelijk aan `RobotWifi`,
      `RobotWifi 1` en `Wifi_turtlebots`. Na de update: die drie verwijderd,
      `TB-AP-09` prioriteit 100 en retries 0. Gevolg: een robot op een
      ander netwerk zetten kan daarna enkel via scherm/ethernet of door zijn
      AP aan te zetten.

## Uitrol

- [x] **Nieuw `docker-compose.yaml` naar elke robot** (met de mount
      `/run/dbus/system_bus_socket`, nodig voor de aan/uit-knoppen; zonder
      die mount geven ze een foutmelding). Image `raspios-zenoh` van
      2026-10-06 of later.
      **Opgelost 2026-10-08**: compose zit in de clone `~/turtlebot_setup` (golden image) en komt bij elke update mee via `git pull`.
- [ ] **AP + robot configureren voor turtlebot01-08** (tabel in
      `ap-migration.md`, status "open").
- [ ] **Overige 8 robots naar Raspberry Pi OS + Docker** (alles is tot nu
      toe enkel op turtlebot09 gevalideerd).
- [ ] **`raspios-migration` mergen naar `master`** - bewust pas na
      volledige validatie (zie beslissing 2026-10-03).

## Uitrolmethode: SD-kaart klonen (golden image)

Idee (2026-10-06): de SD-kaart van turtlebot09 als image nemen en naar
de andere robots kopieren - Raspberry Pi OS, Docker en de 5,6 GB-image
staan er dan meteen op (geen pull over wifi). Kan, omdat
`setup_turtlebot.sh` (systemd `turtlebot-setup.service`, bij elke boot)
de robot herkent aan het **MAC-adres** via `turtlebot_config.csv`. Maar
dat script dekt nu niet alles wat per robot verschilt:

- [x] **Hoe komt `docker-compose.yaml` op een robot?** Nu met de hand
      (`scp` naar `~/turtlebot_setup_test`). Kiezen: meekomen in de
      golden image, `git pull` van een clone van `turtlebot_setup` op de
      robot, of door `setup_turtlebot.sh` laten kopieren.
      **Gekozen 2026-10-07**: clone van `turtlebot_setup` in
      `~/turtlebot_setup` (zit mee in de golden image, updates via `git pull`).
      turtlebot09 draait nu vanuit die map (`~/turtlebot_setup_test` mag weg).
- [x] **`setup_turtlebot.sh` bijwerken voor Raspberry Pi OS**:
  - pad `CONFIG_FILE` wijst nog naar `/home/turtlebot-rpi5/...` (oude
    user; nu `turtlebot`).
  - schrijft enkel `/etc/profile.d/turtlebot_config.sh` (en met `>>`:
    groeit bij elke boot). Docker Compose leest die niet bij een
    automatische herstart -> **`.env` naast `docker-compose.yaml`
    schrijven** (`TURTLEBOT_NR`, `ROS_DOMAIN_ID`, `LDS_MODEL`,
    `ENABLE_CAMERA`), overschrijven i.p.v. toevoegen.
  - **`/etc/hosts`** mee aanpassen (`127.0.1.1 turtlebot<nr>`, zie
    hostname-punt hierboven).
  - na een wijziging van `.env` de container opnieuw aanmaken
    (`docker compose up -d`), anders blijft de geklonede `turtlebot_9`
    draaien met nr 9.
      **2026-10-07** gedaan (turtlebot_setup `7c7ddc8`), op turtlebot09
      getest: container verhuisd naar de nieuwe map, tweede run doet niets.
- [x] **Wifi per robot**: de kloon bevat het NetworkManager-profiel van
      `TB-AP-09`. Elke robot moet naar zijn eigen AP (`TB-AP-<nr>`,
      wachtwoord `TurtleBot@P<nr>`, zie `ap-migration.md`) - door het
      setup-script laten aanmaken op basis van het nr (oude profiel weg).
      **2026-10-07** in `setup_turtlebot.sh`. Nog te testen op een kloon
      (turtlebot06).
- [x] **Unieke identiteit na het klonen**: `/etc/machine-id` en de SSH-
      host-keys zijn anders identiek op alle robots (DHCP-client-ID,
      "host key changed"-waarschuwingen). Eenmalig bij de eerste boot
      van een kloon opnieuw genereren.
      **2026-10-07** in `setup_turtlebot.sh` (marker per MAC, daarna reboot).
      Nog te testen op een kloon (turtlebot06).
- [x] **Golden image opkuisen voor het klonen**: container `turtlebot_9`
      en de `buildx_buildkit_rpi50`-builder + cache verwijderen (enkel
      nodig op de bouwrobot), `/tmp`-logs, bash-history, testkaarten.
      **Opgelost 2026-10-08**: `tools/golden_prepare.sh` + `setup_turtlebot.sh` (buildkit, container, journal, state op de kloon).
- [x] **Image verkleinen**: turtlebot09 heeft een kaart van 32 GB - het
      image eerst inkrimpen (bv. PiShrink) zodat het ook op een iets
      kleinere 32 GB-kaart past en sneller schrijft.
      **Opgelost 2026-10-08**: PiShrink (in `debian:trixie`) via `sdclone.sh read`, 30 -> 21 GB.
- [ ] **Alternatief afwegen**: verse Raspberry Pi OS via Raspberry Pi
      Imager (hostname/wifi/user per kaart ingesteld) + setup-script +
      `docker compose pull` via de ethernet-switch. Trager per robot, maar
      geen kloon-valkuilen.

- [x] **Voorbereiding golden image** (2026-10-07): setup-script draait uit
      de clone (`git pull` werkt alles bij, ook units/polkit), buildkit wordt
      verwijderd op elke robot behalve 09, persistente journal (max 100 MB),
      `apt full-upgrade` op turtlebot09 (Docker 29.8.2, kernel ongewijzigd).
- [x] **Kloontest op turtlebot06** (2026-10-08): golden image van 09
      (`~/turtlebot_clone/sdclone.sh` op de laptop, PiShrink in een
      `debian:trixie`-container want de e2fsck van Ubuntu 22.04 kent
      `orphan_file` niet; 30 -> 21 GB). Eerste boot op 06 volledig automatisch:
      nieuwe machine-id + SSH-keys, partitie vergroot (128 GB-kaart),
      hostname/hosts, wifi `TB-AP-06`, `.env` nr 6, `turtlebot_9` en
      buildkit weg, `turtlebot_6` + alle services up met piep. Drie kleine
      fixes daarna (keys na hostname, gekloonde journal, buildkit-image).
      Let op: de golden image zelf heeft die fixes nog niet - na het klonen
      eenmaal "Software bijwerken" (git pull + setup), of de image opnieuw
      maken.
- [ ] **Uitrol naar 01-05, 07, 08** met de golden image (AP per robot
      eerst configureren; MAC in `turtlebot_config.csv` nakijken).
      **2026-10-09**: turtlebot05 en 07 getest met golden V0.1.0.2: werken
      perfect (samen met 06 en 09 nu 4 van 9). SD-kaarten voor 01-04 en 08
      zijn geschreven, nog niet getest op de robots.
      Nog te doen op 05 en 07 (staan op school): eenmaal "Software bijwerken"
      (golden V0.1.0.2 mist de fixes van na de kloontest). Idem op 01-04/08
      na hun eerste boot.

## Bugs

- [x] **Nav2 draaide ter plaatse (recoveries) i.p.v. naar het doel** -
      opgelost 2026-10-09 (turtlebot_docker `13d567c`). Oorzaak: elk ROS-proces
      op de robot was een Zenoh-*peer*; de rechtstreekse peer-verbindingen
      lukten niet voor elk paar processen, waardoor `controller_server` de
      `map`->`odom` van AMCL nooit kreeg ("map does not exist"). Fix: image-ENV
      `ZENOH_CONFIG_OVERRIDE` `mode="client"` naar `tcp/127.0.0.1:7447` (alles
      via de router, zoals op de laptops) + Nav2 met `use_composition:=False`.
      **Correctie (later op 2026-10-09):** de echte oorzaak was tf2 0.25.23
      (Humble-sync 2026-09-07): ABBA-deadlock waitForTransform /
      testTransformableRequests (ros2/geometry2#982, #995) - de TF-listener van
      een proces bevriest na enkele seconden, costmap-footprints blijven op een
      oude tijd staan. Image haalt tf2 0.25.24 uit ros2-testing (Dockerfile-laag,
      faalt bij < 0.25.24); `turtlebot_vis` heeft 0.25.22 + bewaking. Client-
      modus blijft (kan geen kwaad). Snelle check bij twijfel:
      `/local_costmap/published_footprint`-stamps moeten actueel zijn.
- [x] **Eerste doel na wissel van planner faalde** - nieuwe BT = nieuwe
      clients, Zenoh-ontdekking > Nav2's 20 ms: `bt_navigator`
      `default_server_timeout` 1000 ms (gegenereerde Nav2-parameters).
- [x] **Doelnauwkeurigheid** - keuze ruim/normaal/precies/eigen per doel
      (nav_web_node zet `general_goal_checker` dynamisch), route-tussenpunten
      ruim; standaard nu 10 cm / 0.15 rad i.p.v. TB3's 25 cm. Getest OK.
- [x] **Kaart soms niet zichtbaar op nav.html** - latched `/map` gemist door
      late pagina: nu ook `map_server`'s GetMap-service. Getest OK.
- [x] **Nav2-processen bleven hangen na Stop** (`controller_server`,
      `planner_server` als wezen) - opgelost 2026-10-09: stoppen = SIGINT,
      SIGTERM, SIGKILL incl. kindprocessen (`CHILD_PATTERNS`).
- [x] **Kaarten verdwenen bij elke update** (stonden in de container) - nu in
      `state/maps` (2026-10-09).

- [x] **`turtlebot_vis`: shell sluit bij elk mislukt commando** (opgelost, turtlebot_vis `f9b9df5`) (bv. een
      typfout -> terug uit `docker exec -it turtlebot-vis bash`). Oorzaak: de
      `.bashrc` deed `source /ros_entrypoint.sh`, en dat script begint met
      `set -e`. In de oude `turtlebot_docker/docker_vis` was dit al omzeild
      (eigen `/ros_entrypoint.sh` met `set +e`), in `turtlebot_vis` niet.
      **Gefixt 2026-10-09** in `turtlebot_vis/docker/Dockerfile` (`.bashrc`
      sourcet nu rechtstreeks `/opt/ros/humble/setup.bash`). Image
      `nobel86/turtlebot-rpi5-vis:zenoh` nog te pushen; studenten moeten
      daarna opnieuw `docker compose pull`. (`docker_vis_on_rpi5` in
      `turtlebot_docker` heeft dezelfde fout, maar wordt niet meer gebruikt.)

- [x] **SLAM-knop geeft geen kaart** - opgelost 2026-10-06 door de knop
      naar **Cartographer** om te zetten (turtlebot_docker
      `cartographer_headless.launch.py`, zoals de TurtleBot3 ROS2 e-manual,
      zonder rviz2, met `map_saver` voor de opslaan-knop). Oorzaak was geen
      hang (gdb: alle threads idle) maar slam_toolbox die elke scan weigert
      waarvan het aantal stralen afwijkt van de eerste (LDS-02: 220/221);
      werd de eerste scan geweigerd, dan bleef de kaart leeg tot de robot
      reed. Getest: 4x starten/stoppen via de services, telkens kaart
      stilstaand, geen achterblijvers, kaart opslaan OK. Nog niet in de
      Docker Hub-image (enkel `docker cp` in `turtlebot_9`).
      Gevolg: kaart maken en navigeren zijn nu gescheiden stappen (mappen
      met teleop -> opslaan -> Navigation met kaart), zoals in de e-manual.
- [ ] **slam_toolbox + LDS-02** (enkel als studenten later zelf
      slam_toolbox gebruiken): `ld08_driver` een vast aantal stralen laten
      publiceren (bv. 360 bins van 1 graad).
- [ ] **Debug-valkuil**: een `ros2 launch` gestart als achtergrondproces
      (`cmd &`) in een niet-interactieve bash negeert SIGINT - stoppen met
      SIGTERM. De launch-knoppen (Popen) hebben dit probleem niet.

## Testen

- [x] **Zenoh-client vanaf een studentenlaptop in WSL** (`ros2 topic list`
      over het AP-netwerk, `ROS_DOMAIN_ID=9` voor turtlebot09).
      **Getest 2026-10-08 door Jeremy: werkt** (turtlebot_vis branch `zenoh`,
      image `nobel86/turtlebot-rpi5-vis:zenoh` van 2026-10-08, rmw_zenoh 0.1.9).
- [ ] **WSL mirrored networking mode** testen, zodat `.local`-hostnames
      ook in WSL werken (zie "Robot bereiken: hostname of IP" in
      `ap-migration.md`).
- [ ] **I2C-shield / Grove Base Hat** terug aansluiten na de bordwissel en
      testen.

## Morgen eerst (2026-10-10)
- Image bouwen + op 09 zetten: `79b7222` (routepunten zonder sleep -> rijrichting,
  MPPI GoalAngleCritic 0.25, piep = "on"-melodie, actielog). Mislukte op
  2026-10-09 ~23:00: Docker Hub auth (`POST auth.docker.io/token` 504 met geldige
  login, ook `docker login` met PAT). Lukt het niet: tijdelijk via ghcr.io.
- Daarna: route "test" op buro_groot opnieuw aanklikken (oude punten hebben
  vaste richting 0) en met MPPI testen; recoveries bij punt 1/2 weg?

## Features

- [ ] **Desktop-extra's verwijderen op de vloot / golden image** (op turtlebot09
      gedaan 2026-10-11, +1,3 GB): `apt-get remove --purge chromium chromium-l10n
      chromium-common firefox vlc-l10n rpi-userguide rpd-wallpaper-trixie
      pocketsphinx-en-us python3-mypy` (neemt ook rpi-chromium-mods, thonny, mypy
      mee; geen systeempakketten) + ongebruikte image moby/buildkit:buildx-stable-1.
      turtlebot09 (32 GB-kaart + buildkit-cache ~12 GB, groeit per build) blijft
      krap: grotere SD-kaart of de builder naar een robot met 128 GB.
- [x] **Desktop uit op de hele vloot** (2026-10-10, setup_turtlebot.sh: standaard
      `multi-user.target`, desktop terug per robot met `echo true >
      ~/turtlebot_setup/state/desktop` + herstart). Nog open: desktoppakketten
      verwijderen in een nieuwe golden image? Achtergrond: RaspiOS op de robots is de
      desktopversie: lightdm/labwc draait (~400 MB RAM, 0 % CPU in rust),
      Chromium + Firefox + Vulkan-drivers ~1,5-2 GB op de kaart. turtlebot09 staat
      op `multi-user.target` (geen desktop; terug: `sudo systemctl set-default
      graphical.target && sudo systemctl start lightdm`). Beslissen: ook in
      setup_turtlebot.sh voor de vloot (met schakelaar in state/), en/of de
      desktoppakketten verwijderen in een nieuwe golden image.

- [ ] **Layout-herziening statuspagina** (voorstel 2026-10-10, eerst mockup):
      **Beslist 2026-10-10**: studenten mogen afsluiten/herstarten, NIET bijwerken;
      1 PIN voor de hele vloot; labo-check als icoon met hover + uitklaplijst.
      **Stap 1 (header) gebouwd: v0.6.0** (turtlebot_docker eaefdd1).
      **Stap 2 (Rijden + camera in Navigatie) en stap 3 (Info + Beheer met PIN):
      v0.8.0** (turtlebot_docker 4d6f128). PIN via `fenix_admin.py set` op elke
      robot (nog geen PIN ingesteld - Jeremy kiest). Nog open:
      - [x] PIN voor de hele vloot: knop "Docenten-PIN" in de vlootmonitor
            (enkel de hash naar de robots; robot-image v0.9.0). Getest: hash
            compatibel met fenix_admin.py, monitor zet set_pin in de wachtrij;
            nog niet end-to-end met een echte robot (monitor.conf op 09 niet ingesteld).
      - [x] Navigatie opgeschoond (v0.9.0): icoontjes in de werkbalken, zijpaneel
            "Navigatie" (kaart maken verwezen naar Rijden, bringup-stap weg).
      - [x] Projecten: start/stop-icoontjes (v0.9.0).
      indelen volgens wat de student doet, niet volgens de techniek.
      - Header op elke pagina: tabs, batterij/wifi/temp/internet, update-icoon
        (licht op bij update), aan/uit-menu (afsluiten/herstarten), altijd
        zichtbare rode STOP, chips van lopende launches (met stop per chip).
      - **Rijden** (was Status): camera + teleop + live lidar/kaart samen,
        "Start kaart maken" + "Kaart opslaan" hier; joystick/camera-schakelaar op
        hun eigen kaart.
      - **Navigatie**: camerabeeld als klein venster in de kaart (aan/uit);
        "Geavanceerd" (Nav2) en kaarteditor-herstel naar Beheer.
      - **Projecten**: ongewijzigd.
      - **Info** (was Systeem): alleen-lezen - gezondheid, labo-check, WSL-verbinden,
        nodes, logs.
      - **Beheer** (docenten-PIN, server-side gecontroleerd, state/): bijwerken +
        terugschakelen, robot-config, camera-instellingen, Nav2-instellingen,
        kaart-origineel terugzetten, USB-spaarstand, monitor-toegang.
      - Weg: kaartkaart op Systeem (dubbel, slaat op naar maps/map), "Launch
        control (les 2)".
      - Icoontjes: inline SVG (bv. Lucide, vrije licentie), geen CDN (offline).
      - PIN = drempel tegen ongelukken, geen echte beveiliging (SSH + sudo
        `turtlebot`); echte scheiding = aparte student-gebruiker (zie Gebruikers en rechten).
      - Feedback Jeremy 2026-10-10 (verwerkt in mockup v2): smartphone-layout
        (kaart + camera + teleop, onderste tabbalk), studenten mogen de kaart
        bewerken (origineel terugzetten blijft in Beheer), overal icoontjes met
        hover-tekst, aparte snelheid rechtdoor (m/s) en draaien (rad/s), logo +
        naam, versienummer in de header (vX.Y.Z, hover = image/setup/golden).
      - Naam: werktitel **Fenix** (mockup v3, feniks-logo); definitieve naam nog kiezen.
        Mogelijk later commercieel -> merkcheck nodig (TMview/BOIP, klasse 9 + 42).
        Fenix/Phoenix is zeer gangbaar. Kandidaten 2026-10-10: Alcedo (ijsvogel),
        Navora (verzonnen), Zwin, Reynaert, Kompaan, Fenux (let op: klinkt als
        FANUC, robotica!), Fenyx, Feniqs; Ardea valt af (DLR-drone).
      - **Robot-onafhankelijk**: Jeremy wil de webpagina later ook op zijn andere
        robots gebruiken -> robottype/capabilities uit config (camera, lidar,
        teleop, Nav2 aan/uit per robot), TurtleBot-specifieke delen (OpenCR,
        LDS-02, F710) als modules; op termijn eigen repo.
      - Versienummer: `turtlebot_docker/VERSION` + CHANGELOG.md (sinds 2026-10-10).
      - Te beslissen: afsluiten voor studenten (voorstel: ja, bijwerken nee),
        1 PIN voor de vloot of per robot, labo-check op Rijden (icoon) of op Info.

### Ideeën navigatie (Jeremy, 2026-10-09) - voorgestelde volgorde
1. ~~**Route pauzeren / verder**~~ en 2. ~~**Actie per locatie**~~ gebouwd
   (b0ecbf0, nog te testen met rijden). Ook: doel/route tijdens Verkennen
   pauzeert explore_lite (491a31c).
1. **Route pauzeren / verder** - nav_web houdt de route (index) bij: Pauze =
   huidig doel annuleren, Verder = huidig punt opnieuw sturen. Klein.
2. **Actie per locatie** - per routepunt: wachten N s, piepen, foto (camera
   snapshot -> state/), 360° draaien, AprilTag zoeken. In nav_web (eigen
   routelogica) i.p.v. waypoint_follower-taskplugins; bewaard met de route.
3. **Lage batterij -> naar parkeerplaats** - per kaart een punt "laadplaats"
   (Zones/markers); onder een drempel (bv. 11,4 V, instelbaar) route/doel
   annuleren en daarheen rijden + melding. Geen echt docken (geen laadstation).
4. **Positie (AMCL) automatisch** - laatste positie per kaart bewaren en bij
   Navigatie-start als beginpositie zetten; knop "Robot zoekt zelf" =
   `/reinitialize_global_localization` + traag ronddraaien (werkt slecht in
   symmetrische ruimtes).
5. **Rechte lijnen** - kan nu al: Theta* (any-angle, rechte stukken) + Regulated
   Pure Pursuit. Echte "straight line planner" = eigen C++ plugin (Nav2-tutorial,
   mooi studentproject).
6. **Iets met BT** - BT-keuze per doel (bv. elke seconde herplannen, wachten bij
   obstakel i.p.v. omrijden, andere recovery), actieve BT tonen; studentproject:
   eigen BT-XML uploaden/kiezen op de pagina.

Nieuwe wensen (2026-10-09):

- [ ] **Camera-instellingen (RPi5 CSI) via de webpagina** + goede
      standaardwaarden. `camera_ros` geeft de libcamera-controls als ROS-
      parameters (o.a. `ExposureTime`, `AnalogueGain`, `AeEnable`,
      `Brightness`, `Contrast`, `Saturation`, `Sharpness`, `AwbMode`), naast
      resolutie/fps/`jpeg_quality` uit `camera_params.yaml`. Webpagina: sliders
      -> `set_parameters` via rosbridge, keuze bewaren in `state/` (zoals
      `camera_enabled`) en meegeven bij het starten van `camera_node`. Nagaan
      welke controls live aanpasbaar zijn en welke een herstart vragen.
- [ ] **Camerakalibratie - intrinsiek** (dambordpatroon): `camera_calibration`
      (`cameracalibrator`) op de laptop in `turtlebot_vis` (heeft een GUI,
      werkt via WSLg) tegen `/camera/image_raw`, resultaat naar de robot via
      `camera_ros` (`camera_info_url` / `set_camera_info`) en bewaren in
      `state/`. Alternatief: kalibratiemodus op de webpagina (hogere
      resolutie/fps tijdelijk, beelden vastleggen, kalibratie op de robot).
      Nodig voor o.a. AprilTags. Resultaat (`K`, `D`, `R`, `P`) per robot
      bewaren, want elke cameramodule verschilt; nu staat er geen
      `camera_info_url` in `camera_params.yaml` en publiceert `camera_ros`
      een lege/onbekalibreerde `camera_info`. Per resolutie opnieuw
      kalibreren (640x480 is de standaard).
- [ ] **Camerakalibratie - extrinsiek** (waar zit de camera t.o.v. de robot):
      de burger-URDF (`turtlebot3_burger.urdf`) heeft **geen camera-frame**,
      dus er is geen TF `base_link` -> `camera_link` -> optisch frame, en het
      `frame_id` van de beelden hangt nergens aan. Stappen: (1) statische TF
      met de gemeten positie/hoek van onze CSI-montage (`static_transform_
      publisher` in bringup, of een eigen URDF-uitbreiding), met de juiste
      optische rotatie (z vooruit, x rechts, y omlaag) en `frame_id` gelijk
      zetten in `camera_params.yaml`; (2) waarden per robot bewaren in
      `state/` als de montage verschilt; (3) eventueel nauwkeuriger met een
      AprilTag/dambord op een gekende plek t.o.v. de robot. Nodig om
      detecties (AprilTag, YOLO) op de kaart of in rviz op de juiste plek te
      zetten.
- [x] **Internetverbinding-indicator** - gebouwd 2026-10-09 (turtlebot_docker
      `777077f`/`361b8b2`, nu wereldbol-icoon in de gedeelde kop met details
      bij hoveren; "geen internet" in de update-hint). Oorspronkelijk plan: `system_info_node`
      test om de ~30 s DNS + een TCP-verbinding (bv. `1.1.1.1:443`,
      `github.com`) -> vakje "Internet: ja/nee". Ook gebruiken voor de
      update-knop (zie "Update-knop offline" bij Offline gebruik).
- [x] **Joystick (Logitech F710) aan/uit via de webpagina** - gebouwd en
      getest 2026-10-09 op turtlebot09 (turtlebot_docker `e630352`, image
      `sha256:fb7c98e8…`, setup `8995c87`). Knop + detectie ("Logitech Gamepad
      F710 gedetecteerd") op de teleop-kaart, rij in de labo-check, knoppen op
      `system.html`. `teleop_twist_joy` -> `/cmd_vel_joy` via
      `launch_control_node` (`/launch/joystick`), los van bringup, niet
      onthouden (na herstart uit). Config `docker/joystick_f710.yaml`: LB =
      dodemansknop, linker stick vooruit/achteruit 0,1 m/s, rechter stick
      draaien 1,0 rad/s, RB = turbo (0,22 m/s, 2,0 rad/s). Compose mount nu
      heel `/dev/input` (i.p.v. `js0` onder `devices:`), zodat een later
      ingestoken ontvanger zichtbaar is en de container ook zonder start.
      Getest: rijden, turbo, LB loslaten = stop, joystick wint van webteleop
      (gemeten: webberichten tijdens joystickgebruik niet doorgegeven).
      Nog te testen: ontvanger uittrekken/insteken terwijl de container draait.
- [x] **Prioriteit tussen stuurbronnen met `twist_mux`** - getest op 09 (joystick > web > /cmd_vel) -
      **gebouwd 2026-10-09** (turtlebot_docker `ed4c567`, fork turtlebot3
      `dba8cf8`), lokaal getest in een Humble-container; image nog te bouwen
      en op een robot te testen.
      | Bron | Topic | Prioriteit |
      |---|---|---|
      | Joystick F710 (`teleop_twist_joy`) | `/cmd_vel_joy` | 100 |
      | Webteleop (statuspagina) | `/cmd_vel_web` | 50 |
      | Nav2 (ook via Simple Commander), `teleop_keyboard`, studentencode | `/cmd_vel` | 10 |
      Uitgang `/cmd_vel_out` -> `turtlebot3_node` (remap in
      `turtlebot3_bringup/launch/robot.launch.py` van de fork). Niet
      `/cmd_vel_nav` als Nav2-ingang: dat is in Nav2 Humble al het interne
      topic tussen controller en velocity smoother. `twist_mux` draait altijd
      (`twist_mux_start.sh` vanuit `services_start.sh`) en staat bij de
      diensten op `system.html`. Zonder `twist_mux` rijdt de robot niet.
      Testen op de robot: webteleop rijdt, Nav2-doel rijdt, webteleop tijdens
      Nav2 neemt over en Nav2 gaat daarna verder.
      Webteleop rijdt (Jeremy 2026-10-09). Nog te doen: noodstop via een `lock` (let op: bij een lock stuurt
      `twist_mux` geen nulsnelheid - zelf eerst een stop publiceren),
      **Op turtlebot09 (2026-10-09)**: `twist_mux` draait, met bringup is
      `/cmd_vel_out` 1 pub (twist_mux) / 1 sub (turtlebot3_node) en heeft
      `/cmd_vel` enkel twist_mux als subscriber. Rijtests (webteleop, Nav2,
      overnemen) nog niet gedaan.
      actieve bron tonen op de statuspagina.
- [x] **Masterpagina** - gebouwd 2026-10-09: `monitor/monitor.py` (laptop docent,
      Windows of WSL, zie monitor/README.md), robots pushen via `MONITOR_URL`
      (`monitor.conf` -> .env). Getest met turtlebot09 -> laptop op TB-AP-09.
      Nog te doen: vast IP voor de laptop op het switch-subnet, adres in
      monitor.conf, testen met meerdere robots via de switch.
- [ ] ~~Masterpagina: alle turtlebots in 1 overzicht~~ (oorspronkelijke notitie) (batterij, temperatuur,
      services, versie, wie verbonden is). Let op: met een AP per robot in
      router-modus (NAT) kan een laptop op de switch de robots niet
      rechtstreeks bereiken - daarom is `turtlebot_monitor` (nmap op 1 subnet)
      destijds afgevoerd. Opties: (a) **robots pushen** elke paar seconden een
      klein JSON-statusbericht naar een centrale server op het
      switch-netwerk (HTTP of MQTT; werkt door NAT, robots hebben die server
      als vast adres in de setup), (b) port forwarding 8080/9090 op elke AP
      (9x handwerk; elke pagina blijft rosbridge-verkeer kosten). Voorkeur:
      (a), met links naar de statuspagina per robot. Centrale server: de
      laptop van de docent of een extra Pi aan de switch.
- [x] **Nav2-navigatie op de webpagina** - gebouwd 2026-10-09 (`nav.html` +
      `nav_web_node`, turtlebot_docker `e4874ed`..`d8ff090`), door Jeremy getest:
      robot rijdt naar het doel. Lag eerst aan Zenoh peer-modus (zie Bugs).
      Daarna toegevoegd: planner per doel (NavFn Dijkstra/A*, Smac 2D, Theta*),
      controller per doel (DWB, Regulated Pure Pursuit), kaart kiezen +
      opslaan als, SLAM/Navigatie starten de bringup mee. Alle 4 planners
      plannen een pad van 5,4 m (getest zonder rijden); **rijtests met
      Theta*/Smac en RPP + routes in een lus nog te doen**. Oorspronkelijk plan: kaart tonen (`/map`), robotpositie
      (TF `map`->`base_footprint`), beginpositie zetten (`/initialpose`,
      zoals "2D Pose Estimate" in rviz), doel klikken (`navigate_to_pose`),
      gepland pad (`/plan`) en voortgang/annuleren. De Navigation-knop
      (`navigation2.launch.py` met opgeslagen kaart) bestaat al; dit maakt het
      bruikbaar zonder rviz. Vervangt/omvat het punt "Waypoint/doel zetten"
      hieronder.
- [x] **Traject tekenen op de kaart** - route op `nav.html` (punten
      aanklikken, lus, laatste punt weg/wissen) als reeks `navigate_to_pose`-
      doelen. Nog niet: routes opslaan in `state/`. Oorspronkelijk plan: meerdere punten aanklikken -> route
      (Nav2 `navigate_through_poses` of `follow_waypoints`), routes opslaan
      in `state/` en opnieuw afspelen, eventueel in een lus (patrouille).
      Bouwt verder op de Nav2-webpagina; voorbeelden: `vizanti`, OpenAMRobot
      (zie hieronder).

- [x] **Waypoint/doel zetten via de webpagina** (nav.html: doel, route, lus - getest) (+ robotpositie en het
      geplande Nav2-pad op de kaart tonen): klikken op de kaart ->
      Nav2 `navigate_to_pose` / `/goal_pose`, klik-coordinaten omrekenen
      via `msg.info.resolution`/`msg.info.origin` (zie
      `ap-migration-log.md`).
- [x] **Robot uitschakelen / herstarten vanuit de webpagina** - gebouwd
      2026-10-06 (turtlebot_docker `4e953d5`, turtlebot_setup `0d18e99`):
      kaart "Robot" op `system.html` met bevestiging -> `/system/reboot` /
      `/system/shutdown` in `launch_control_node` (launches stoppen,
      uit-melodie, logind via gemounte `/run/dbus/system_bus_socket`).
      logind-rechten bevestigd (`CanReboot`/`CanPowerOff` = yes). Nog te
      testen in de nieuwe image. Let op: compose op elke robot heeft de
      extra D-Bus-mount nodig. **Getest 2026-10-06**: Herstarten via de knop
      OK (uit-melodie, echte reboot 23:46, alles + "on"-melodie terug).
      Uitschakelen nog niet apart getest (zelfde pad, enkel `PowerOff`).
- [x] **Piep bij correcte opstart** - gebouwd 2026-10-06 (turtlebot_docker
      `4e953d5`): `beep.py` (OpenCR-melodie via 1 Dynamixel-2.0-write op
      adres 50, of `/sound` tijdens bringup) - beide paden live bevestigd
      (2 melodietjes gehoord). `services_start.sh` speelt "on" als poorten
      7447/8080/9090/7681 open zijn, "error" na 90 s. Getest in de nieuwe
      image (container-start en reboot): melodie gehoord. "error"-pad nog
      niet getest.
- [ ] **Objectdetectie (YOLO) op de camera-topic**
      (`/camera/image_raw/compressed`). Drie opties, op volgorde van
      voorkeur:
      1. **Op de laptop/WSL van de student** (aanbevolen startpunt): ROS2-
         node subscribet via Zenoh, draait YOLOv8n/YOLO11n, publiceert
         detecties en/of een geannoteerd beeld. Geen wijziging aan robot
         of image, geen extra CPU-last naast SLAM/Nav2; didactisch het
         onderscheid robot vs. edge compute.
      2. **Op de Pi 5 zelf, enkel CPU**: haalbaar maar traag (geschat
         ~1-3 fps met PyTorch, ~5-10 fps na NCNN/ONNX-export op lagere
         resolutie - niet gemeten). Concurreert met Nav2/SLAM, en
         `ultralytics`+`torch` maakt de image fors groter -> dan in een
         aparte container.
      3. **Op de Pi 5 met Raspberry Pi AI HAT+ (Hailo-8L/8)**: realtime
         (>30 fps), maar hardware-aankoop per robot. Hailo-drivers worden
         goed ondersteund onder Raspberry Pi OS.

- [x] **Gedeelde kop op alle pagina's** (2026-10-09, `d8ff090`): tabbladen
      Status | Navigatie | Systeem + iconen batterij (staaf), wifi (streepjes),
      Pi-temperatuur (thermometer, voeding/ventilator in tooltip), internet.
- [x] **Lidar-draaiuren** (2026-10-09): de LDS-02 heeft geen motor-commando
      en draait zolang hij USB-stroom krijgt, ook zonder bringup (gemeten: data
      op `/dev/ttyUSB0` zonder driver). `system_info_node` telt de tijd dat
      `/dev/ttyUSB0` bestaat -> `state/lidar_hours.json`, getoond op
      `system.html`. Teller start op 2026-10-09 (geen historiek).
- [x] **Lidar uitzetten als hij niet nodig is** (2026-10-09): de LDS-02 heeft
      geen motorcommando, maar de USB-stroom van de Pi 5 kan uit - enkel voor
      alle 4 poorten samen (`uhubctl` op alle root hubs; enkel poort 3-1 uit
      zet de 5V niet af). Getest op 09: lidar stopt, OpenCR (op batterij) en
      F710 komen na "aan" terug. Schakelen gebeurt op de HOST
      (`usb_power_host.sh`, `turtlebot-usb-power@on|off.service`, uhubctl via
      setup): uhubctl in de container liet spooktoestellen achter. Image:
      `usb_power on|off|status` (start de host-unit via D-Bus);
      `launch_control_node` zet de stroom uit na 2 min zonder gebruik (geen
      launch, geen proces met ttyACM0/ttyUSB0/input open) en aan voor
      bringup/SLAM/Navigatie/joystick; knop + "automatisch"-vinkje op
      system.html; `ros2 launch`-wrapper in de terminal zet ze aan.
      docker-compose: ttyACM0/ttyUSB0 uit `devices:` (container moet ook
      starten met USB uit). Getest op 09 (zonder rijden): auto-uit, bringup en
      joystick vanuit "uit", weigeren van "uit" tijdens gebruik, terminal-
      wrapper. Nog met Jeremy: knop/vinkje op system.html bekijken.
- [ ] **Lidar-scan op het camerabeeld leggen**: vraagt de intrinsieke
      kalibratie (`camera_info`) en de extrinsieke (TF `base_scan` ->
      camera optisch frame, zie camerakalibratie hierboven). Dan per scanpunt
      projecteren in het beeld (op de laptop in `turtlebot_vis` of op de
      pagina met canvas).
- [x] **MPPI-controller** aanbieden op `nav.html` (2026-10-09: 1000 trajecten, 8-15% van 1 kern, rijdt goed) (zit in de image, maar zwaar
      voor een Pi 5 naast de rest - eerst CPU meten met kleinere batch).
- [x] **2026-10-09 avond - gebouwd** (handleiding: turtlebot_docker/docs/statuspagina.md):
      tab Projecten (project.json per project): lidar_avoid, apriltag_demo,
      nav_patrol, explore_demo (+ explore_lite uit de broncode); camera-
      instellingen + intrinsieke kalibratie per resolutie (calibrate_camera.sh
      in turtlebot_vis); kaart export/import als zip (+png), kaartenbibliotheek
      in de monitor; "Aanpassingen"-icoon; zones ook tijdens SLAM/verkennen
      (+ verkenningsgebied); Verkennen en SLAM/Navigatie sluiten elkaar uit;
      rosbridge-waakhond (getest met SIGSTOP); odometrie start op 0;
      turtlebot3_ros respawn; batterij 0 % = 11,0 V.
      Lessen: twee Nav2-stacks tegelijk -> robot rijdt door + Pi overbelast ->
      rosbridge (Zenoh) vast; "Alles standaard"/auto-wissen mag nooit werk van
      de gebruiker wissen (map_buro-bewerking + 4 zones verloren).
- [ ] **Testen met Jeremy (open)**: AprilTag (tag op gsm) + camerakalibratie
      (dambord); lidar_avoid en nav_patrol rijdend; verkennen met
      verkenningsgebied (raam); kaart naar andere robot via export of monitor;
      monitor met vast IP (monitor.conf) en meerdere robots.
- [ ] **Rijtests met batterij (open van 2026-10-09)**: verboden zone + virtuele
      muur (pad gaat erom), voorkeurszone (+ kost in Geavanceerd), snelheidszone
      (vertraagt hij?), lege batterij -> rode melding en na wisselen komt
      turtlebot3_ros vanzelf terug (respawn).
- [ ] **Kaart + zones + routes exporteren/importeren** naar andere robots
      (vraag Jeremy 2026-10-09). Opties: (a) downloaden/uploaden als bundel
      via nav.html (laptop wisselt van AP), (b) kaartenbibliotheek op de
      fleet monitor: robot uploadt, andere robots halen op via het
      opdrachtkanaal (werkt door de NAT, ook voor alle robots tegelijk).
- [ ] **Noodstop / actieve stuurbron tonen** (twist_mux-vervolg): e-stop-knop
      op elke pagina (twist_mux lock-topic) + welke bron rijdt nu.
- [x] **Kaartbeheer** (2026-10-09: hernoemen/kopie/verwijderen, routes per kaart, kaarteditor met origineel-backup; free_thresh-bug 0.25 -> 0.196 opgelost): kaarten hernoemen/verwijderen op de pagina, routes
      opslaan per kaart.

## Inspiratie: OpenAMRobot (github.com/openAMRobot)

- [ ] **`openamrobot-ui` demo-modus bekijken** (`docker compose up`,
      `http://127.0.0.1:5050`, "Explore without a robot") - welke pagina's
      zijn nuttig in de les? MIT-licentie; ROS 2 Jazzy (wij: Humble).
      Interessant: click-to-goal + waypoints/routes, kaartbeheer, Blockly-
      programma's, rosbag opnemen/afspelen, health/console/parameters.
      Lessen in `docs/lessons/` (o.a. 03 browser <-> ROS, 10 topics as the
      contract, 12 debugging met ROS CLI) passen bij onze rosbridge-opzet.
- [ ] **Experiment: openamrobot-ui op de laptop tegen de rosbridge van
      turtlebot09** (`ws://10.0.9.10:9090`). Verwacht: kaart/teleop/doelen/
      camera/console werken (standaard topics/Nav2-acties), routes/
      kaartbeheer/missies niet (hun Jazzy-backend-nodes). Let op: zelfde
      poorten 9090/8080 als onze robot.
- [ ] **Ideeën/code overnemen** in onze statuspagina (MIT): click-to-goal +
      waypoints, rosbag-opname, kaartbeheer.
- [ ] `openamr-platform-sw`: AprilTag-docking als studentenproject met de
      TB3-camera; "ROS 2 Complete Course" in `docs/` als extra lesmateriaal.

## Andere repos om van af te kijken (gecontroleerd 2026-10-08)

- [ ] **Foxglove-bridge / Lichtblick** (`foxglove/foxglove-sdk`, map `ros/`;
      `lichtblick-suite/lichtblick` = open-source fork van Foxglove Studio):
      visualisatie in de browser i.p.v. rviz2 in WSL, bridge is C++ en
      efficienter dan rosbridge. Mogelijk alternatief voor `turtlebot_vis`.
- [ ] **`dheera/rosboard`**: lichte webserver-node die elk ROS-topic toont -
      vergelijken met onze statuspagina (generieke topic-viewer).
- [ ] **`MoffKalast/vizanti`** (branch `ros2`): web-visualizer + missieplanner
      via rosbridge (doelen/waypoints op de kaart) - voorbeeld voor click-to-goal.
- [ ] **`robo-friends/m-explore-ros2`**: autonome exploratie (frontiers) -
      mooie demo/oefening: TB3 brengt zelf een ruimte in kaart.
- [ ] **`mgonzs13/yolo_ros`**: YOLO in ROS 2 (Humble) - voor het YOLO-
      feature hierboven (op de laptop/WSL).
- [ ] **`christianrauch/apriltag_ros`**: AprilTag-detectie (zelfde auteur
      als `camera_ros`) - markers zoeken/volgen met de TB3-camera.
- [ ] **`ROBOTIS-GIT/turtlebot3_applications`** en
      **`turtlebot3_autorace`** (branches `humble`/`jazzy`): officiele TB3-
      oefeningen met camera (lijnvolgen, autorace, parkeren) - kant-en-klare
      opdrachten.
- [ ] **`ros-navigation/navigation2_tutorials`** + Nav2 Simple Commander
      (Python): waypoints/patrouilles programmeren.
- [ ] **`linorobot/linorobot2`**: doe-het-zelf ROS 2-robot op een Pi, goede
      documentatie (setup, Nav2-tuning) als referentie.

## Migratie naar ROS 2 Jazzy (later)

- [ ] **Jazzy afwegen**. Waarom: Humble is EOL in **mei 2027** (Jazzy: mei
      2029); OpenAMRobot, linorobot2, TurtleBot4 en nieuwe Nav2-features
      (docking server, route server) mikken op Jazzy; `rmw_zenoh` is in Jazzy
      beter ondersteund; ROBOTIS heeft `jazzy`-branches voor `turtlebot3`,
      `turtlebot3_applications` en `turtlebot3_autorace`. Wat het vraagt:
      - robot-image (`turtlebot_docker`) en studenten-image (`turtlebot_vis`)
        **tegelijk** migreren: Humble en Jazzy praten niet met elkaar
        (berichttypes/type-hashes, ook niet via Zenoh);
      - basisimage `ros:jazzy` (Ubuntu 24.04), eigen builds opnieuw nakijken:
        `camera_ros`/libcamera/libpisp, `ld08_driver`, `cartographer_headless`;
      - TB3-firmware/OpenCR en `turtlebot3_node` Jazzy-compatibel?
      - les- en GitBook-materiaal nakijken op commando-/API-verschillen.
      Liefst niet midden in een semester; eerst parallel op een testrobot met
      een eigen tag (bv. `raspios-jazzy`).
- [ ] **Of Jazzy overslaan -> Lyrical Luth** (LTS, mei 2026, Ubuntu 26.04,
      EOL mei 2031). Stand 2026-10-08 (arm64-pakketten op packages.ros.org):
      Lyrical heeft al navigation2, slam_toolbox, rmw_zenoh, rosbridge,
      camera_ros, dynamixel_sdk, maar NOG GEEN turtlebot3-pakketten,
      cartographer_ros en LDS-drivers (Jazzy wel). Voorstel: dit academiejaar
      op Humble blijven (support tot mei 2027), migratie in de zomer van 2027
      rechtstreeks naar Lyrical als ROBOTIS/cartographer dan klaar zijn,
      anders Jazzy als terugval. Opnieuw nakijken voorjaar 2027.

## Studenten via VS Code

- [x] **Persistente studentenwerkmap**: code in de container verdwijnt nu bij
      elke update (container wordt opnieuw aangemaakt).
      **Gebouwd 2026-10-09, getest op turtlebot09** (image `2026-10-09 ed4c567`,
      digest `sha256:215be0ff…`): pakket gebouwd in `/root/ros2_ws`, container
      opnieuw aangemaakt -> code + build staan er nog, `ros2 pkg prefix` vindt
      het zonder `source`: bind mount `./ros2_ws` -> `/root/ros2_ws`
      (`docker-compose.yaml`, gitignored), aangemaakt door `setup_turtlebot.sh`
      (als `turtlebot`, met `src/`), leeggemaakt door `golden_prepare.sh`.
      In de image: `.bashrc` sourcet `/root/ros2_ws/install/setup.bash`
      als die bestaat; de browserterminal (ttyd) start in `/root/ros2_ws`.
      Testen: pakket maken + `colcon build` in `/root/ros2_ws`, update
      uitvoeren -> code en build staan er nog, overlay automatisch gesourcet.
      Naam `ros2_ws` (zoals de officiele ROS 2-tutorials), **ook in
      `turtlebot_vis`**: `./ros2_ws` naast `docker-compose.yaml` in WSL ->
      `/root/ros2_ws`, overlay automatisch gesourcet (lokaal getest
      2026-10-09). Let op: de containers draaien als root, dus `build/`,
      `install/` en in de container aangemaakte bestanden zijn in WSL van root
      -> vanuit VS Code in WSL niet bewerkbaar zonder sudo. Oplossen met
      `user:` in compose of studenten enkel in de container laten werken.
- [ ] **Optie A: Remote-SSH rechtstreeks in de container** - `openssh-server`
      in de image, `sshd` op poort 2222 (host-netwerk) gestart vanuit
      `services_start.sh` (+ poort in de labo-check/diensten), eigen login
      (bv. `student`, wachtwoord-patroon zoals ttyd `TurtleBot@P<nr>`),
      startmap = studentenwerkmap. Studenten zitten zo meteen in de ROS-
      omgeving zonder host-toegang (past bij "Aparte student-gebruiker").
      Aandachtspunten: ~200-300 MB RAM per verbonden VS Code-server op de Pi
      (meten met meerdere studenten op 1 robot); kaart "Verbinden vanaf je
      laptop" uitbreiden met een kant-en-klare `~/.ssh/config`-regel.
      Standaard blijft: ontwikkelen in VS Code op de laptop in `turtlebot_vis`
      (geen belasting voor de Pi); A enkel voor code die op de robot moet draaien.

## Offline gebruik (geen internet via de AP-WAN)

Werkt offline: statuspagina (roslib lokaal), teleop, labo-check, camera,
lidar, `turtlebot_vis` via Zenoh, SSH/ttyd, bringup/SLAM/Nav2 - alles blijft
binnen het AP-netwerk van de robot.

- [ ] **VS Code Remote-SSH offline**: de VS Code Server wordt bij de eerste
      verbinding gedownload. Op de laptops `"remote.SSH.localServerDownload":
      "always"` zetten (laptop downloadt de arm64-server en kopieert hem via
      SSH), of de server vooraf in de golden image zetten (versie moet bij de
      VS Code-client passen).
- [ ] **Studentenlaptops wisselen van netwerk**: Windows ziet "geen internet"
      op `TB-AP-<nr>` en kan automatisch naar eduroam springen -> robot weg.
      In de lesinstructies: automatisch verbinden met andere netwerken uit,
      of de AP's toch internet geven via de switch.
- [ ] **Klok zonder NTP**: nagaan of de RTC van elke Pi 5 een batterij heeft;
      zonder batterij kan de tijd na een stroomonderbreking verkeerd staan
      (TF-problemen in rviz op de laptop; zichtbaar in de labo-check "Klok").
      Eventueel de robot zelf als NTP-server voor de laptop, of omgekeerd.
- [ ] **Vooraf ophalen**: Docker-images (`turtlebot_vis` in WSL, robot-image)
      en apt/pip-pakketten die studenten nodig hebben, in het begin van het
      semester - offline werkt `docker pull`/`apt install`/`pip install` niet.
- [x] **Update-knop offline** (2026-10-10, na labotest op school zonder
      internet): `update_turtlebot.sh` controleert eerst internet (1.1.1.1/8.8.8.8,
      DNS + github.com/registry-1.docker.io, max 10 s per test), git pull met
      timeout 120 s, unit `TimeoutStartSec=30min`; laatste stap/fout in
      `state/update_status.txt` -> system.html ("Update bezig: <stap>" /
      "mislukt - Geen internet via de AP ..."). launch_control_node weigert de
      update meteen zonder internet. Pagina-deel pas na een image-build
      (turtlebot_docker), script-deel na de eerste update (git pull).
- [x] **"Alles bijwerken" in de vlootmonitor in groepjes** (2026-10-10):
      wachtrij in `monitor/monitor.py` (1/2/3 tegelijk, standaard 2), voortgang +
      fouten per robot, "Wachtrij stoppen". Klaar-detectie via `launch.update`
      (robot-image vanaf turtlebot_docker na cbde25f); oudere robots: klaar na
      offline->online of na 6 min. Getest met nagebootste robots, nog niet met
      de echte vloot.
- [ ] **Terug naar een oudere versie (rollback)**: nu bestaat enkel de
      meeschuivende tag `raspios-zenoh`, oude builds staan alleen nog als
      digest op Docker Hub. Plan: elke build ook als versietag pushen
      (`raspios-zenoh-<datum>-<commit>`), compose-image via `.env`
      (`TURTLEBOT_IMAGE`, door setup_turtlebot.sh uit `state/image_pin`), op
      system.html een keuzelijst met de versietags (Docker Hub API) +
      "Terug naar nieuwste". Update-hint en vlootmonitor tonen "vastgepind".
      **Eerste stap gebouwd 2026-10-10**: update_turtlebot.sh bewaart de vorige
      image als `:vorige` (enkel als er na de pull >= 5 GB vrij is - turtlebot09
      heeft 32 GB; enkel verschillende lagen kosten ruimte), `rollback_turtlebot.sh`
      + `turtlebot-rollback.service` wisselen huidige en vorige om (zonder
      internet; nog eens = terug). host_info.json `image_previous`; system.html
      knop "Terug naar vorige versie" + /system/rollback (turtlebot_docker, pas na
      image-build). Lokaal getest met test-images, nog niet op een robot. Werkt
      pas vanaf de 2e update na deze wijziging. Enkel de image, niet de setup-repo.
- [ ] **Smartphone/laptop op AP zonder internet**: Android/iOS sturen het verkeer
      dan via mobiele data -> statuspagina laadt niet (2026-10-10 op school).
      In de lesinstructies: mobiele data uit, of "verbonden blijven" kiezen.

## Gebruikers en rechten

- [ ] **Aparte `student`-gebruiker met minder rechten** - doel: ongelukken
      voorkomen (`sudo apt upgrade`, wifi wijzigen, compose-bestanden
      wissen), géén echte security-grens. Let op: lidmaatschap van de
      `docker`-groep = root-equivalent, en de container draait
      `privileged: true`, dus elke shell in de container (ook via ttyd) kan
      in de praktijk alles op de host. Opties:
      1. `student` zonder `sudo`/`netdev`/`docker`-groep; `.env` en
         `docker-compose.yaml` blijven van `turtlebot` (enkel leesbaar).
      2. Docker-toegang via een sudoers-whitelist i.p.v. de `docker`-
         groep, bv. enkel `docker ps`, `docker logs`,
         `docker exec -it turtlebot_* bash`.
      3. (Later, echte hardening) `privileged: true` vervangen door
         expliciete `devices:` + `cap_add` (OpenCR, lidar, I2C, camera:
         `/dev/media*`, `/dev/video*`, `/dev/dma_heap`) - opnieuw testen,
         vooral de camera.
      **Eerst beslissen**: wat moeten studenten in les 1 concreet kunnen op
      de robot - enkel in de container ROS2-commando's typen, ook zelf
      `docker compose up/down`/`ps`/`logs`, of ook Linux-basics op de host?

## Afspraken / te beslissen

- [ ] **Campus-netwerkbeheer** bevestigen dat 9 AP's achter 1 switch-
      uplink geen probleem is (DHCP-leases, eventueel apart VLAN).
- [ ] **AP-kanaaltoewijzing** bijstellen zodra de tafelschikking in het
      lokaal vastligt.

- [x] **Image-versie op de statuspagina** (2026-10-07, turtlebot_docker
      `a08d4e5`): build-arg `IMAGE_VERSION`, getoond op `system.html`.
- [x] **Software bijwerken vanuit de webpagina** (2026-10-07): knop op
      `system.html` -> `/system/update` -> host-unit `turtlebot-update.service`
      (git pull + setup + `docker compose pull`/`up -d`). Via de host getest
      (nieuwe image binnen 24 s, container opnieuw aangemaakt); de knop zelf
      nog te testen in de browser.
- [x] **Statuspagina-uitbreiding** (2026-10-07, turtlebot_docker `6e9aa67`,
      image live op turtlebot09 via de update-service): Pi-gezondheid
      (temperatuur, onderspanning/throttling + 5V via `/dev/vcio`, SD-kaart),
      lidar-plot met instelbare verversing (rosbridge `throttle_rate`),
      labo-check-kaart, verbindingsinfo voor WSL met kopieerknop + verbonden
      Zenoh-laptops, `/rosout`-logviewer. Nog na te kijken in de browser
      (layout, lidar-plot oriëntatie, kopieerknop over http).
- [x] **Camera aan/uit vanuit de webpagina** (2026-10-08, turtlebot_docker
      `061c6b2`): knop op de camerakaart (`index.html`) + start/stop in
      Launch control. Keuze onthouden in `~/turtlebot_setup/state/camera_enabled`
      (bind mount, overleeft update/herstart; zonder bestand geldt
      `ENABLE_CAMERA` uit de CSV). `camera_node` start enkel als er een
      sensor is (`camera_present.sh`, v4l-subdev-naam; `cam -l` segfault).
      Getest op 09 (aan/uit, onthouden na container-herstart).
- [x] **Software-versies + diagnose op de statuspagina** (2026-10-08,
      turtlebot_docker `7aa8cfd`, turtlebot_setup `b84f740`): golden-stempel
      (`/etc/turtlebot-golden`, gezet door `tools/golden_prepare.sh`), setup-
      commit, OS/kernel/Docker/bootloader (`state/host_info.json`, geschreven
      door `setup_turtlebot.sh`), vorige afsluiting netjes/onverwacht, klok-
      verschil robot-laptop + NTP (timesyncd-config: be.pool, Debian als
      terugval), ping/jitter naar het AP, diensten, container-starts,
      SD-kaartfouten (dmesg). Live op 09, `system_info_node` blijft ~0 % CPU.
- [x] **Commit-links + update-hint** (2026-10-08, turtlebot_docker `ebe002c`,
      turtlebot_setup `e167150`): klikbare commits (setup, image, golden),
      laatste 5 setup-commits, "Update beschikbaar" (robot controleert om de
      30 min GitHub + Docker Hub-digest). Golden-stempel nu
      `V<major>.<minor>.<patch>.<build>` (`golden_prepare.sh [x.y.z]`).
- [x] **Golden image V0.1.0.2** (2026-10-08 00:54, setup `fb0696c`, image
      `eb4442f`) op de laptop (`~/turtlebot_clone/turtlebot-golden.img`).
      Geflasht op turtlebot06: volledig automatisch OK (identiteit, keys
      `root@turtlebot06`, partitie, wifi, `.env`, buildkit + image weg,
      services + piep, diagnose, update-hint -> update-service -> up-to-date).
      Nieuwe golden: `sudo ~/turtlebot_setup/tools/golden_prepare.sh [x.y.z]`
      op 09, uitschakelen, `sudo bash ~/turtlebot_clone/sdclone.sh read
      /dev/mmcblk0` (echte terminal).
- [x] **Camera-knop getest op een robot zonder camera** (turtlebot06,
      2026-10-08): AAN -> "geen camera gevonden - 'aan' onthouden", geen
      camera_node; container-herstart -> "[camera] ingeschakeld maar geen
      camera gevonden", alle services up; UIT -> onthouden.
- [ ] **Rosbag opnemen vanuit de webpagina**: start/stop-knop, bestand
      downloaden (studenten nemen data op de robot op en spelen thuis af).
- [x] **Camera-verversing instelbaar** (zoals de lidar-plot), om wifi-
      verkeer te beperken als veel pagina's open staan.
      **Opgelost 2026-10-07** (turtlebot_docker `5eb79ec`): uit/1/5/max fps, standaard 5.
- [ ] **Voortgangsbalk tijdens de update** (`docker compose pull`) op de
      webpagina.

## Laag prioritair

- [ ] rviz2 Image-display toont `compressed` niet in de transport-dropdown
      (werkt wel; `rqt_image_view` als workaround).
- [ ] Eventueel 64 GB SD-kaart voor de testrobot (turtlebot09 heeft
      `SD32G`), zodat bouwen op de robot niet telkens vastloopt.
