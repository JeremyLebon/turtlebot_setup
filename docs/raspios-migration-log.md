# Uitvoeringslogboek - raspios-migration

Logboek van wat er effectief al uitgevoerd is op de eerste testrobot, zodat
je dit ook zelfstandig (of op de volgende robot) kan herhalen. Volgorde
volgt `raspios-migration.md`. Enkel echt uitgevoerde stappen staan hier -
voor de volledige/generieke instructies zie `raspios-migration.md`.

**Testrobot:** RPi5, hostname `raspberrypi`, IP `192.168.60.69`,
user `turtlebot` (wachtwoord: zie eigen wachtwoordbeheer, niet hier
genoteerd).

**Sessie:** 2026-09-21

## Stap 0 - Verkenning (read-only, vóór wijzigingen)

Bevindingen (zie ook chat voor volledig verslag):
- OS: Debian 13 (trixie) op Raspberry Pi OS, kernel `6.18.50+rpt-rpi-2712`, arm64.
- I2C al werkend: `/dev/i2c-1`, `/dev/i2c-13`, `/dev/i2c-14` aanwezig,
  `dtparam=i2c_arm=on` staat al in `/boot/firmware/config.txt`.
- `camera_auto_detect=1` staat al aan, `rpicam-hello` aanwezig, maar
  `rpicam-hello --list-cameras` -> "No cameras available!" (nog geen
  CSI-camera fysiek aangesloten op deze robot - volgt later).
- Docker: nog niet geinstalleerd.
- Netwerk: enkel wlan0 actief (192.168.60.69/24), eth0 down/niet aangesloten.

Conclusie: stap 1 (flashen) en stap 2 (I2C) uit `raspios-migration.md` waren
op deze robot al gebeurd/standaard aanwezig. Verdergegaan bij stap 4
(Docker) - stap 3 (camera-sanity-check) volgt later zodra de camera
fysiek aangesloten is.

## Stap 4 - Docker installeren (uitgevoerd, 2026-09-21)

Commando's, uitgevoerd via SSH op `turtlebot@192.168.60.69`:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker turtlebot
rm -f get-docker.sh
# nieuwe SSH-sessie openen zodat de docker-groep actief is (relogin vereist)
```

Resultaat:
- Docker Engine **29.8.1** geinstalleerd (community, arm64), incl.
  `docker-compose-plugin` (**Docker Compose v5.5.1**) en `docker-buildx-plugin`.
  Geinstalleerd via het officiele Debian-apt-repo (`download.docker.com/linux/debian trixie`).
- Docker-service via systemd enabled + gestart (`systemctl enable --now docker.service`).
- `turtlebot`-gebruiker toegevoegd aan de `docker`-groep -> `docker ps` en
  `docker compose version` werken zonder `sudo` (geverifieerd in een
  nieuwe SSH-sessie).

Nog te doen op deze robot (volgende sessie): stap 5 (repo's clonen - branch
`raspios-migration` moet dan wel eerst gepusht zijn naar GitHub, staat nu
nog enkel lokaal), stap 6 (image bouwen), stap 7 (systemd-unit), stap 8
(stack testen), camera fysiek aansluiten + stap 3 opnieuw.

## Stap 6 (voorbereiding) - Remote buildx-builder op de RPi5 (uitgevoerd, 2026-09-21)

In plaats van bouwen op de RPi5 zelf (te traag) of via QEMU-emulatie op de
laptop (traag voor de nieuwe `libcamera`-build), is gekozen voor een
buildx-builder die vanaf de laptop getriggerd wordt maar native op de RPi5
compileert. Uitgevoerd op de laptop (niet op de robot):

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub turtlebot@192.168.60.69
ssh turtlebot@192.168.60.69 'echo passwordless OK'   # verificatie

docker buildx create --name rpi5 --driver docker-container \
  --platform linux/arm64 "ssh://turtlebot@192.168.60.69"
docker buildx inspect rpi5 --bootstrap
```

Resultaat:
- Passwordless SSH van laptop (`jeremy@rosdrivenjeremy`, key `~/.ssh/id_ed25519`)
  naar `turtlebot@192.168.60.69` werkt.
- Builder `rpi5` aangemaakt en bootstrapped: BuildKit v0.32.2, driver
  `docker-container`, endpoint `ssh://turtlebot@192.168.60.69`, platform
  `linux/arm64` als **native** primair platform (geverifieerd met een
  test-build: `uname -m` -> `aarch64`, gebouwd in ~1s, geen QEMU-vertraging).
- Nog te doen: de effectieve `turtlebot-rpi5:raspios`-image bouwen/pushen
  met `docker buildx build --builder rpi5 --platform linux/arm64 -f
  docker/Dockerfile -t nobel86/turtlebot-rpi5:raspios --push .` (dit is de
  volgende, langere stap - nog niet uitgevoerd; `raspios-migration`-branch
  moet ook nog gepusht worden naar GitHub of lokaal beschikbaar zijn op het
  build-pad).

