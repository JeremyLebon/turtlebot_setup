# Todo / featurelijst - RaspiOS + Zenoh + per-robot AP migratie

Centrale lijst van open punten (branch `raspios-migration`). Details en
achtergrond staan in de migratielogs (`raspios-migration-log.md`,
`ap-migration-log.md`); deze lijst verwijst ernaar i.p.v. alles te
herhalen. Laatst bijgewerkt: 2026-10-06.

## Voor de fleet-uitrol

- [ ] **Polkit/NetworkManager-rechten** voor de `turtlebot`-user, zodat
      `nmcli device wifi connect` geen `sudo` meer vraagt (zie
      `ap-migration-log.md`, gotchas turtlebot09).
- [ ] **AP router-modus uit de doos bevestigen**: start elke TL-WR902AC
      automatisch in router-modus zodra WAN aangesloten is, of was dat bij
      turtlebot09 toeval?
- [ ] **Image-grootte onderzoeken**: `raspios-zenoh` is gegroeid van
      5,17 GB naar 7,64 GB. Uitzoeken met `docker history` (apt-cache,
      libcamera/colcon build-artefacten in lagen?). Relevant voor 8 robots
      die over wifi pullen op SD-kaarten van 32 GB.
- [x] **Image herbouwen + pushen** (2026-10-06, digest
      `sha256:74c5692b...`, turtlebot09 draait erop) met de wifi-signaalweergave
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
- [x] **Buildkit-cache opruimen** (2026-10-06, 6,7 GB vrijgemaakt; volgende
      build op de robot start dus van nul) op turtlebot09 na de Docker Hub-push
      (SD-kaart van 32 GB loopt vol bij builds op de robot).

## Uitrol

- [ ] **AP + robot configureren voor turtlebot01-08** (tabel in
      `ap-migration.md`, status "open").
- [ ] **Overige 8 robots naar Raspberry Pi OS + Docker** (alles is tot nu
      toe enkel op turtlebot09 gevalideerd).
- [ ] **`raspios-migration` mergen naar `master`** - bewust pas na
      volledige validatie (zie beslissing 2026-10-03).

## Bugs

- [ ] **SLAM-knop geeft geen kaart** (gevonden 2026-10-04, turtlebot09).
      `navigation2.launch.py slam:=True` (wat launch control start):
      slam_toolbox registreert de lidar, verwerkt de eerste scan en hangt
      dan - geen logs meer (ook niet de periodieke "Graph size"-debugregel),
      bijna 0% CPU, nooit een `/map`. Ook zo bij rechtstreeks starten,
      dus niet de schuld van launch control.
      Werkt wél: slam_toolbox alleen (`ros2 run`, `online_sync_launch.py`)
      en `nav2_bringup slam_launch.py` - 5/5 keer kaart binnen seconden.
      Scans (~10 Hz, 215-220 punten) en TF `odom -> base_scan` zijn OK; de
      "LaserRangeScan contains X range readings, expected Y"-meldingen
      (LDS-02 met variabele lengte) zijn niet de oorzaak.
      Vermoeden (niet bewezen): een blokkerende publish in `rmw_zenoh`
      (RELIABLE publisher, congestion control "block") zodra de Nav2-stack
      meeluistert op `/map`. Gisteren werkte dezelfde knop wel; de versies
      (`rmw_zenoh 0.1.9`, `slam_toolbox 2.6.10`, `nav2 1.1.20`) lijken
      ongewijzigd. Wel anders: services via entrypoint, `ROS_DOMAIN_ID`
      99 -> 9, container opnieuw aangemaakt.
      Volgende stappen: `gdb` in de container voor een stacktrace van de
      hangende node; test met `rmw_cyclonedds_cpp`; workaround = SLAM-knop
      enkel `nav2_bringup slam_launch.py` laten starten (kaart maken met
      teleop, opslaan, dan Navigation met de kaart).

## Testen

- [ ] **Zenoh-client vanaf een studentenlaptop in WSL** (`ros2 topic list`
      over het AP-netwerk, `ROS_DOMAIN_ID=9` voor turtlebot09).
- [ ] **WSL mirrored networking mode** testen, zodat `.local`-hostnames
      ook in WSL werken (zie "Robot bereiken: hostname of IP" in
      `ap-migration.md`).
- [ ] **I2C-shield / Grove Base Hat** terug aansluiten na de bordwissel en
      testen.

## Features

- [ ] **Waypoint/doel zetten via de webpagina**: klikken op de kaart ->
      Nav2 `navigate_to_pose` / `/goal_pose`, klik-coordinaten omrekenen
      via `msg.info.resolution`/`msg.info.origin` (zie
      `ap-migration-log.md`).
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

## Laag prioritair

- [ ] rviz2 Image-display toont `compressed` niet in de transport-dropdown
      (werkt wel; `rqt_image_view` als workaround).
- [ ] Eventueel 64 GB SD-kaart voor de testrobot (turtlebot09 heeft
      `SD32G`), zodat bouwen op de robot niet telkens vastloopt.
