# Odometry (/odom) and wheels

## What is odometry?

**Odometry** is estimating the position of the robot by **counting how far the
wheels have turned**. It is like walking with your eyes closed and counting your
steps: it works well for a short time, but small errors add up.

The robot starts at `(x, y, θ) = (0, 0, 0)` when the simulation starts. From
then on every small movement is added to that position.

## The wheels of the TurtleBot3 Burger

| | Burger |
|---|---|
| wheel radius `r` | 0.033 m |
| distance between the wheels `L` | 0.160 m |
| wheel circumference `2πr` | 0.207 m |

The topic `/joint_states` (`sensor_msgs/msg/JointState`) shows the wheels:

* `name[]`: `wheel_left_joint`, `wheel_right_joint`
* `position[]`: how far each wheel has turned, in **radians** (keeps counting)
* `velocity[]`: rotation speed of each wheel in rad/s

From wheel rotation to distance:

```
distance     = position * r          [m]
speed_wheel  = velocity * r          [m/s]
```

{% hint style="info" %}
The real robot has **encoders** on the motors: 4096 ticks per wheel rotation,
in the topic `/sensor_state`. The simulation only has `/joint_states`, which the
real robot also has.
{% endhint %}

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

In Gazebo the **DiffDrive plugin** does both: it turns `/cmd_vel` into wheel
speeds, and it calculates `/odom` from the wheels (30 times per second).

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

On a real robot:

* the wheels **slip** (smooth floor, accelerating, turning)
* the wheel radius is not exactly 0.033 m (wear, dust)
* bumps, thresholds, cables
* small errors in θ become large errors in x, y after a few metres

In **Gazebo** the floor is perfect and the wheel radius is exact, so the odometry
is almost perfect. Don't be fooled: on the real robot it drifts much more. That
is why SLAM or AMCL compares the [laser scan](laser-scan.md) with a map and
publishes a correction (`map -> odom`, see [TF](tf.md)).

## Try it

```bash
ros2 topic echo /odom --field pose.pose.position
ros2 topic echo /joint_states
```

Drive straight ahead with `teleop_twist_keyboard` and compare the change of `x`
in `/odom` with the change of `position` × 0.033 in `/joint_states`.

<details>

<summary>Check yourself</summary>

1. The left wheel `position` went from 10.0 to 28.85 rad. How far did the left wheel drive?
   * 18.85 rad × 0.033 m ≈ 0.62 m (= 3 wheel rotations).
2. `/cmd_vel` has `linear.x = 0`, `angular.z = 1.0` rad/s. What are the wheel speeds?
   * v_left = -0.08 m/s, v_right = +0.08 m/s: turning left on the spot.
3. In the simulation `/odom` stays correct for minutes. Will that also be the case on the real robot?
   * No: slip and small errors make the real odometry drift.

</details>

Next: [The first ros2 node](../../the-first-ros2-node.md) (subscribe to `/odom`).