## Stap 6 - Image build, poging 1: gefaald (2026-09-21)

`docker buildx build --builder rpi5 ...` gestart (lokaal working-tree pad,
branch nog niet gepusht). Faalde op de libcamera-buildstap:

```
meson.build:3:0: ERROR: Value "rpi/pisp" for option "pipelines" is not in
allowed choices: "all, auto, imx8-isi, ipu3, mali-c55, rkisp1, rpi/vc4,
simple, uvcvideo, vimc, virtual"
```

Oorzaak: `docker/Dockerfile` clonede tag `v0.4.0` van
`raspberrypi/libcamera`, en die versie kent de `rpi/pisp`-pipeline (nodig
voor de RPi5 ISP) nog niet - die is pas later toegevoegd.

Fix: `git ls-remote --tags` gebruikt om recente tags op te lijsten, tag in
`docker/Dockerfile` gewijzigd naar `v0.7.2+rpt20260817` (meest recente
gedateerde Raspberry Pi-release op moment van build). Build opnieuw gestart.

## Stap 6 - Image build, poging 2: geslaagd (2026-09-21)

Zelfde commando als hierboven, met de gefixte libcamera-tag. `libcamera`
bouwde succesvol (169.7s), colcon-build (turtlebot3-packages, ld08_driver,
camera_ros) geslaagd, image geëxporteerd en gepusht naar
`nobel86/turtlebot-rpi5:raspios`.

**Push bevestigd afgerond**: `docker.io/nobel86/turtlebot-rpi5:raspios`,
digest `sha256:b4987376446e10a07f1f957883e1f5d1fa4a1183db9ff97f88c7c122c56947c5`.
Push zelf duurde ~718s (~12 min) - logisch gezien de wifi-uplink van de
robot en de omvang van de image (libcamera + nav2 + cartographer).
`docker compose pull` op de testrobot zou deze nu moeten kunnen ophalen
(compose gebruikt al de `:raspios`-tag, zie stap 6 hierboven in
`raspios-migration.md`).

## Stap 3/2 - I2C-test (uitgevoerd, 2026-09-21)

Camera nog niet fysiek aangesloten (I2C-shield zit ervoor), dus eerst I2C
getest i.p.v. camera (stap 3 uit de gids).

```bash
sudo apt-get install -y i2c-tools   # was al geinstalleerd, versie 4.4-2
sudo i2cdetect -y 1
sudo i2cdetect -y 13
sudo i2cdetect -y 14
```

Resultaat:
- **Bus 1** (GPIO-header I2C): 1 device gevonden op **adres 0x38**
  (vermoedelijk het I2C-shield zelf of een sensor erop, bv.
  AHT10/AHT20-temp/vocht-sensor of PCF8574 I/O-expander). Bevestigt dat
  I2C end-to-end werkt op deze Raspberry Pi OS-build.
- **Bus 13 en 14**: elk adres antwoordt - geen echte devices, vermoedelijk
  HDMI-DDC/CEC-buslijnen, niet relevant voor peripherals. Genegeerd.

Nog te doen: camera fysiek aansluiten zodra het I2C-shield dat toelaat,
dan stap 3 (camera-sanity-check) alsnog uitvoeren.

## Grove Base Hat - analoge poorten (uitgevoerd, 2026-09-21)

Het I2C-shield op deze testrobot is een **Grove Base Hat voor Raspberry
Pi**. Diens ADC-chip zit op I2C-adres **0x04** (bus 1) - niet zichtbaar in
een gewone `i2cdetect -y 1` scan, want 0x00-0x07 is het gereserveerde
adresbereik dat standaard wordt overgeslagen. Wel zichtbaar met:

```bash
sudo i2cdetect -y -a 1   # -a = scan ook gereserveerde adressen
```

Officiele Seeed-library geinstalleerd en getest:

```bash
sudo pip3 install --break-system-packages grove.py
sudo python3 -c "
from grove.adc import ADC
adc = ADC()
for ch in range(8):
    print(ch, adc.read_raw(ch), adc.read_voltage(ch))
"
```

Resultaat: alle 8 kanalen lezen consistente waarden (geen fouten) - ADC en
I2C-pad werken end-to-end. Waarden zelf zijn ruis (~1.6-1.8V), want er
hangt nog geen sensor aan de poorten - normaal voor zwevende ingangen.

Nog te doen: een echte analoge sensor (potentiometer, lichtsensor, ...) op
een Grove-poort aansluiten en het bijhorende kanaal opnieuw uitlezen ter
bevestiging.

## Stap 8 - Volledige stack testen (uitgevoerd, 2026-09-21)

`docker-compose.yaml` (raspios-migration) naar de testrobot gekopieerd
(`~/turtlebot_setup_test/`, branch nog niet gepusht dus via `scp`). Testwaarden
in `.env`: `TURTLEBOT_NR=99`, `ROS_DOMAIN_ID=99`, `LDS_MODEL=LDS-01` (dummy
- deze robot staat niet in `turtlebot_config.csv`).

