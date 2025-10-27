#!/bin/bash
# /usr/local/bin/setup_turtlebot.sh

CONFIG_FILE="turtlebot_config.csv"
NET_IFACE="wlan0"  


# Lees MAC-adres
MAC=$(cat /sys/class/net/$NET_IFACE/address | tr '[:lower:]' '[:upper:]')

# Zoek configuratie
LINE=$(grep "$MAC" "$CONFIG_FILE")

if [ -z "$LINE" ]; then
  echo "⚠️ Geen match gevonden voor MAC $MAC in $CONFIG_FILE"
  exit 1
fi

# Parse CSV (mac,hostname,ros_domain_id)
IFS=',' read -r CSV_MAC HOSTNAME ROS_DOMAIN_ID LIDAR <<< "$LINE"

echo "✅ Instellingen gevonden voor $HOSTNAME (ROS_DOMAIN_ID=$ROS_DOMAIN_ID)"

# Stel hostname in
hostnamectl set-hostname "$HOSTNAME"

# ✅ Avahi herstarten zodat nieuwe hostname meteen zichtbaar is via .local
if systemctl list-unit-files | grep -q avahi-daemon.service; then
  echo "🔄 Herstart Avahi-daemon..."
  systemctl restart avahi-daemon
  sleep 2
  echo "✅ Avahi-daemon opnieuw opgestart"
else
  echo "⚠️ Avahi-daemon niet gevonden — controleer of Avahi is geïnstalleerd."
fi

#Stel ROS_DOMAIN_ID in
echo "export ROS_DOMAIN_ID=$ROS_DOMAIN_ID" > /etc/profile.d/ros_domain.sh

#Stel LIDAR model in
echo "export LDS_MODEL=$LIDAR" > /etc/profile.d/lidar_model.sh
echo "✅ Instellingen LIDAR_TYPE: $LIDAR)"



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
