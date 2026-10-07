#!/bin/bash
# /usr/local/bin/setup_turtlebot.sh
#
# Per-robot configuratie, bij elke boot uitgevoerd door
# turtlebot-setup.service (als root). De robot wordt herkend aan het
# MAC-adres van wlan0 via turtlebot_config.csv. Zo kan één SD-kaart
# (golden image) naar alle robots gekloond worden: dit script maakt er bij
# de eerste boot op een ander bord een turtlebot<nr> van.
#
# Idempotent: doet enkel iets als er effectief iets verschilt.

set -u

SETUP_USER="turtlebot"
SETUP_DIR="${SETUP_DIR:-/home/$SETUP_USER/turtlebot_setup}"   # clone van turtlebot_setup
CONFIG_FILE="${CONFIG_FILE:-$SETUP_DIR/turtlebot_config.csv}"
NET_IFACE="wlan0"
STATE_DIR="/var/lib/turtlebot-setup"

# Lees MAC-adres
MAC=$(tr '[:lower:]' '[:upper:]' < /sys/class/net/$NET_IFACE/address)

# Zoek configuratie
LINE=$(grep -i ",$MAC," "$CONFIG_FILE")

if [ -z "$LINE" ]; then
  echo "⚠️ Geen match gevonden voor MAC $MAC in $CONFIG_FILE"
  exit 1
fi

# Parse CSV (nr,mac,hostname,ros_domain_id,lidar,camera)
IFS=',' read -r NR CSV_MAC HOSTNAME ROS_DOMAIN_ID LIDAR CAMERA <<< "$LINE"
CAMERA=$(echo "${CAMERA:-false}" | tr -d '[:space:]')
NR2=$(printf '%02d' "$NR")

echo "✅ Instellingen gevonden voor $HOSTNAME (nr $NR, ROS_DOMAIN_ID=$ROS_DOMAIN_ID)"

# --- Unieke identiteit na het klonen --------------------------------------
# Een gekloonde kaart heeft dezelfde machine-id (DHCP-client-ID) en SSH-
# host-keys als het origineel. Eenmalig per MAC-adres opnieuw genereren;
# daarna een reboot zodat alle services de nieuwe machine-id gebruiken.
REBOOT_NEEDED=false
mkdir -p "$STATE_DIR"
IDENTITY_MARKER="$STATE_DIR/identity-$(echo "$MAC" | tr -d ':')"
if [ ! -f "$IDENTITY_MARKER" ]; then
  echo "🔑 Nieuw bord ($MAC): machine-id en SSH-host-keys opnieuw genereren"
  rm -f "$STATE_DIR"/identity-*
  rm -f /etc/machine-id
  systemd-machine-id-setup
  rm -f /etc/ssh/ssh_host_*
  ssh-keygen -A
  touch "$IDENTITY_MARKER"
  REBOOT_NEEDED=true
fi

# --- Hostname ----------------------------------------------------------------
if [ "$(hostname)" != "$HOSTNAME" ]; then
  hostnamectl set-hostname "$HOSTNAME"
  echo "✅ Hostname ingesteld op $HOSTNAME"
fi
# /etc/hosts mee aanpassen, anders kan sudo de hostname niet herleiden
# (wacht dan telkens op een DNS-timeout).
if grep -q '^127\.0\.1\.1' /etc/hosts; then
  sed -i "s/^127\.0\.1\.1\s.*/127.0.1.1\t\t$HOSTNAME/" /etc/hosts
else
  printf '127.0.1.1\t\t%s\n' "$HOSTNAME" >> /etc/hosts
fi

# Avahi herstarten zodat de nieuwe hostname meteen zichtbaar is via .local
if systemctl list-unit-files | grep -q avahi-daemon.service; then
  systemctl restart avahi-daemon
else
  echo "⚠️ Avahi-daemon niet gevonden — controleer of Avahi is geïnstalleerd."
fi

