# Task 1 - Obstacle alarm

Make `obstacle_alarm.py`, based on your `sub_scan.py` from the lab: when
something is **closer than 0.30 m in front of the robot**, print a warning.
Work in the simulation (`turtlebot3_world.launch.py`) and drive towards a wall or
a pillar with teleop.

1. Take the front part of the scan, as in [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic/): `ranges[:n] + ranges[-n:]`.
2. Use the **closest** distance (`min`) instead of the mean. Why is the mean not good for an alarm?
3. Ignore invalid values: keep only finite values **larger than 0.12 m** (the
   real lidar gives `0.0` when there is no echo, the simulation gives `inf`).
4. Closest distance below 0.30 m: log a warning with `self.get_logger().warn(...)`,
   but print **"obstacle!" only once** when the obstacle appears, and
   **"free again"** when it is gone.

Expected output, for example:

```
[WARN] [obstacle_alarm]: obstacle at 0.27 m!
[INFO] [obstacle_alarm]: free again
```

<details>

<summary>Hints</summary>

* A single chair leg in front of the robot hardly changes the **mean** of 30
  values; the **minimum** shows it immediately.
* "Only once": remember in `self.alarm` whether the obstacle was already there in
  the previous scan - the same idea as the rising edge of the A button in
  [Drive 10cm with a button](../ros2-nodes/drive-10cm-with-a-button.md).
* Sound (extra, real robot): make the service client in `__init__`
  (`self.create_client(Sound, '/sound')`) and use `call_async(...)` in the
  callback. Never wait for the answer inside a callback: that blocks your node.

</details>

{% hint style="info" %}
**Extra for the next lab (real robot):** let the robot play a sound when the
obstacle appears: service `/sound`, type `turtlebot3_msgs/srv/Sound`, value `3`
(see [Play a sound](../play-a-sound.md)). The simulation has no `/sound` service.
{% endhint %}

## Extension - scan sectors

Do the same for **four** directions: print the closest distance **in front**,
**left**, **behind** and **right** of the robot.

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FODudHqthpJTbo5FEnO7l%2Ffile.excalidraw.svg?alt=media\&token=95719208-4142-42a1-8c38-e621c706bd27)

Expected output, for example:

```
front 0.84 m | left 0.35 m | behind 1.92 m | right inf m
```

<details>

<summary>Hints for the extension</summary>

* Index 0 is in front, the angle grows counterclockwise: a quarter of the
  array further is **left**, half way is **behind**, three quarters is **right**
  (see [Laser scan](../theory/laser-scan.md)).
* Don't use fixed numbers: calculate them, then the same script works in the
  simulation (360 points) and on the real robot (about 220-230 points):

  ```python
  n = len(msg.ranges)
  quarter = n // 4
  k = int(math.radians(15) / msg.angle_increment)   # +-15 degrees around each direction
  left = msg.ranges[quarter - k : quarter + k]
  ```

* **Front** is special: it is at the start **and** at the end of the array
  (`ranges[:k] + ranges[-k:]`).
* Filter invalid values (`inf`, `nan`, values below 0.12 m) before `min()`,
  and handle an empty list.

</details>

Extra: also print the **angle** (in degrees) of the closest obstacle of the whole scan.
