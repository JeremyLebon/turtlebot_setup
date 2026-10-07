#!/bin/bash
# ~/turtlebot_setup/update_turtlebot.sh - uitgevoerd door
# turtlebot-update.service (als root): repo bijwerken, nieuwste image
# ophalen en de container enkel opnieuw aanmaken als er iets veranderde.

set -eu

SETUP_USER="turtlebot"
SETUP_DIR="/home/$SETUP_USER/turtlebot_setup"

echo "🔄 git pull in $SETUP_DIR"
runuser -u "$SETUP_USER" -- git -C "$SETUP_DIR" pull --ff-only

# Setup opnieuw (nieuwe CSV/units/.env uit de pull toepassen)
"$SETUP_DIR/setup_turtlebot.sh"

echo "🔄 docker compose pull"
docker compose --project-directory "$SETUP_DIR" pull

# Herstart enkel als image of compose-config veranderde
docker compose --project-directory "$SETUP_DIR" up -d
docker image prune -f >/dev/null
echo "🎉 Update voltooid"
