# Migratie: Ubuntu -> Raspberry Pi OS (RPi5 turtlebots)

Doel: een nieuwe golden image bouwen op **Raspberry Pi OS Lite (64-bit)**
i.p.v. Ubuntu, met werkende I2C en de CSI-camera (via `camera_ros`/`libcamera`)
i.p.v. de USB-webcam. De bestaande Ubuntu-fleet (9 robots, branch `main` van
deze repo en van `turtlebot_docker`) blijft ongewijzigd tot dit gevalideerd is.

> Op de eerste testrobot (RPi5, `192.168.60.69`) is dit Debian 13 (trixie) -
> Raspberry Pi OS is intussen van Bookworm naar trixie geëvolueerd. Het pad
> `/boot/firmware/config.txt` en de rest van deze gids blijven hetzelfde;
> gebruik gewoon de meest recente Raspberry Pi Imager, welke Debian-basis
> die ook aflevert.

Test dit eerst op **1 losse RPi5/turtlebot**, niet op de volledige fleet.
Zie `raspios-migration-log.md` in deze map voor het logboek van wat er
effectief al is uitgevoerd op de testrobot.

## 1. Raspberry Pi OS flashen

- Raspberry Pi Imager gebruiken, OS: "Raspberry Pi OS Lite (64-bit)".
- In de Imager-instellingen (tandwiel-icoon): hostname, user (bv. `turtlebot-rpi5`),
  wifi (voor eerste setup) en SSH inschakelen.
- Opstarten, inloggen via SSH.

## 2. I2C inschakelen

```bash
sudo raspi-config nonint do_i2c 0
# of manueel in /boot/firmware/config.txt:
#   dtparam=i2c_arm=on
sudo reboot
```

Controle na reboot:
```bash
ls /dev/i2c-1
sudo apt-get install -y i2c-tools
i2cdetect -y 1
```

Op de testrobot stond dit al aan (recente Raspberry Pi Imager zet
`dtparam=i2c_arm=on` en `camera_auto_detect=1` standaard in config.txt) -
controleer dit dus eerst voor je het manueel toevoegt.

## 3. Camera - sanity check op OS-niveau (vóór Docker)

Raspberry Pi OS heeft `rpicam-apps` standaard aan boord. Test dit eerst
rechtstreeks op de host, los van Docker/ROS2:

```bash
rpicam-hello --list-cameras
rpicam-hello -t 2000
```

Als dit hier al niet werkt, heeft verder gaan met `camera_ros` in de
container geen zin - eerst hardware/kabel/aansluiting controleren.

## 4. Docker installeren

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# opnieuw inloggen zodat de docker-group actief is
```

Compose-plugin zit al mee met `get-docker.sh`. Controleren:
```bash
docker compose version
```

## 5. Repo's clonen (branch `raspios-migration`)

```bash
git clone -b raspios-migration https://github.com/JeremyLebon/turtlebot_docker.git
git clone -b raspios-migration https://github.com/JeremyLebon/turtlebot_setup.git
```

(Deze branches staan lokaal klaar op de ontwikkelmachine - eerst pushen naar
GitHub voordat je ze op de RPi5 kan clonen, of rechtstreeks `scp`/`rsync`
gebruiken voor de eerste test.)

## 6. Image bouwen onder een nieuwe tag

Belangrijk: gebruik de tag `:raspios-zenoh` (deze branch bevat ondertussen
zowel de RPi OS- als de Zenoh-migratie, samengevoegd), **niet** `:latest`,
zodat de bestaande Ubuntu-fleet (die `:latest` pullt) niet per ongeluk een
niet-geteste image binnenkrijgt.

Bouw dit **niet** rechtstreeks op de RPi5 (te traag) en ook niet via de
gewone x86-buildx uit de hoofd-README (QEMU-emulatie is traag voor de
`libcamera`-build hieronder). Gebruik i.p.v. daarvan een remote buildx-builder
die vanaf de laptop getriggerd wordt maar native op de RPi5 compileert - zie
"Native arm64 build via a remote builder on the RPi5" in
`turtlebot_docker/README.md`. Kort samengevat:

```bash
ssh-copy-id turtlebot@<robot-ip>   # eenmalig, passwordless SSH
docker buildx create --name rpi5 --driver docker-container \
  --platform linux/arm64 "ssh://turtlebot@<robot-ip>"
docker buildx inspect rpi5 --bootstrap

cd turtlebot_docker
docker buildx build --builder rpi5 --platform linux/arm64 \
  -f docker/Dockerfile -t nobel86/turtlebot-rpi5:raspios --push .
