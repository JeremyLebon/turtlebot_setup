# Homework

Finish these tasks **at home, before the next session**. You have no robot at
home, so you work in the **simulation**: the container `gazebo_turtlebot_cont`
from the simulation book (Gazebo + ROS 2 Jazzy).

{% hint style="warning" %}
* Store your scripts in `/home/dockeruser/dev_ws` (the `dev_ws` folder of the
  `ros2-jazzy-gazebo-turtlebot` repository), not in the `turtlebot-vis` container:
  without a robot, the `turtlebot-vis` container has no Zenoh router to talk to.
* Simulation vs. real robot: in the simulation `/cmd_vel` is a `TwistStamped`,
  the lidar has 360 points, and there is no `/battery_state`.
{% endhint %}

## Task 1 - Scan sectors

Do the [Exercise](ros2-nodes/read-in-the-scan-topic/exercise.md) of *Read in the
scan topic* in the simulation (`turtlebot3_world.launch.py`): print the mean
distance **in front**, **left**, **behind** and **right** of the robot, and the
**closest obstacle** with its angle.

{% hint style="info" %}
Calculate the indices from `angle_increment` (see [Laser scan](theory/laser-scan.md)),
not with fixed numbers: then the same script works in the simulation (360 points)
and on the real robot (about 220-230 points).
{% endhint %}

## Task 2 - Battery warning

Start [Simulation of sensors](simulation-of-sensors.md): it publishes random
values on `/sim/battery_state`. Write a node that subscribes to
`/sim/battery_state`, prints the voltage and the percentage, and prints a
**warning** when the voltage is below **11.2 V** or the percentage below **50 %**.

On the real robot you only change the topic to `/battery_state`.

## Task 3 - Drive exactly 1 m with odometry

In *Drive 10cm with a button* the robot drives on **time**. Now use **`/odom`**:
drive forward at 0.1 m/s until the robot has driven **1.0 m** from its start
position, then stop (publish all speeds 0).

* Subscribe to `/odom` and remember the start position.
* Distance from the start: `math.hypot(x - x0, y - y0)`.
* Publish `TwistStamped` on `/cmd_vel` (simulation).

Extra: turn exactly **90°** to the left, using the yaw from the quaternion
(see [IMU](theory/imu.md)).

## Task 4 - Theory

Answer the **Check yourself** questions of the theory pages:
[Laser scan](theory/laser-scan.md), [Odometry](theory/odometry.md),
[IMU](theory/imu.md), [TF](theory/tf.md), [cmd_vel](theory/cmd-vel.md) and
[QoS](theory/qos.md).

## Hand in

Upload on Toledo, before the next session:

* your Python scripts of task 1, 2 and 3;
* a screenshot of the terminal output of each script;
* your answers of task 4.

{% hint style="success" %}
Next session: SLAM (make a map) and autonomous navigation with the real robot.
{% endhint %}
