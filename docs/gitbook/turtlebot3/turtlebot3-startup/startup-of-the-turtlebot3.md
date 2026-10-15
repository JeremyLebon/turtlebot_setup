# Startup of the turtlebot3

The TurtleBot3 can be powered in 2 ways:

* Via DC adapter (on the table, for programming)
* Via battery (for driving)

Connect the battery to the TurtleBot and switch it on.

* The OpenCR board plays a short melody.
* After about 1 minute the Raspberry Pi is ready: the robot software starts
  **automatically** in a Docker container (`turtlebot_<nr>`) and you hear a
  second short melody. You don't have to start anything yourself yet.

{% hint style="info" %}
**The lidar does not turn yet?** That is normal. To spare the lidar, the USB
power of the robot is switched off when nothing uses it. It switches on by
itself when you start the bringup (see
[Startup turtlebot software](startup-turtlebot-software.md)).
{% endhint %}

{% hint style="danger" %}
**Battery**: below **11.0 V** the OpenCR switches the motors off and the robot
beeps. Below about 11.2 V: charge or swap the battery. You can read the voltage
with `ros2 topic echo /battery_state --field voltage` (after the bringup) or on
the status page.
{% endhint %}

Continue with [Connect to the turtlebot3](connect-to-the-turtlebot3.md).
