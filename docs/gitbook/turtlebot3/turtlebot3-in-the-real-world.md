# Turtlebot3 in the real world

In the simulation you drove a virtual TurtleBot3 in Gazebo. Now you work with the **real robot**. The ROS 2 topics are the same (`/scan`, `/odom`, `/imu`, `/cmd_vel`, ...), so most of what you learned still works - but the real world has a battery, a wifi connection, wheel slip and sensor noise.

How the lab is set up:

* Every TurtleBot has its **own wifi network** `TB-AP-<nr>`.
* The robot software runs in a **Docker container** on the Raspberry Pi of the robot (`turtlebot_<nr>`). It starts by itself when the robot boots.
* On your laptop you use the **`turtlebot-vis`** container (RViz2, teleop and your own nodes). It talks to the robot with ROS 2 over **Zenoh**.

{% hint style="warning" %}
**Before the lab, with internet** (eduroam, at home): download the laptop container, see [Setup laptop (student)](turtlebot3-startup/setup-laptop-student.md). It is about 4 GB, and the robot wifi has no (or only slow) internet.
{% endhint %}

{% hint style="info" %}
New to the topics, TF, odometry or QoS? Read the [Theory: what the robot measures](theory/) first.
{% endhint %}