Eerste poging: `/dev/ttyUSB0` (LIDAR) en `/dev/input/js0` (gamepad)
ontbraken nog op deze testrobot -> tijdelijke
`docker-compose.override.yaml` gebruikt om enkel `ttyACM0` + `i2c-1` te
mounten. Na het aansluiten van de ontbrekende hardware: override verwijderd,
volledige compose gebruikt.

```bash
docker compose pull
docker compose up -d
docker exec turtlebot_99 bash -c "source /root/turtlebot3_ws/install/setup.bash; ros2 launch turtlebot3_bringup robot.launch.py"
```

Resultaat:
- `ros2 pkg list` bevestigt `camera_ros` en `ld08_driver` aanwezig naast de
  standaard turtlebot3-packages.
- Bringup geslaagd: OpenCR verbonden op `/dev/ttyACM0`, gyro-kalibratie
  voltooid, alle publishers/servers gestart zonder fouten.
- `/imu` publiceert stabiel op 20Hz (geverifieerd met `ros2 topic hz`).
- `/scan` (LIDAR): publisher-proces start zonder fout, maar geen data
  binnen 4s - vermoedelijk LIDAR-motor niet actief in deze bank-opstelling
  (geen softwareprobleem, verder na te kijken met de LIDAR effectief
  gemonteerd/gevoed).
- Teleop en SLAM nog niet getest.

Container `turtlebot_99` staat nog actief op de testrobot voor verder
gebruik.

## Stap 8 (vervolg) - LIDAR `/scan` fix: verkeerd LDS_MODEL (2026-09-21)

Root cause voor het ontbrekende `/scan` hierboven: de test-`.env` had
`LDS_MODEL=LDS-01` (dummy waarde), maar deze testrobot heeft fysiek een
**LDS-02**. Met LDS-01 ingesteld start `robot.launch.py` de verkeerde
driver (`hlds_laser_publisher`, voor LDS-01) i.p.v. `ld08_driver` (voor
LDS-02) - die leest wel ruwe bytes van `/dev/ttyUSB0` (bevestigd:
~25.8KB/2s via `timeout 2 cat /dev/ttyUSB0 | wc -c`), maar kan ze niet
correct parsen naar `/scan`-berichten.

Fix: processen gestopt (`pkill`/`kill -9` op robot_state_publisher,
hlds_laser_publisher/turtlebot3_ros, meerdere pogingen nodig - PID's
manueel opgezocht via `ps aux`), bringup herstart met `LDS_MODEL=LDS-02`.
Resultaat: `ld08_driver` meldt zelf `FOUND LDS-02` /
`LDS-02 started successfully`, `/scan` publiceert op ~9.8Hz
(`ros2 topic hz /scan`).

**Belangrijk voor de fleet-uitrol:** `turtlebot_config.csv` bevat al het
juiste LIDAR-model per robot (kolom `lidar`, LDS-01 voor turtlebot01-03,
LDS-02 voor turtlebot04-09) en `setup_turtlebot.sh` zet dat automatisch in
`LDS_MODEL` - dit probleem was enkel een gevolg van de dummy testwaarde
hier, geen bug in de bestaande fleet-configuratie.

## Stap 8 (vervolg) - Teleop getest (uitgevoerd, 2026-09-21)

Interactieve `ros2 run turtlebot3_teleop teleop_keyboard` is niet
bruikbaar over een niet-interactieve SSH-sessie. In plaats daarvan
rechtstreeks op `/cmd_vel` gepubliceerd (dezelfde onderliggende
mechaniek als teleop_keyboard):

```bash
# odom voor
ros2 topic echo /odom --field pose.pose.position --once
# 1.2s vooruit aan 0.05 m/s
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.05}}"   # timeout 2s
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0}}"  # expliciete stop
# odom na
ros2 topic echo /odom --field pose.pose.position --once
```

Resultaat: positie ging van `(0.176, 0.027)` naar `(0.284, 0.067)` -
~11.5cm verplaatsing, robot stopte correct na de expliciete stop-command.
Bevestigt de volledige besturingsketen (`cmd_vel` -> OpenCR -> wielen ->
odom) werkt end-to-end op Raspberry Pi OS.

Nog te doen: SLAM (`navigation2.launch.py slam:=True`), camera zodra
aangesloten.

## Stap 8 (vervolg) - SLAM getest (uitgevoerd, 2026-09-21)

```bash
ros2 launch turtlebot3_navigation2 navigation2.launch.py slam:=True use_sim_time:=False
```

Resultaat:
- Volledige nav2 lifecycle-stack activeert zonder fouten: controller_server,
  smoother_server, planner_server (GridBased/NavfnPlanner), behavior_server
  (spin/backup/drive_on_heading/wait), bt_navigator, waypoint_follower,
  velocity_smoother - allemaal "Activating" + bond met lifecycle_manager,
  geen errors in het log.
