# Todo / featurelijst - RaspiOS + Zenoh + per-robot AP migratie

Centrale lijst van open punten (branch `raspios-migration`). Details en
achtergrond staan in de migratielogs (`raspios-migration-log.md`,
`ap-migration-log.md`); deze lijst verwijst ernaar i.p.v. alles te
herhalen. Laatst bijgewerkt: 2026-10-07.

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

## Uitrol

- [ ] **Nieuw `docker-compose.yaml` naar elke robot** (met de mount
      `/run/dbus/system_bus_socket`, nodig voor de aan/uit-knoppen; zonder
      die mount geven ze een foutmelding). Image `raspios-zenoh` van
      2026-10-06 of later.
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
- [ ] **Golden image opkuisen voor het klonen**: container `turtlebot_9`
      en de `buildx_buildkit_rpi50`-builder + cache verwijderen (enkel
      nodig op de bouwrobot), `/tmp`-logs, bash-history, testkaarten.
- [ ] **Image verkleinen**: turtlebot09 heeft een kaart van 32 GB - het
      image eerst inkrimpen (bv. PiShrink) zodat het ook op een iets
      kleinere 32 GB-kaart past en sneller schrijft.
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

## Bugs

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

- [ ] **Zenoh-client vanaf een studentenlaptop in WSL** (`ros2 topic list`
      over het AP-netwerk, `ROS_DOMAIN_ID=9` voor turtlebot09).
- [ ] **WSL mirrored networking mode** testen, zodat `.local`-hostnames
      ook in WSL werken (zie "Robot bereiken: hostname of IP" in
      `ap-migration.md`).
- [ ] **I2C-shield / Grove Base Hat** terug aansluiten na de bordwissel en
      testen.

## Features

- [ ] **Waypoint/doel zetten via de webpagina** (+ robotpositie en het
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
- [ ] **Nieuwe golden image** maken: `sudo ~/turtlebot_setup/tools/golden_prepare.sh`
      op 09 (apt upgrade, pull, stempel, opkuis), uitschakelen, kaart inlezen
      met `~/turtlebot_clone/sdclone.sh read /dev/mmcblk0` (in een echte
      terminal, sudo).
- [ ] **Camera-knop testen op een robot zonder camera** (turtlebot06):
      update via "Software bijwerken", dan camera AAN -> melding "geen camera
      gevonden", geen crash; container herstarten -> "[camera] ingeschakeld
      maar geen camera gevonden"; daarna terug UIT.
- [ ] **Rosbag opnemen vanuit de webpagina**: start/stop-knop, bestand
      downloaden (studenten nemen data op de robot op en spelen thuis af).
- [ ] **Camera-verversing instelbaar** (zoals de lidar-plot), om wifi-
      verkeer te beperken als veel pagina's open staan.
- [ ] **Voortgangsbalk tijdens de update** (`docker compose pull`) op de
      webpagina.

## Laag prioritair

- [ ] rviz2 Image-display toont `compressed` niet in de transport-dropdown
      (werkt wel; `rqt_image_view` als workaround).
- [ ] Eventueel 64 GB SD-kaart voor de testrobot (turtlebot09 heeft
      `SD32G`), zodat bouwen op de robot niet telkens vastloopt.
