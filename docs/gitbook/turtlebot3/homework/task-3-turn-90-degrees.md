# Task 3 - Turn exactly 90°

In the lab you drove **straight** (*Drive 10cm with a button*, on time). Now the
robot **turns**, and you use the **odometry** to know when to stop: turn exactly
**90° to the left** on the spot, then stop.

1. Subscribe to `/odom` and calculate the **yaw** (heading) from the quaternion
   in `pose.pose.orientation` (see [IMU - Quaternions](../theory/imu.md)).
2. Remember the yaw of the **first** message: that is your start.
3. Publish on `/cmd_vel` (simulation: `TwistStamped`) with only `angular.z`
   (positive = left, for example 0.3 rad/s).
4. Stop (publish all speeds 0) as soon as the robot turned 90° (π/2 rad).
5. Print the start yaw and how far the robot really turned, in degrees.

Check it in Gazebo: is the robot turned exactly a quarter turn?

<details>

<summary>Hints</summary>

* Yaw from a quaternion `q`:
  `math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))`.
* The yaw jumps from **+180° to -180°**. Starting at 170° and turning 90° left
  ends at -100°, so `yaw - start` gives -270°. Bring the difference back between
  -180° and +180°: `math.atan2(math.sin(d), math.cos(d))`.
* The robot overshoots when it turns fast until the very end: turn **slower**
  when you get close (for example speed proportional to the remaining angle,
  with a minimum).
* Stop your node when it is done, and always publish speed 0 at the end.

</details>

## Extension - drive a square

Combine driving and turning: drive a **square of 0.5 m × 0.5 m** and come back to
the start. Use `/odom` for both the distance (`math.hypot(x - x0, y - y0)`) and
the angle. How far from the start does the robot end? Why?
