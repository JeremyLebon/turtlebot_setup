# Task 1 - Scan sectors

Do the [Exercise](../ros2-nodes/read-in-the-scan-topic/exercise.md) of *Read in the
scan topic* in the simulation (`turtlebot3_world.launch.py`): print the mean
distance **in front**, **left**, **behind** and **right** of the robot, and the
**closest obstacle** with its angle.

{% hint style="info" %}
Calculate the indices from `angle_increment` (see [Laser scan](../theory/laser-scan.md)),
not with fixed numbers: then the same script works in the simulation (360 points)
and on the real robot (about 220-230 points).
{% endhint %}
