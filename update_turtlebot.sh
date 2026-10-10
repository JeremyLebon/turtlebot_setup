#!/bin/bash
# ~/turtlebot_setup/update_turtlebot.sh - uitgevoerd door
# turtlebot-update.service (als root): repo bijwerken, nieuwste image
# ophalen en de container enkel opnieuw aanmaken als er iets veranderde.

set -eu

SETUP_USER="turtlebot"
SETUP_DIR="/home/$SETUP_USER/turtlebot_setup"
# Laatste stap / fout, getoond op system.html (state/ is in de container
# gemount op /root/turtlebot_state, gelezen door launch_control_node)
STATUS_FILE="$SETUP_DIR/state/update_status.txt"

status() {
  echo "$1"
  mkdir -p "$SETUP_DIR/state"
  printf '%s\n' "$1" > "$STATUS_FILE" || true
}
fail() {
  status "❌ $1"
  exit 1
}

# --- Internet? ---------------------------------------------------------------
# Zonder deze check blijven git/docker hangen op DNS- en connect-timeouts
# (AP zonder werkende WAN-uplink).
status "🔎 Internetverbinding controleren"
online() {
  timeout 10 bash -c ">/dev/tcp/$1/443" 2>/dev/null
}
if ! online 1.1.1.1 && ! online 8.8.8.8; then
  fail "Geen internet via de AP (WAN-poort van de AP niet verbonden?) - update niet mogelijk"
fi
for host in github.com registry-1.docker.io; do
  getent hosts "$host" >/dev/null || fail "Internet wel, maar DNS werkt niet ($host) - update niet mogelijk"
  online "$host" || fail "$host niet bereikbaar - update niet mogelijk"
done

status "🔄 Setup-repo bijwerken (git pull)"
timeout 120 runuser -u "$SETUP_USER" -- git -C "$SETUP_DIR" pull --ff-only \
  || fail "git pull mislukt - details: journalctl -u turtlebot-update"

# Setup opnieuw (nieuwe CSV/units/.env uit de pull toepassen)
status "⚙️ Setup toepassen"
"$SETUP_DIR/setup_turtlebot.sh" || fail "setup_turtlebot.sh mislukt - details: journalctl -u turtlebot-update"

status "⬇️ Nieuwe image ophalen (docker compose pull, kan enkele minuten duren)"
docker compose --project-directory "$SETUP_DIR" pull \
  || fail "docker compose pull mislukt - details: journalctl -u turtlebot-update"

# Herstart enkel als image of compose-config veranderde
status "🔁 Container bijwerken"
docker compose --project-directory "$SETUP_DIR" up -d \
  || fail "docker compose up mislukt - details: journalctl -u turtlebot-update"
docker image prune -f >/dev/null
# host_info.json opnieuw (nieuwe image-digest/commits voor de statuspagina)
"$SETUP_DIR/setup_turtlebot.sh" >/dev/null
status "🎉 Update voltooid"
