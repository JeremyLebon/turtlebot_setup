# Theory: what the robot measures

You have now seen the topics of the robot in Gazebo, RViz2 and the terminal.
Before you write your own nodes, this chapter explains **where the data comes
from** and **what it means**: a short piece of theory for each important topic,
applied to the TurtleBot3 Burger in Gazebo. Keep the simulation running: every
page has a few commands to try.

* [Laser scan (`/scan`)](theory/laser-scan.md) - what the lidar sees
* [Odometry (`/odom`) and wheels](theory/odometry.md) - where the robot thinks it is
* [IMU (`/imu`)](theory/imu.md) - rotation and acceleration
* [TF - coordinate frames](theory/tf.md) - how everything fits together
* [Driving the robot (`/cmd_vel`)](theory/cmd-vel.md) - speed commands
* [QoS - Quality of Service](theory/qos.md) - why you sometimes receive nothing

## Where does the data come from?

In the simulation there is no real hardware: **Gazebo** calculates the physics
(wheels, floor, walls) and simulates the sensors. A **bridge** turns the Gazebo
messages into ROS 2 topics.

```
            Docker container gazebo_turtlebot_cont (your laptop)
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Gazebo (gz sim)                    ros_gz_bridge         ROS 2      │
 │  ┌──────────────────────────┐                                         │
 │  │ lidar sensor   ──────────┼──────────────────────────►  /scan       │
 │  │ IMU sensor     ──────────┼──────────────────────────►  /imu        │
 │  │ DiffDrive plugin ────────┼──────────────────────────►  /odom, /tf  │
 │  │ JointState plugin ───────┼──────────────────────────►  /joint_states
 │  │ simulation time ─────────┼──────────────────────────►  /clock      │
 │  │ DiffDrive plugin ◄───────┼───────────────────────────  /cmd_vel    │
 │  └──────────────────────────┘                                         │
 │                                                                       │
 │  robot_state_publisher (URDF + /joint_states) ───────►  /tf, /tf_static,
 │                                                          /robot_description
 │  RViz2, teleop_twist_keyboard, your nodes                             │
 └──────────────────────────────────────────────────────────────────────┘
```

* The **DiffDrive plugin** moves the wheels when you send `/cmd_vel` and
  **calculates the odometry**.
* The sensors in Gazebo get a bit of **noise** on purpose, so the data looks
  like real sensor data.
* Gazebo has its own clock (`/clock`). That is why nodes in the simulation use
  `use_sim_time:=True`: they follow the simulation time, not the clock of your laptop.

On the real robot the same topics come from real hardware (see
[Simulation vs. real robot](../simulation-vs-real-robot.md)). That is the strength
of ROS: your code does not see the difference.

## Conventions used by all ROS robots

ROS uses fixed conventions (REP-103), so every robot and every tool agrees:

| Quantity | Unit | |
|---|---|---|
| distance | metre (m) | not cm or mm! |
| angle | radian (rad) | 1 rad ≈ 57.3°, 90° = π/2 ≈ 1.571 rad |
| linear speed | m/s | |
| angular speed | rad/s | |
| time | seconds (ROS time stamp in the `header`) | |

Axes of the robot (right-hand rule):

```
            x (forward)
            ▲
            │
   y ◄──────●        z points up, out of the screen
  (left)   robot
```

* **x** = forward, **y** = left, **z** = up.
* A **positive rotation** around z is **counterclockwise** (to the left).
  So `angular.z = +0.5` in `/cmd_vel` turns the robot to the left.

{% hint style="info" %}
Try it: start the simulation, then `ros2 topic list` and `ros2 topic info /odom`.
Which node publishes `/odom`? (Hint: it is the bridge.)
{% endhint %}
