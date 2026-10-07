#!/bin/bash
# Voorbereiden van de bouwrobot (turtlebot09) vlak voor het inlezen van zijn
# SD-kaart als golden image. Daarna: robot uitschakelen, kaart inlezen met
# sdclone.sh (laptop). Zie docs/todo.md, "Uitrolmethode: SD-kaart klonen".
#
#   sudo ~/turtlebot_setup/tools/golden_prepare.sh
set -eu

SETUP_DIR=/home/turtlebot/turtlebot_setup
[ "$(id -u)" = 0 ] || { echo "Start met sudo."; exit 1; }

echo "🔄 Systeem bijwerken (apt full-upgrade)..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -q
apt-get full-upgrade -y -q -o Dpkg::Options::=--force-confold
apt-get autoremove -y -q
apt-get clean

echo "🔄 Repo + Docker-image bijwerken..."
runuser -u turtlebot -- git -C "$SETUP_DIR" pull --ff-only
docker compose --project-directory "$SETUP_DIR" pull
docker image prune -f >/dev/null

# Stempel: zichtbaar op de statuspagina van elke kloon (host_info.json).
# Volgnummer: teller op de bouwrobot (v1 = eerste kloon naar turtlebot06,
# 2026-10-07).
COUNTER=/var/lib/turtlebot-setup/golden-count
N=$(( $(cat "$COUNTER" 2>/dev/null || echo 1) + 1 ))
mkdir -p "$(dirname "$COUNTER")" && echo "$N" > "$COUNTER"
STAMP="golden v$N - $(date '+%F %H:%M') - van $(hostname), setup $(runuser -u turtlebot -- git -C "$SETUP_DIR" log -1 --format=%h)"
echo "$STAMP" > /etc/turtlebot-golden
echo "🏷️  $STAMP"

# Opkuisen: niets persoonlijks/tijdelijks meeklonen. De robot-specifieke
# rest (machine-id, SSH-keys, wifi, .env, state/) regelt setup_turtlebot.sh
# op elke kloon zelf.
rm -f /home/turtlebot/.bash_history /root/.bash_history
rm -f "$SETUP_DIR"/state/camera_enabled "$SETUP_DIR"/state/container_starts
rm -rf /tmp/* 2>/dev/null || true
journalctl --vacuum-time=1s >/dev/null 2>&1 || true

echo "✅ Klaar. Schakel de robot nu uit (statuspagina of 'sudo poweroff')"
echo "   en lees de kaart in met: sudo bash ~/turtlebot_clone/sdclone.sh read /dev/mmcblk0"
