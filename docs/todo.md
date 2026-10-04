# Todo / featurelijst - RaspiOS + Zenoh + per-robot AP migratie

Centrale lijst van open punten (branch `raspios-migration`). Details en
achtergrond staan in de migratielogs (`raspios-migration-log.md`,
`ap-migration-log.md`); deze lijst verwijst ernaar i.p.v. alles te
herhalen. Laatst bijgewerkt: 2026-10-04.

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
- [ ] **Buildkit-cache opruimen** op turtlebot09 na de Docker Hub-push
      (SD-kaart van 32 GB loopt vol bij builds op de robot).

## Uitrol

- [ ] **AP + robot configureren voor turtlebot01-08** (tabel in
      `ap-migration.md`, status "open").
- [ ] **Overige 8 robots naar Raspberry Pi OS + Docker** (alles is tot nu
      toe enkel op turtlebot09 gevalideerd).
- [ ] **`raspios-migration` mergen naar `master`** - bewust pas na
      volledige validatie (zie beslissing 2026-10-03).

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
