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

## Startup at home

The same steps as in the simulation book
([Installation](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/installation), [Startup](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/turtlebot-in-simulation/startup),
[The first ros2 node](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node)):

1. Open a WSL terminal and start the simulation container:

   ```sh
   cd ros2-jazzy-gazebo-turtlebot
   docker compose up
   ```

2. Open a **second** WSL terminal, go inside the container and start Gazebo with the robot:

   ```sh
   docker exec -it gazebo_turtlebot_cont bash
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

3. Open **VS Code** > Remote Explorer > WSL > Dev Containers >
   `ros2-jazzy-gazebo-turtlebot` > attach, folder `/home/dockeruser/dev_ws`.
   Make your scripts there and run them in the VS Code terminal
   (`python3 <script>.py`).

4. **Only for task 2:** copy the script of
   [Simulation of sensors](simulation-of-sensors.md) to
   `/home/dockeruser/dev_ws/simulation_sensors.py` and start it in an extra
   terminal (`python3 simulation_sensors.py`). It publishes fake battery and
   sensor values on `/sim/...`.

5. Drive the robot (for task 1) in another terminal:

   ```sh
   ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
   ```

{% hint style="info" %}
Check: `ros2 topic list` in the container shows `/scan`, `/odom`, `/cmd_vel`,
... (and `/sim/battery_state` when step 4 runs).
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

Start [Simulation of sensors](simulation-of-sensors.md) (step 4 of the
startup): it publishes random values on `/sim/battery_state`. Write a node that subscribes to
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