```

De `camera_ros`/`libcamera`-build in de Dockerfile is het meest
hardware-gevoelige stuk (zie commentaar in `docker/Dockerfile`). Verwacht
hier iteratie: package- of tagversies bijstellen tot de build slaagt en de
camera op deze specifieke RPi5 + module werkt.

## 7. Systemd-unit installeren

Vandaag wordt `setup_turtlebot.sh` manueel gedraaid na het flashen. Met
Raspberry Pi OS voegen we een systemd-unit toe zodat dit automatisch bij
elke boot gebeurt:

```bash
sudo cp turtlebot_setup/setup_turtlebot.sh /usr/local/bin/setup_turtlebot.sh
sudo chmod +x /usr/local/bin/setup_turtlebot.sh
sudo mkdir -p /home/turtlebot-rpi5/turtlebot_setup
sudo cp turtlebot_setup/turtlebot_config.csv /home/turtlebot-rpi5/turtlebot_setup/
sudo cp turtlebot_setup/systemd/turtlebot-setup.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now turtlebot-setup.service
```

Test eerst manueel (`sudo /usr/local/bin/setup_turtlebot.sh`), controleer de
output, en test dan pas met een reboot of de service automatisch aanslaat.

## 8. Volledige stack testen

```bash
cd turtlebot_setup
docker compose pull
docker compose up -d
```

**`up -d` (achtergrond) vs. `up` (voorgrond) - belangrijk voor studenten:**
met `docker compose up` zonder `-d` hangt de container vast aan je
SSH-sessie/terminal. Valt je wifi/SSH-verbinding weg, krijgt dat
voorgrond-proces een signaal en sluit `docker compose` de containers
**netjes af** - niet enkel je zicht erop verdwijnt, de hele stack
(bringup, Zenoh, camera) stopt dan mee. Met `-d` staat de container los
van je SSH-sessie en overleeft een wegvallende verbinding probleemloos.
Om toch live logs te zien: `docker compose logs -f` (kan gewoon gestopt
worden met Ctrl+C zonder de container te raken), of draai `docker compose
up` (voorgrond) binnenin een `tmux`/`screen`-sessie op de robot als je
echt de voorgrond-ervaring wil met behoud van robuustheid tegen
verbindingsonderbrekingen.

**Let op na een reboot/stroomonderbreking**: de container heeft
momenteel geen restart-policy (bewuste keuze - studenten leren zo zelf
Docker (her)starten). Na een reboot moet dus manueel opnieuw
`docker compose up -d` gedraaid worden.

In de container:
```bash
ros2 launch turtlebot3_bringup robot.launch.py
```

Camera: automatisch via `ENABLE_CAMERA=true` in `.env`/`turtlebot_config.csv`
(zie `camera_start.sh` in `turtlebot_docker`) - geen manueel commando meer
nodig. Om zelf te testen:
```bash
ros2 topic echo /camera/image_raw --no-arr   # of rqt_image_view vanaf een laptop
```

`camera_params.yaml` (staat al in de image, zie `turtlebot_docker/camera_params.yaml`)
zet resolutie/framerate/JPEG-kwaliteit bewust laag (640x480, 15fps,
kwaliteit 60) om de bandbreedte van de gecomprimeerde stream binnen de
wifi-budget te houden - standaardinstellingen (800x600 auto, kwaliteit
95, 30fps) mat ~23-26 Mbit/s op echte hardware, deze instellingen ~1,3-1,5
Mbit/s (~17-20x minder). Belangrijk: `width`/`height` zijn read-only
tijdens het draaien - wijzigingen daarvan vereisen een herstart van
`camera_node` (niet enkel `ros2 param set`). Niet elke robot heeft een
camera - `ENABLE_CAMERA` staat per robot in `turtlebot_config.csv`.

Statuspagina (draait automatisch, geen commando nodig): open
`http://<robot-ip>:8080` in een browser voor een live overzicht
(batterij, lidar, IMU, odometrie, camera) - werkt volledig offline, geen
internet nodig. Zie `turtlebot_docker/status_page/`.

I2C (vanuit de container, als er I2C-peripherals aangesloten zijn):
```bash
i2cdetect -y 1
```

Rest van de smoke-test zoals in de bestaande `turtlebot_docker/README.md`:
teleop, SLAM (`navigation2.launch.py slam:=True`), navigatie.

## 9. Nieuwe golden image maken

Pas nadat stap 8 volledig werkt:

```bash
lsblk
sudo dd if=/dev/mmcblk0 of=~/rpi5_turtlebot_raspios_v1.img status=progress
```

De bestaande Ubuntu-images (`rpi5_turtlebot_V2_shrunk.img` e.a.) blijven
staan als fallback.

## 10. Uitrol

Pas uitrollen naar de overige turtlebots nadat dit op minstens 1, liefst 2,
fysieke robots gevalideerd is (camera, I2C, LIDAR, teleop, SLAM, en een
volledige boot-cyclus met de systemd-unit).
