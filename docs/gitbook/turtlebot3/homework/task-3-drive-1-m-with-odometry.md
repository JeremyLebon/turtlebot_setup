# Task 3 - Drive exactly 1 m with odometry

In *Drive 10cm with a button* the robot drives on **time**. Now use **`/odom`**:
drive forward at 0.1 m/s until the robot has driven **1.0 m** from its start
position, then stop (publish all speeds 0).

* Subscribe to `/odom` and remember the start position.
* Distance from the start: `math.hypot(x - x0, y - y0)`.
* Publish `TwistStamped` on `/cmd_vel` (simulation).

Extra: turn exactly **90°** to the left, using the yaw from the quaternion
(see [IMU](../theory/imu.md)).
