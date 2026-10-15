# Turtlebot3 - startup

Follow these steps in this order:

1. [Connect to the WIFI](connect-to-the-wifi.md) - your laptop on `TB-AP-<nr>`
2. [Startup of the turtlebot3](startup-of-the-turtlebot3.md) - battery on, wait for the beep
3. [Connect to the turtlebot3](connect-to-the-turtlebot3.md) - a terminal inside the robot container
4. [Startup docker](startup-docker.md) - check that the robot container runs (nothing to start)
5. [Startup turtlebot software](startup-turtlebot-software.md) - start the bringup
6. [Setup laptop (student)](setup-laptop-student.md) - the `turtlebot-vis` container on your laptop

{% hint style="info" %}
Replace `<nr>` everywhere by the number of **your** robot, without a leading zero: robot 5 -> `TB-AP-05`, `10.0.5.10`, `turtlebot_5`, `ROS_DOMAIN_ID=5`.
{% endhint %}
