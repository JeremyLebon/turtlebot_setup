# IMU (/imu)

## What is an IMU?

An **IMU** (Inertial Measurement Unit) is a small chip that measures how the
robot **moves and rotates**. On the real TurtleBot3 it is on the OpenCR board;
in Gazebo it is a simulated sensor in the frame `imu_link`. It contains:

* a **gyroscope**: rotation speed around x, y and z (rad/s)
* an **accelerometer**: acceleration along x, y and z (m/s²)

(You know these sensors from your phone and from the flight controller of a drone.)

From both, the **orientation** of the robot is calculated: how it is turned in space.

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

## The IMU in Gazebo

| | simulation | real robot |
|---|---|---|
| rate | 200 Hz | lower (check with `ros2 topic hz /imu`) |
| noise | gaussian, added by Gazebo | real noise and drift |
| frame | `imu_link` | `imu_link` |

## The Imu message

`/imu` is of type `sensor_msgs/msg/Imu`:

| field | meaning | robot standing still on the floor |
|---|---|---|
| `orientation` | rotation as a quaternion (`x, y, z, w`) | depends on the heading |
| `angular_velocity` | rad/s around x, y, z | ≈ 0, 0, 0 (+ noise) |
| `linear_acceleration` | m/s² along x, y, z | ≈ 0, 0, **9.81** |

{% hint style="info" %}
Standing still, the accelerometer measures **9.81 m/s² upwards**: it measures
gravity. That is how the IMU knows which way is down (roll and pitch). For yaw
there is no such reference, so on a real robot yaw slowly **drifts**.
{% endhint %}

## Quaternions

ROS does not store orientation as three angles, but as a **quaternion**: four
numbers `(x, y, z, w)`. Quaternions have no problems with angles that jump from
+180° to -180° and are easy to combine. You don't have to understand the
maths, just remember:

* no rotation: `(0, 0, 0, 1)`
* for a ground robot only `z` and `w` change
* convert to **yaw** (in rad) like this (you will see this code again in
  [The first ros2 node](../../the-first-ros2-node.md)):

```python
import math

q = msg.orientation          # also works for msg.pose.pose.orientation of /odom
yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
print(math.degrees(yaw))
```

## IMU and wheels

| | wheels (odometry) | IMU (gyroscope) |
|---|---|---|
| distance | ✅ good | ❌ (double integration of acceleration → very large drift) |
| rotation | ⚠️ errors from slip | ✅ good, slow drift over time |

That is why the real TurtleBot3 combines both: distance from the wheels, heading
from the IMU. Combining sensors to get a better result than each sensor alone
is called **sensor fusion**. (In the simulation `/odom` only uses the wheels -
the perfect Gazebo floor makes that good enough.)

## Try it

```bash
ros2 topic hz /imu
ros2 topic echo /imu --field angular_velocity
ros2 topic echo /imu --field linear_acceleration
```

* Turn the robot left with `teleop_twist_keyboard`: which value of `angular_velocity` changes? Positive or negative?
* Compare `angular_velocity.z` of `/imu` with `twist.twist.angular.z` of `/odom`.

<details>

<summary>Check yourself</summary>

1. The robot turns left at 0.5 rad/s. What does `angular_velocity.z` show?
   * About +0.5 (counterclockwise is positive).
2. The quaternion is `(0, 0, 0.707, 0.707)`. What is the yaw?
   * atan2(2·0.707·0.707, 1 − 2·0.707²) = atan2(1, 0) = π/2 → 90°, turned to the left.
3. Why can't we calculate the position of the robot from the accelerometer?
   * Acceleration has to be integrated twice; every small error grows very fast (quadratically in time).

</details>

Exercise: [Here come the sensors](../here-come-the-sensors.md) (IMU part).

Next: [TF - coordinate frames](tf.md).
