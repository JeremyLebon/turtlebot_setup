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

- [ ] **Robot blijft op een ander wifi-netwerk hangen** (2026-10-09:
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

- [ ] **`turtlebot_vis`: shell sluit bij elk mislukt commando** (bv. een
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

## Features

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
- [ ] **Internetverbinding-indicator** op de statuspagina: `system_info_node`
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
- [ ] **Prioriteit tussen stuurbronnen met `twist_mux`** -
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
- [ ] **Masterpagina: alle turtlebots in 1 overzicht** (batterij, temperatuur,
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
- [ ] **Nav2-navigatie op de webpagina**: kaart tonen (`/map`), robotpositie
      (TF `map`->`base_footprint`), beginpositie zetten (`/initialpose`,
      zoals "2D Pose Estimate" in rviz), doel klikken (`navigate_to_pose`),
      gepland pad (`/plan`) en voortgang/annuleren. De Navigation-knop
      (`navigation2.launch.py` met opgeslagen kaart) bestaat al; dit maakt het
      bruikbaar zonder rviz. Vervangt/omvat het punt "Waypoint/doel zetten"
      hieronder.
- [ ] **Traject tekenen op de kaart**: meerdere punten aanklikken -> route
      (Nav2 `navigate_through_poses` of `follow_waypoints`), routes opslaan
      in `state/` en opnieuw afspelen, eventueel in een lus (patrouille).
      Bouwt verder op de Nav2-webpagina; voorbeelden: `vizanti`, OpenAMRobot
      (zie hieronder).

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

- [ ] **Persistente studentenwerkmap**: code in de container verdwijnt nu bij
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
- [ ] **Update-knop offline**: mislukt (`git pull`/`docker pull`); de update-
      hint toont "kon niet controleren". Melding op de pagina duidelijker maken
      ("geen internet - update niet mogelijk").

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