- `slam_toolbox` (sync-node) start correct: Ceres-solver (SCHUR_JACOBI
  preconditioner), registreert de LIDAR als sensor.
- `/map` (nav_msgs/OccupancyGrid) wordt gepubliceerd door `slam_toolbox`,
  correct geabonneerd door `global_costmap`. Update-rate stabiel **0.2Hz**
  (elke 5s), normaal gedrag voor een stilstaande robot.
- Map-afmetingen: 122x97 cellen, resolutie 0.05m/cel (~6,1m x 4,85m
  gebied), origin bij (-0.664, -1.092).

Niet afgerond: gedetailleerde occupancy-celstatistiek (bezet/vrij/
onbekend) via een los python-scriptje - liep vast door quoting-problemen
over geneste SSH/bash/python-aanroepen, proces manueel gestopt. Niet
essentieel, de bovenstaande resultaten bevestigen SLAM werkt end-to-end.

Nog te doen: camera zodra aangesloten. SLAM-proces staat nog actief op de
testrobot.

## Zenoh-branch samengevoegd + gecombineerde image getest (2026-09-21)

Op vraag: `zenoh`-branch gemerged in `raspios-migration` (beide repo's).
Conflicten:
- `turtlebot_docker/docker/Dockerfile`: package-lijst gecombineerd
  (`ros-humble-rmw-zenoh-cpp` toegevoegd naast bestaande packages),
  `zenoh_start_router.sh` COPY + `.bashrc`-hook behouden, camera_ros/
  libcamera-blok behouden, `ROS_DOMAIN_ID`/`LDS_MODEL` blijven
  uitgecommentarieerd (env-var uit compose i.p.v. hardcoded in image).
- `docker-compose.yaml` (beide repo's): enkel de image-tag botste
  (`:raspios` vs `:zenoh`) -> nieuwe gecombineerde tag `:raspios-zenoh`
  gebruikt, rest (RMW_IMPLEMENTATION, i2c-device, comments) was al correct
  auto-merged.

Gecombineerde image gebouwd + gepusht via de remote buildx-builder:

```bash
docker buildx build --builder rpi5 --platform linux/arm64 \
  -f docker/Dockerfile -t nobel86/turtlebot-rpi5:raspios-zenoh --push .
```

Digest: `sha256:773859d5e146624c3acd743b2cbaeeeca7bf78b2b5e48ae8ddec54ac880cc0d7`.
Build ~125s, push ~438s (grotere image door camera_ros+libcamera+zenoh
samen).

Getest op de testrobot (container `turtlebot_99` herstart met de nieuwe
image, `~/turtlebot_setup_test/docker-compose.yaml` bijgewerkt naar
`:raspios-zenoh` + `RMW_IMPLEMENTATION=rmw_zenoh_cpp`):

- **Zenoh-router**: start automatisch bij container-start (via
  `.bashrc`-hook), log toont `Started Zenoh router with id ...`, luistert
  bevestigd op `tcp/0.0.0.0:7447` (`ss -tlnp`) - de IPv4-fix uit
  `zenoh_start_router.sh` werkt zoals bedoeld.
- **Bringup**: geslaagd met `LDS_MODEL=LDS-02`, alle nodes/servers actief,
  geen fouten.
- **`/imu`**: publiceert op 20Hz via Zenoh (`ros2 topic hz`).
- **`/scan`**: publiceert op ~10.1Hz via Zenoh (vergelijkbaar met de
  ~9.8Hz eerder gemeten over CycloneDDS).
- **`ros2 topic list`**: toont alle verwachte topics.

Kanttekening (tooling, geen functioneel probleem): `timeout N ros2 topic
hz ...` over SSH/docker exec bleek niet altijd netjes af te sluiten na N
seconden onder Zenoh (SIGTERM lijkt niet altijd door te dringen tot het
onderliggende rclpy-proces) - manueel `kill -9` nodig in 2 test-runs. Iets
om rekening mee te houden bij verder scripten van tests, geen bug in de
robot-software zelf.

**Nog niet getest**: verbinding vanaf een externe laptop/student (via
`ZENOH_CONFIG_OVERRIDE` client-config, zie `zenoh-migration.md`) en
specifiek het WSL2-scenario - dat blijft de belangrijkste openstaande
verificatie.

## WSL-test + netwerkdiagnose (2026-09-21)

Jeremy heeft `turtlebot_vis` (branch `zenoh`) getest op WSL en kreeg
verbinding (`ros2 topic list` werkte, `rviz2` toonde data), maar meldde
merkbare vertraging. Diagnose op de robot:

- CPU/geheugen: geen probleem (load ~0.4 op 4 cores, nav2+slam_toolbox
  samen ~30% CPU, 1.1GB/8GB geheugen gebruikt).
- Wifi-signaal van de robot zelf: uitstekend (93/100, 270 Mbit/s, kanaal 36).
- Ping-jitter naar de robot: **4ms tot 226ms**, mdev 55ms - abnormaal hoog
  voor een sterk signaal.
- `iftop`-meting (10s): robot -> WSL-laptop (`192.168.60.245`) ~400-440
  Kbps, laptop -> robot ~20-27 Kbps - ver onder de link-capaciteit.

Conclusie: geen bandbreedteprobleem, geen CPU/geheugenprobleem op de
robot. De jitter wijst op **contentie op het gedeelde `Wifi_turtlebots`-
netwerk** (bevestigt het reeds gedocumenteerde pijnpunt van vorig jaar),
niet op iets in de Zenoh/ROS2-stack zelf. `iftop`/`nethogs` geinstalleerd
op de testrobot voor eventueel verder gebruik (let op: `/usr/sbin` zit
niet in het standaard SSH-`$PATH`, gebruik `sudo iftop ...` of het
volledige pad).

**Access points voor per-robot isolatie**: Jeremy heeft morgen 9x
TP-Link TL-WR902AC beschikbaar (consumenten-travel-router, geen VLAN-
ondersteuning, geen centraal beheer/controller-ecosysteem). Aanbevolen
config: elke unit in **Router-modus** (niet AP-modus) - ethernetpoort als
WAN-uplink naar de gedeelde switch, wifi-radio geeft een eigen NAT'te,
geisoleerde subnet per robot. Robot verbindt dan als gewone wifi-client
(geen RPi5-hotspot meer nodig). AP-modus zou i.p.v. isolatie gewoon één
plat netwerk geven, want dit toestel kent geen VLAN's. Kanalen moeten
manueel per unit verdeeld worden (geen auto-coördinatie tussen units).

**Status**: testrobot is nu afgesloten (pauze). Volgende sessie: verder
testen zodra de access points beschikbaar zijn.

## Board vervangen + CSI-camera werkend (2026-09-21)

Bij het heropstarten bleef de RPi5-LED enkel rood (geen groen/boot-
activiteit) - vermoeden van kortsluiting via de camera-aansluiting (zie
troubleshooting-advies eerder in deze sessie: stroom eraf, camera
loskoppelen, kabeltype/oriëntatie/vergrendeling controleren). Jeremy heeft
het board vervangen door een nieuwe RPi5, met dezelfde SD-kaart.

- Nieuw IP: **192.168.60.249** (was 192.168.60.69 - ander board = ander
  MAC-adres = nieuwe DHCP-lease op het gedeelde netwerk). Gevonden via
  `nmap -sn 192.168.60.0/24`.
- SD-kaart-inhoud volledig intact: Docker, de `turtlebot_99`-container
  (gestopt maar aanwezig), de buildx-builder-container - niets verloren.
- Camera aanvankelijk nog niet gedetecteerd (verwacht - firmware-niveau
  detectie bij boot, en fysieke aansluiting moest opnieuw/gecontroleerd
  worden op het nieuwe board). Na meerdere reboots + het fysiek
  controleren van de CSI-kabel (RPi5 heeft een ander/kleiner
  connectortype dan oudere Pi's - "Standard-Mini" kabel nodig, oriëntatie
  metalen contacten weg van het klepje, klepje volledig dichtklikken):
  **camera werkt.**

```
rpicam-hello --list-cameras
0 : imx708_wide [4608x2592 10-bit RGGB] (Camera Module 3 Wide, 12MP)

rpicam-still -o /tmp/test.jpg -t 2000 --width 640 --height 480
-> gelukt, /tmp/test.jpg (37KB)
```

Kleine onschuldige waarschuwing in de libcamera-log ("No static
properties available for 'imx708_wide'") - blokkeert de werking niet,
enkel dat sommige auto-tuning-parameters op defaults draaien i.p.v.
sensor-specifieke kalibratie.

I2C-shield/Grove Base Hat: nog **niet** opnieuw aangesloten/gedetecteerd
op dit nieuwe board (`i2cdetect -y -a 1` blijft leeg) - dit is een aparte,
nog openstaande fysieke aansluiting t.o.v. de camera.

Nog te doen: `camera_ros` effectief testen in de `raspios-zenoh`-container
nu de camera bevestigd werkt op host-niveau, I2C-shield heraansluiten.

## camera_ros in container: libpisp-versiemismatch gevonden en gefixt (2026-09-21)

`ros2 run camera_ros camera_node` faalde in de container met
`terminate ... what(): no cameras available`, ook al werkte de camera
prima op host-niveau (`rpicam-hello`/`rpicam-still`).

Troubleshooting-traject:
1. `pipewire`/`wireplumber` (host-desktop-mediasessie) hield
   `/dev/media0`/`/dev/media2` vast (`fuser` toonde dit) -> gestopt,
   uitgeschakeld en gemaskeerd via `systemctl --user mask` (headless
   robot heeft geen audio/camera-sessiebeheer nodig). Loste het probleem
   niet volledig op, maar is sowieso een terechte opkuis.
2. Container volledig herschapen (`docker compose down/up`) i.p.v. enkel
   herstart, voor het geval `/dev` een oude snapshot was - geen verschil.
3. Basistoegang getest (`os.open()` in python op `/dev/media0` binnen de
   container): lukt probleemloos - dus geen permissie/capability-issue.
4. Verbose libcamera-log (`LIBCAMERA_LOG_LEVELS=*:0`) toonde:
   `RPI pisp.cpp:896 Unable to acquire a CFE instance` - specifiek in de
   `rpi/pisp`-pipeline handler (de `rpi/vc4`/Unicam-fout ernaast is
   irrelevant/verwacht, RPi5 heeft geen Unicam-hardware).
5. **Root cause gevonden**: `libpisp`-versiemismatch. Host (apt-package
   `libpisp1`): **v1.7.0**. Container (automatisch opgehaalde
   meson-wrap-dependency tijdens de libcamera-build): **v1.5.0** - te oud
   voor deze (nieuwere) PiSP-hardwarerevisie.

Fix in `turtlebot_docker/docker/Dockerfile`: `libpisp` expliciet vanaf
broncode bouwen op tag `v1.7.0` (matcht host-versie), vóór de
libcamera-build, plus `--wrap-mode=nofallback` op de libcamera
meson-setup zodat een mismatch voortaan hard faalt i.p.v. stil een oude
versie te bundelen. Nieuwe build gestart via de remote buildx-builder.

**Zijnota - buildx-builder-endpoint**: na de board-vervanging (nieuw IP
192.168.60.249) moest de buildx-builder `rpi5` opnieuw aangemaakt worden
(`docker buildx create --name rpi5 ... "ssh://turtlebot@192.168.60.249"`)
- hergebruikte gelukkig dezelfde onderliggende buildkit-container.

Na de libpisp-fix (build + push, ~576s) opnieuw getest: **exact dezelfde
fout** ("Unable to acquire a CFE instance"), ook al was libpisp nu wel
degelijk 1.7.0 in de container (bevestigd via `find`). libpisp-versie was
dus niet de (volledige) oorzaak.

Verder uitgesloten via gerichte tests:
- Geen enkel proces houdt de devices vast op het moment van de poging
  (grondige `/proc/*/fd`-scan over alle processen, niet enkel `fuser`).
- `--pid=host` toegevoegd aan een losse `docker run`-test: geen verschil
  (dus geen PID-namespace-probleem).

**Root cause gevonden via web-onderzoek** (forumthread "Running rpicam
inside Docker on Raspberry Pi"): libcamera enumereert camera's via
**libudev**, en leest daarvoor de udev-database op de host
(`/run/udev/data/*`) - niet enkel de ruwe `/dev`-nodes. `privileged: true`
mount dit **niet** automatisch mee. Bevestigd: container had helemaal
geen `/run/udev` (bestond niet), terwijl de host daar exact de juiste
entries had staan (`c510:0-3` voor de media-devices).

**Fix**: `/run/udev:/run/udev:ro` toegevoegd aan `volumes:` in
`docker-compose.yaml` (beide repo's). Getest met een losse `docker run`
(werkte meteen: camera geregistreerd, stream geconfigureerd) én via de
echte compose-container. **Volledig bevestigd**: `camera_ros` start
zonder fouten, `/camera/image_raw` (+ `/camera/camera_info`,
`/camera/image_raw/compressed`) publiceren stabiel op **30fps**.

Enige restwaarschuwing (cosmetisch, geen blocker): ontbrekend
camera-kalibratiebestand (`.yaml`) - gebruikt gewoon defaults, kan later
aangemaakt worden via een standaard ROS2-camera-kalibratieprocedure indien
gewenst.

## WSL: camera-feed bekijken + latency bevestigd opgelost via compressed transport (2026-09-21)

Board vervangen -> nieuw IP **192.168.60.249** (was .69) - `turtlebot_vis`
`.env` (`ROBOT_ZENOH_IP`) moet hierop aangepast worden bij elke test na
een board/IP-wissel.

Volledige stack herstart en getest zichtbaar in WSL:
- `/camera/image_raw` gebruiken in rviz2 gaf weinig te zien: normaal, want
  `/camera/image_raw/compressed` (CompressedImage) rechtstreeks als
  Image-display-topic selecteren werkt niet (verkeerd berichttype) - je
  moet het basistopic `/camera/image_raw` kiezen en de transport-hint op
  `compressed` zetten.
- rviz2 toonde `compressed` niet als optie in de transport-dropdown, ook
  al bevestigde de gebruiker dat `compressed_image_transport` wel
  degelijk geinstalleerd is en het topic met data zichtbaar is via CLI
  (`ros2 topic list`/`echo`) - dus een rviz2-specifiek
  plugin-discovery-probleem (pluginlib), geen ROS-graph/Zenoh-probleem.
- **Workaround/alternatief dat wel meteen werkte**: `ros2 run
  rqt_image_view rqt_image_view`, compressed topic gekozen -> "heel
  responsief". Bevestigt de latency-diagnose: raw (800x600 XRGB8888,
  ~58MB/s bij 30fps) was de bottleneck, niet Zenoh/wifi zelf. Voor het
  puur bekijken van de camera-feed is dit een prima werkende oplossing;
  het rviz2-dropdown-issue is nog niet verder uitgezocht (lage
  prioriteit, rqt_image_view volstaat).

**Opgelost - root cause was tóch een ontbrekend package**:
`osrf/ros:humble-desktop-full` (de basis-image van `turtlebot_vis`) bevat,
in tegenstelling tot de aanname eerder in dit logboek, **geen**
`compressed_image_transport` standaard. Manueel geinstalleerd in de
container:

```bash
sudo apt install ros-$ROS_DISTRO-compressed-image-transport
```

Na deze installatie werkte het topic manueel intypen in rviz2's
Image-display Topic-veld (de dropdown zelf blijft de optie niet
automatisch tonen - dat blijft een apart, lager-prioriteit UI-issue).

**Permanente fix**: `ros-humble-compressed-image-transport` toegevoegd
aan `turtlebot_vis/docker/Dockerfile` (branch `zenoh`), zodat dit niet
telkens manueel herhaald moet worden bij een nieuwe/verse container of
door andere studenten. **Camera-feed werkt nu volledig in rviz2 vanuit
WSL, via compressed transport.**

(Nvm eerdere aanname in dit logboek dat `rqt_image_view` bewees dat het
package al aanwezig was - dat blijkt achteraf niet correct; mogelijk
gebruikt rqt_image_view een ander decodeerpad voor CompressedImage dan
rviz2's Image-display, wat verklaart waarom het daar wel werkte zonder
het package.)

## Camera-bandbreedte getuned + permanent gemaakt (2026-09-21)

Gemeten bandbreedte (via `iftop` op de robot, robot -> WSL-laptop) bij
standaardinstellingen van `camera_ros` (800x600 auto, `jpeg_quality=95`,
30fps): **~23-26 Mbit/s**. Stapsgewijs getuned en telkens gemeten:

| Stap | Instelling | Bandbreedte |
|---|---|---|
| 0 (start) | 800x600, kwaliteit 95, 30fps | ~23-26 Mbit/s |
| 1 | + kwaliteit 60 | ~4,6-5,3 Mbit/s |
| 2 | + 640x480, 15fps | **~1,3-1,5 Mbit/s** |

Totale reductie: ~17-20x. `width`/`height` zijn **read-only** tijdens het
draaien van de node (`ros2 param set` faalt daarop) - vereist een
herstart van `camera_node` met de nieuwe waarden. `jpeg_quality` en
`FrameDurationLimits` (framerate, in microseconden - 66667us = 15fps) zijn
wel live aanpasbaar.

**Permanent gemaakt**: nieuw bestand `turtlebot_docker/camera_params.yaml`
(zelfde patroon als `cyclonedds_config.xml`), gekopieerd in de image via
de Dockerfile naar `/root/turtlebot3_ws/camera_params.yaml`. Starten met:
```bash
ros2 run camera_ros camera_node --ros-args --params-file /root/turtlebot3_ws/camera_params.yaml
```
Getest en bevestigd: 640x480, 15fps (exact), geen fouten.

**Zijnoot - camera fysiek gewisseld tijdens het testen**: gebruiker
wisselde kort naar een ander/goedkoper cameramodule-type, wat een
"Failed to start streaming: Input/output error" gaf bij het starten van
`camera_node` (logisch, andere/niet-ondersteunde sensor). Na terugplaatsen
van de originele imx708-module: `rpicam-hello --list-cameras` toonde
meteen weer normale (niet-sentinel) crop-waarden, en `camera_node` startte
zonder problemen - geen reboot nodig deze keer (in tegenstelling tot de
eerdere board-vervangingssessie).

## Camera optioneel gemaakt + turtlebot09 MAC bijgewerkt (2026-09-21)

- Nieuw: `ENABLE_CAMERA`-omgevingsvariabele + `turtlebot_docker/docker/
  camera_start.sh` (zelfde patroon als `zenoh_start_router.sh`) - start
  `camera_node` automatisch bij shell-start, enkel als `ENABLE_CAMERA=true`.
  Nieuwe `camera`-kolom in `turtlebot_config.csv` (overal `false` - per
  robot aan te passen). Live getest in de container (`docker cp`, niet
  herbouwd/gepusht naar Docker Hub): beide standen werken correct, incl.
  idempotent gedrag bij een tweede aanroep.
- **Kanttekening tijdens het testen**: `pgrep -f camera_node` bleek
  zichzelf te matchen wanneer ik het los testte via
  `bash -c "pgrep -fa camera_node"` (de wrapper-string zelf bevat de
  zoekterm). Dit is geen bug in het eigenlijke script (dat wordt als
  bestand aangeroepen, niet als inline-string, dus geen zelf-match daar),
  maar de `[c]amera_node`-bracket-trick is defensief toegevoegd in
  `camera_start.sh` voor de zekerheid.
- **turtlebot09 MAC-adres bijgewerkt**: het board dat eerder sneuvelde
  (rode LED, vermoede kortsluiting) is vervangen; nieuw board MAC
  `88:A2:9E:2C:EA:4D`. Bijgewerkt in `turtlebot_config.csv` en effectief
  getest via `setup_turtlebot.sh` op het board zelf: correct herkend als
  turtlebot09 (ROS_DOMAIN_ID=9, LDS-02, hostname + Avahi correct
  bijgewerkt).

## Volledige image herbouwd + end-to-end automatische camera-start bevestigd (2026-09-21)

`turtlebot_config.csv`: `camera=true` gezet voor turtlebot09 (bevestigd
camera fysiek aanwezig). Volledige image herbouwd/gepusht via de remote
buildx-builder (build-cache bleek niet hergebruikt - volledige ~10 min
build + ~10 min push, geen snelle incrementele build zoals gehoopt).

Bij het testen op de robot bleek de lokale test-`docker-compose.yaml` op
`~/turtlebot_setup_test/` verouderd (miste de `ENABLE_CAMERA`-regel - die
was lokaal wel toegevoegd/gepusht naar git, maar nooit naar de robot's
testmap gekopieerd). Rechtgezet door het bestand opnieuw te scp'en.

Na `docker compose down/up` met de nieuwe image + correcte compose +
`.env` (`ENABLE_CAMERA=true`): **`camera_node` startte volledig
automatisch op** (geen `docker exec`/manuele tussenkomst meer nodig),
`/camera/image_raw/compressed` publiceert stabiel op 15fps - exact de
getunede instellingen. Dit bevestigt de volledige `ENABLE_CAMERA`-feature
werkt end-to-end vanuit de gebakken image.

## Per-robot statuspagina toegevoegd (2026-09-21)

`turtlebot_monitor` (apart repo) bekeken op vraag - bleek nooit volledig
afgewerkt (placeholder launch-commando in `docker-compose.yaml`), had een
verouderd MAC-adres voor turtlebot09, en is architecturaal onverenigbaar
met de geplande per-robot access points (nmap-scan van één gedeeld
subnet). README toegevoegd aan dat repo met deze bevindingen.

I.p.v. daaraan verder te bouwen: nieuwe, eenvoudigere aanpak in
`turtlebot_docker` - geïnspireerd op `JeremyLebon/robot`'s
`components/robot_web` en iRobot Create3's ingebouwde statuspagina.
`rosbridge_server` (websocket, poort 9090) + een statische HTML/roslibjs-
pagina (poort 8080), rechtstreeks per robot, geen domain_bridge/nmap
nodig - dus geen last van de AP-isolatie.

Live getest in de container (apt install + docker cp, nog niet in de
gepushte image): echte WebSocket-handshake bevestigd (HTTP 101), en
effectieve data ontvangen via rosbridge - `/battery_state` (12.08V,
87.8%) en `/scan` (226 ranges). Gecommit + gepusht naar
`raspios-migration`, **nog niet herbouwd/gepusht naar Docker Hub** - een
volgende volledige rebuild neemt dit mee.

## Teleop + systeeminfo toegevoegd aan de statuspagina (2026-09-21)

Op vraag: teleop-bediening (D-pad + snelheidsslider + pijltjestoetsen,
publiceert op `/cmd_vel`) en een systeeminfo-paneel (IP, MAC, CPU-load,
geheugen, uptime) toegevoegd aan de statuspagina.

Systeeminfo (IP/MAC/CPU/geheugen) is geen standaard ROS-topic, dus nieuw
klein stdlib-only nodetje `system_info_node.py` toegevoegd (geen psutil
nodig - `os.getloadavg()`, `/proc/meminfo`, `/proc/uptime`, SIOCGIFADDR-
ioctl voor het IP). Publiceert JSON op `/system_info` (std_msgs/String),
elke 2s.

Live getest via rosbridge (zelfde protocol als de webpagina gebruikt):
- `/system_info`: correcte data ontvangen (`hostname: turtlebot09,
  ip: 192.168.60.249, mac: 88:A2:9E:2C:EA:4D, cpu_load_1min: 0.55,
  mem_percent: 10.6, uptime_seconds: 2517`).
- `/cmd_vel`: twist-reeks verstuurd via rosbridge-publish (dezelfde
  publicatiemethode als de teleop-knoppen), gevolgd door expliciete stop.

Gecommit + gepusht, nog niet herbouwd naar Docker Hub (idem als de
statuspagina zelf).