# --- Wifi: eigen access point TB-AP-<nr> -------------------------------------
# Zie docs/ap-migration.md. Profielen van andere robots (bv. TB-AP-09 op een
# kloon van turtlebot09) worden verwijderd.
AP_NAME="TB-AP-$NR2"
AP_PSK="TurtleBot@P$NR2"
for con in $(nmcli -t -f NAME connection show | grep '^TB-AP-'); do
  if [ "$con" != "$AP_NAME" ]; then
    nmcli connection delete "$con" && echo "🗑️ Wifi-profiel $con verwijderd"
  fi
done
if ! nmcli -t -f NAME connection show | grep -qx "$AP_NAME"; then
  nmcli connection add type wifi ifname "$NET_IFACE" con-name "$AP_NAME" \
    ssid "$AP_NAME" wifi-sec.key-mgmt wpa-psk wifi-sec.psk "$AP_PSK" \
    connection.autoconnect yes connection.autoconnect-priority 100 \
    && echo "✅ Wifi-profiel $AP_NAME aangemaakt"
  # Mag mislukken (AP nog niet geconfigureerd/buiten bereik): autoconnect
  # probeert het later opnieuw.
  nmcli --wait 20 connection up "$AP_NAME" >/dev/null 2>&1 \
    || echo "⚠️ $AP_NAME (nog) niet bereikbaar"
fi

# --- Omgevingsvariabelen -----------------------------------------------------
# .env naast docker-compose.yaml: die leest Docker Compose zelf, ook bij een
# automatische herstart (profile.d enkel bij een interactieve login).
ENV_CONTENT="TURTLEBOT_NR=$NR
ROS_DOMAIN_ID=$ROS_DOMAIN_ID
LDS_MODEL=$LIDAR
ENABLE_CAMERA=$CAMERA"

cat > /etc/profile.d/turtlebot_config.sh <<EOF
export TURTLEBOT_NR=$NR
export ROS_DOMAIN_ID=$ROS_DOMAIN_ID
export LDS_MODEL=$LIDAR
export ENABLE_CAMERA=$CAMERA
EOF

ENV_FILE="$SETUP_DIR/.env"
if [ -d "$SETUP_DIR" ]; then
  if [ ! -f "$ENV_FILE" ] || [ "$(cat "$ENV_FILE")" != "$ENV_CONTENT" ]; then
    echo "$ENV_CONTENT" > "$ENV_FILE"
    chown "$SETUP_USER:$SETUP_USER" "$ENV_FILE"
    # Vlag i.p.v. variabele: overleeft de identiteits-reboot hieronder
    touch "$STATE_DIR/compose-pending"
    echo "✅ $ENV_FILE bijgewerkt (nr $NR, lidar $LIDAR, camera $CAMERA)"
  fi
else
  echo "⚠️ $SETUP_DIR bestaat niet — geen .env geschreven"
fi

if [ "$REBOOT_NEEDED" = true ]; then
  echo "🔄 Herstarten om de nieuwe identiteit te activeren..."
  systemctl --no-block reboot
  exit 0
fi

# --- Container ---------------------------------------------------------------
# Enkel na een gewijzigde .env (bv. eerste boot van een kloon, die nog de
# container van de originele robot heeft). Anders zorgt
# restart: unless-stopped er zelf voor.
if [ -f "$STATE_DIR/compose-pending" ] && [ -f "$SETUP_DIR/docker-compose.yaml" ]; then
  # Container(s) met een ander nummer (kloon van een andere robot) of uit een
  # andere compose-map (bv. het oude ~/turtlebot_setup_test) opruimen
  for c in $(docker ps -a --format '{{.Names}}' | grep '^turtlebot_[0-9]*$'); do
    dir=$(docker inspect "$c" --format '{{index .Config.Labels "com.docker.compose.project.working_dir"}}')
    if [ "$c" != "turtlebot_$NR" ] || [ "$dir" != "$SETUP_DIR" ]; then
      docker rm -f "$c" && echo "🗑️ Container $c verwijderd"
    fi
  done
  docker compose --project-directory "$SETUP_DIR" up -d \
    && rm -f "$STATE_DIR/compose-pending" \
    && echo "✅ Container turtlebot_$NR gestart"
fi

echo "🎉 TurtleBot setup voltooid!"
