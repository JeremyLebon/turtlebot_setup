# Theory: what the robot measures

Reference chapter: **where the data comes from** and **what it means**, for
each important topic, applied to our TurtleBot3 Burger. You saw most of it in
the simulation; here are the values of the real robot. The exercises link to
the page you need.

* [Laser scan (`/scan`)](theory/laser-scan.md) - what the lidar sees
* [Odometry (`/odom`) and encoders](theory/odometry.md) - where the robot thinks it is
* [IMU (`/imu`)](theory/imu.md) - rotation and acceleration
* [TF - coordinate frames](theory/tf.md) - how everything fits together
* [Driving the robot (`/cmd_vel`)](theory/cmd-vel.md) - speed commands and twist_mux
* [QoS - Quality of Service](theory/qos.md) - why you sometimes receive nothing

## Where does the data come from?

```
                 TurtleBot3 Burger (robot)                         Laptop (student)
 ┌─────────────────────────────────────────────────────┐
 │  LDS-02 lidar ──USB──┐                              │
 │                      │   Raspberry Pi 5             │
 │                      ▼   (container turtlebot_<nr>) │
 │                 ld08_driver ──────────► /scan       │
 │                                                     │     Zenoh      ┌──────────────┐
 │  OpenCR board ──USB──► turtlebot3_node ─► /odom     │ ◄────wifi────► │ turtlebot-vis│
 │   • 2 motors with       (ROS 2 driver)  ─► /imu     │   TB-AP-<nr>   │  RViz2, rqt, │
 │     encoders                            ─► /tf      │                │  your nodes  │
 │   • IMU chip                            ─► /joint_states            └──────────────┘
 │   • battery, buttons                    ─► /sensor_state, /battery_state
 │                                                     │
 │                 /cmd_vel ──► twist_mux ──► turtlebot3_node ──► motors
 └─────────────────────────────────────────────────────┘
```

* The **OpenCR** board is a microcontroller board. It reads the motor encoders,
  the IMU, the battery and the buttons and drives the two motors.
* `turtlebot3_node` on the Raspberry Pi talks to the OpenCR over USB and turns
  everything into ROS 2 topics. It also **calculates the odometry** and
  publishes the transform `odom -> base_footprint`.
* The **LDS-02** lidar has its own driver (`ld08_driver`) that publishes `/scan`.

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
Try it: `ros2 topic list` and `ros2 topic info /odom` (in the `turtlebot-vis`
container). Which node publishes `/odom`? Which nodes publish `/scan` and `/imu`?
{% endhint %}
