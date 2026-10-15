# Odometry (/odom) and encoders

## What is odometry?

**Odometry** is estimating the position of the robot by **counting how far the
wheels have turned**. It is like walking with your eyes closed and counting your
steps: it works well for a short time, but small errors add up.

The robot starts at `(x, y, θ) = (0, 0, 0)` when `turtlebot3_node` starts. From
then on it adds every small movement to that position.

## Encoders on the TurtleBot3

Each wheel is driven by a Dynamixel **XL430** motor with a built-in encoder:

| | Burger |
|---|---|
| encoder ticks per wheel rotation | 4096 |
| wheel radius `r` | 0.033 m |
| distance between the wheels `L` | 0.160 m |
| wheel circumference `2πr` | 0.207 m |
| distance per tick | 0.207 / 4096 ≈ 0.05 mm |

You can see the raw values in two topics:

* `/sensor_state` (`turtlebot3_msgs/msg/SensorState`): `left_encoder`,
  `right_encoder` - the number of ticks (integer).
* `/joint_states` (`sensor_msgs/msg/JointState`): `position[]` of
  `wheel_left_joint` and `wheel_right_joint` in **radians** and `velocity[]` in rad/s.

From ticks to distance travelled by a wheel:

```
angle_wheel  = ticks * 2π / 4096        [rad]
distance     = angle_wheel * r          [m]
speed_wheel  = velocity * r             [m/s]   (velocity from /joint_states)
```

## From two wheels to the position of the robot

The TurtleBot3 is a **differential drive** robot: two driven wheels and a
caster at the back. It cannot drive sideways. Every small time step:

```
d_left, d_right = distance of each wheel since the last step

d     = (d_right + d_left) / 2          distance of the robot centre
dθ    = (d_right - d_left) / L          rotation of the robot

x    += d * cos(θ + dθ/2)
y    += d * sin(θ + dθ/2)
θ    += dθ
```

* Both wheels the same distance → driving straight (`dθ = 0`).
* Wheels in opposite directions → turning on the spot (`d = 0`).

The same formulas the other way around turn a command on `/cmd_vel`
(`linear.x = v`, `angular.z = ω`) into wheel speeds:

```
v_left  = v - ω * L / 2
v_right = v + ω * L / 2
```

{% hint style="info" %}
**On our robot** the IMU helps: `turtlebot3_node` is configured with
`use_imu: true`. The **distance** comes from the wheel encoders, but the
**rotation θ** comes from the [IMU](imu.md). The IMU measures rotation better
than the wheels, which slip when the robot turns.
{% endhint %}

## The Odometry message

`/odom` is of type `nav_msgs/msg/Odometry`:

| field | meaning |
|---|---|
| `header.frame_id` | `odom` - the position is relative to the start point |
| `child_frame_id` | `base_footprint` - the robot |
| `pose.pose.position` | `x`, `y` (m), `z` is always 0 |
| `pose.pose.orientation` | rotation as a **quaternion** (`x, y, z, w`) - see [IMU](imu.md) |
| `twist.twist.linear.x` | forward speed (m/s) |
| `twist.twist.angular.z` | rotation speed (rad/s) |
| `pose.covariance`, `twist.covariance` | how uncertain the estimate is |

The same position is also published as the transform `odom -> base_footprint` on
`/tf` (see [TF](tf.md)).

## Why does odometry drift?

* the wheels **slip** (smooth floor, accelerating, turning)
* the wheel radius is not exactly 0.033 m (wear, tyre pressure, dust)
* bumps, thresholds, cables
* small errors in θ become large errors in x, y after a few metres

So `/odom` is **smooth and fast, but not correct over long distances**. To know
where the robot really is, SLAM or AMCL compares the [laser scan](laser-scan.md)
with a map and publishes a correction (`map -> odom`, see [TF](tf.md)).

## Try it

```bash
ros2 topic echo /odom --field pose.pose.position
ros2 topic echo /sensor_state --field left_encoder
ros2 topic echo /joint_states
```

Drive 1 m forward (mark it on the floor) and compare with `x` in `/odom`.
Then turn 4 times on the spot and look at `x`, `y`: are they still 0?

<details>

<summary>Check yourself</summary>

1. The left encoder went from 10 000 to 22 288 ticks. How far did the left wheel drive?
   * 12 288 ticks = 3 rotations → 3 × 0.207 m ≈ 0.62 m.
2. `/cmd_vel` has `linear.x = 0`, `angular.z = 1.0` rad/s. What are the wheel speeds?
   * v_left = -0.08 m/s, v_right = +0.08 m/s: turning left on the spot.
3. After driving through the lab for 5 minutes, the robot in RViz2 (fixed frame `odom`) is 30 cm next to where it really is. Is something broken?
   * No, that is normal odometry drift.

</details>

Next: [Read the encoder value](../ros2-nodes/read-the-encoder-value.md).
