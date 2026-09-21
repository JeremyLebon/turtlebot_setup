# Migratie: CycloneDDS -> Zenoh (rmw_zenoh_cpp)

Doel: `RMW_IMPLEMENTATION` omschakelen van `rmw_cyclonedds_cpp` naar
`rmw_zenoh_cpp`. DDS werkt op zich ook via WSL2 (zie
`turtlebot_docker/README.md` voor de context), maar de
multicast-discovery-mechanica van DDS brengt merkbaar veel
netwerk-overhead met zich mee - zeker relevant op een gedeelde/beperkte
wifi-verbinding met meerdere robots/studenten tegelijk (zie ook het
wifi-congestieprobleem van vorig jaar). Zenoh in client-modus (unicast TCP
naar een vaste router-endpoint, geen multicast-scouting nodig) is hier
lichter. Deze migratie staat los van de
Raspberry Pi OS-migratie (`raspios-migration`-branch) - werkt op de huidige
Ubuntu-fleet, geen RPi5-hardwarewijzigingen nodig.

Branch: `zenoh`, in zowel `turtlebot_docker` als `turtlebot_setup`,
afgeleid van `master`.

## Waarom niet gewoon `ZENOH_ROUTER_URI` zoals in `robot`?

In `JeremyLebon/robot` (`core/ros_entrypoint.bash`) staat een gedeeltelijke
Zenoh-opzet: die checkt of `ZENOH_ROUTER_URI` gezet is, maar gebruikt die
waarde nergens om de zenoh-sessie effectief te configureren - er wordt geen
config-bestand geschreven en geen `ZENOH_SESSION_CONFIG_URI`/
`ZENOH_CONFIG_OVERRIDE` gezet op basis daarvan. Die env var is dus
gedocumenteerd maar niet aangesloten; bruikbaar binnen 1 host (multicast
binnen de container/host werkt), maar lost het cross-host/WSL2-probleem
niet op zoals het er nu staat.

Voor deze migratie is daarom rechtstreeks de officiële, wel-gedocumenteerde
`rmw_zenoh_cpp`-configuratie gebruikt (geverifieerd via de
`ros2/rmw_zenoh`-documentatie):

- `ZENOH_SESSION_CONFIG_URI` - pad naar een JSON5-configbestand voor de
  zenoh-sessie.
- `ZENOH_CONFIG_OVERRIDE` - simpelere one-liner om configvelden te
  overschrijven zonder apart bestand (dit is wat we hier gebruiken).
- Bundled router starten: `ros2 run rmw_zenoh_cpp rmw_zenohd`.

**Belangrijke valkuil (bevestigd via de officiële docs):** de standaard
routerconfig luistert op `tcp/[::]:7447` (IPv6 ANY) en **crasht op
IPv4-only systemen** - en de turtlebot-netwerken (nmcli hotspot/wlan0) zijn
IPv4-only. Vandaar de expliciete `ZENOH_CONFIG_OVERRIDE` met
`tcp/0.0.0.0:7447` in `docker/zenoh_start_router.sh`.

## Wat is aangepast

### `turtlebot_docker` (branch `zenoh`)
- `docker/Dockerfile`: `ros-humble-rmw-zenoh-cpp` toegevoegd (naast de
  bestaande `ros-humble-rmw-cyclonedds-cpp`, die blijft staan als fallback).
  Nieuw bestand `docker/zenoh_start_router.sh` wordt gekopieerd naar
  `/usr/local/bin/` en bij shell-start (via `.bashrc`) uitgevoerd: start
  éénmalig een lokale `rmw_zenohd`-router op `tcp/0.0.0.0:7447`, enkel als
  `RMW_IMPLEMENTATION=rmw_zenoh_cpp` en er nog geen router draait.
- `docker-compose.yaml`: `RMW_IMPLEMENTATION` default naar `rmw_zenoh_cpp`
  (cyclonedds-regel staat in commentaar voor snelle rollback). Image-tag
  `nobel86/turtlebot-rpi5:zenoh` i.p.v. `:latest`.

### `turtlebot_setup` (branch `zenoh`)
- `docker-compose.yaml`: zelfde `RMW_IMPLEMENTATION`-wissel, image-tag
  `:zenoh`. `network_mode: host` staat al aan, dus poort 7447 is meteen
  bereikbaar op het robot-IP - geen extra `ports:` nodig.
- `setup_turtlebot.sh` / `turtlebot_config.csv`: **ongewijzigd**.
  `ROS_DOMAIN_ID` blijft gewoon per robot ingesteld zoals vandaag (Zenoh
  gebruikt dit nog steeds om topics te scopen), en is met de per-robot-AP
  aanpak eerder een extra veiligheidslaag dan de enige isolatie.

## Aan de studentenkant (laptop / WSL)

Op de laptop die met de wifi/AP van een specifieke turtlebot verbindt
(robot-IP = de gateway van die AP, bv. `10.42.0.1`):

```bash
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
export ZENOH_CONFIG_OVERRIDE='mode="client";connect/endpoints=["tcp/10.42.0.1:7447"]'

ros2 topic list   # zou nu de topics van die robot moeten tonen
```

Dit forceert de zenoh-sessie in "client"-modus die rechtstreeks (unicast
TCP) naar de robot's router verbindt, i.p.v. te vertrouwen op
multicast-scouting - werkt door WSL2's virtuele netwerk heen met veel
minder overhead dan DDS-multicast-discovery.

## Testen

1. Image bouwen op de `zenoh`-branch (zelfde remote-buildx-aanpak als bij
   raspios, of gewoon de bestaande x86-buildx-workflow uit de README - deze
   Dockerfile heeft geen zware from-source build zoals libcamera, dus
   cross-build via QEMU is hier geen probleem):
   ```bash
   docker buildx build --platform linux/arm64 -f docker/Dockerfile \
     -t nobel86/turtlebot-rpi5:zenoh --push .
   ```
2. Op de robot: `docker compose up`, dan in de container controleren dat de
   router gestart is: `cat /tmp/rmw_zenohd.log`, `pgrep -fa rmw_zenohd`.
3. Vanaf een laptop verbonden met die robot's wifi: bovenstaande
   client-config zetten, `ros2 topic list` / `ros2 topic echo` testen.
4. Specifiek het WSL2-scenario testen, met `turtlebot_vis` (branch
   `zenoh`) - dat kon ik hier niet zelf testen, geen WSL/Windows-client
   beschikbaar. Dit is de belangrijkste nog openstaande verificatie.

## Status

- `zenoh`-branch samengevoegd in `raspios-migration` (beide repo's,
  gecommit + gepusht naar GitHub).
- Gecombineerde image `nobel86/turtlebot-rpi5:raspios-zenoh` gebouwd en
  getest op de testrobot: router start automatisch, luistert correct op
  `tcp/0.0.0.0:7447`, `/imu` (20Hz) en `/scan` (~10Hz) bevestigd werkend
  via Zenoh (zie `raspios-migration-log.md`).
- `turtlebot_vis` (branch `zenoh`) aangepast met de bijhorende
  client-config, klaar om te testen.
- Nog open: stap 4 hierboven (het effectieve WSL2-scenario, door Jeremy
  zelf uit te voeren).
