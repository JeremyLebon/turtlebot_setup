# Startup of the turtlebot3

The TurtleBot3 can be powered in 2 ways:

* Via DC adapter
* Via battery

Connect the battery to the TurtleBot and switch it on.

* The OpenCR board plays a short melody.
* After about 1 minute the Raspberry Pi is ready: the robot software starts
  **automatically** (you don't have to start a Docker container yourself) and
  you hear a short startup beep.

{% hint style="info" %}
Everything runs in a Docker container on the robot (`turtlebot_<nr>`). It starts
by itself after every boot and keeps running.
{% endhint %}

Continue with [Connect to the turtlebot3](connect-to-the-turtlebot3.md) and check
the battery voltage and the **labo-check** on the status page.
