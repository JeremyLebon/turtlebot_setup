# IMU (/imu)

## What is an IMU?

An **IMU** (Inertial Measurement Unit) is a small chip that measures how the
robot **moves and rotates**. On the TurtleBot3 the IMU is on the **OpenCR**
board. It contains:

* a **gyroscope**: rotation speed around x, y and z (rad/s)
* an **accelerometer**: acceleration along x, y and z (m/s²)

(You know these sensors from your phone and from the flight controller of a drone.)

The OpenCR combines both in a filter and calculates the **orientation** of the
robot: how it is turned in space.

```
          z (yaw)
          ▲
          │
          │
          ●─────► x (roll)      roll  = rotation around x (tilt left/right)
         ╱                      pitch = rotation around y (nose up/down)
        ╱                       yaw   = rotation around z (heading)
       ▼
      y (pitch)
```

For a ground robot, **yaw** (the heading) is by far the most important one.
Roll and pitch stay almost 0 on a flat floor.

## The Imu message

`/imu` is of type `sensor_msgs/msg/Imu`, frame `imu_link`:

| field | meaning | robot standing still on the floor |
|---|---|---|
| `orientation` | rotation as a quaternion (`x, y, z, w`) | depends on the heading |
| `angular_velocity` | rad/s around x, y, z | ≈ 0, 0, 0 |
| `linear_acceleration` | m/s² along x, y, z | ≈ 0, 0, **9.81** |

{% hint style="info" %}
Standing still, the accelerometer measures **9.81 m/s² upwards**: it measures
gravity. That is how the IMU knows which way is down (roll and pitch). For yaw
there is no such reference, so yaw slowly **drifts**.
{% endhint %}

## Quaternions

ROS does not store orientation as three angles, but as a **quaternion**: four
numbers `(x, y, z, w)`. Quaternions have no problems with angles that jump from
+180° to -180° and are easy to combine. You don't have to understand the
maths, just remember:

* no rotation: `(0, 0, 0, 1)`
* for a ground robot only `z` and `w` change
* convert to **yaw** (in rad) like this:

```python
import math

q = msg.orientation          # also works for msg.pose.pose.orientation of /odom
yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
print(math.degrees(yaw))
```

## IMU and odometry on our robot

The wheels are good at measuring **distance**, but bad at measuring **rotation**:
during a turn the wheels slip. The gyroscope measures rotation directly. That is
why `turtlebot3_node` uses the yaw of the IMU for the heading in `/odom`
(`use_imu: true`, see [Odometry](odometry.md)).

| | wheel encoders | IMU (gyroscope) |
|---|---|---|
| distance | ✅ good | ❌ (double integration of acceleration → very large drift) |
| rotation | ⚠️ errors from slip | ✅ good, slow drift over time |

Combining sensors to get a better result than each sensor alone is called
**sensor fusion**.

## Try it

```bash
ros2 topic hz /imu
ros2 topic echo /imu --field angular_velocity
ros2 topic echo /imu --field linear_acceleration
```

* Turn the robot by hand around its vertical axis: which value of `angular_velocity` changes? Positive or negative to the left?
* Tilt the robot (carefully!): what happens with `linear_acceleration`?

<details>

<summary>Check yourself</summary>

1. The robot turns left at 0.5 rad/s. What does `angular_velocity.z` show?
   * About +0.5 (counterclockwise is positive).
2. The quaternion is `(0, 0, 0.707, 0.707)`. What is the yaw?
   * atan2(2·0.707·0.707, 1 − 2·0.707²) = atan2(1, 0) = π/2 → 90°, turned to the left.
3. Why can't we calculate the position of the robot from the accelerometer?
   * Acceleration has to be integrated twice; every small error grows very fast (quadratically in time).

</details>
