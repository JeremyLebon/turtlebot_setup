#!/bin/bash
# /usr/local/bin/setup_turtlebot.sh

CONFIG_FILE="/etc/turtlebot_config.csv"
NET_IFACE="wlan0"  # pas aan naar wlan0 als je wifi gebruikt

# Lees MAC-adres
MAC=$(cat /sys/class/net/$NET_IFACE/address | tr '[:lower:]' '[:upper:]')

# Zoek configuratie
LINE=$(grep "$MAC" "$CONFIG_FILE")

if [ -z "$LINE" ]; then
  echo "⚠️ Geen match gevonden voor MAC $MAC in $CONFIG_FILE"
  exit 1
fi

# Parse CSV (mac,hostname,ros_domain_id)
IFS=',' read -r CSV_MAC HOSTNAME ROS_DOMAIN_ID <<< "$LINE"

echo "✅ Instellingen gevonden voor $HOSTNAME (ROS_DOMAIN_ID=$ROS_DOMAIN_ID)"

# Stel hostname in
hostnamectl set-hostname "$HOSTNAME"

# Stel ROS_DOMAIN_ID in
# echo "export ROS_DOMAIN_ID=$ROS_DOMAIN_ID" > /etc/profile.d/ros_domain.sh

# # Pas Docker .env aan (indien aanwezig)
# if [ -f /home/ubuntu/docker/.env ]; then
#   sed -i "s/^ROS_DOMAIN_ID=.*/ROS_DOMAIN_ID=$ROS_DOMAIN_ID/" /home/ubuntu/docker/.env
# fi

# # (optioneel) restart docker-compose
# if [ -f /home/ubuntu/docker/docker-compose.yml ]; then
#   cd /home/ubuntu/docker
#   docker compose up -d
# fi

echo "🎉 TurtleBot setup voltooid!"
