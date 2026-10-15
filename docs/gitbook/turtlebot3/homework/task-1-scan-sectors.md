# Task 1 - Scan sectors

In the lab you used the **front** of the scan (the obstacle alarm). Now do the
same for **four** directions: print the closest distance **in front**, **left**,
**behind** and **right** of the robot. Work in the simulation
(`turtlebot3_world.launch.py`) and drive around with teleop.

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FODudHqthpJTbo5FEnO7l%2Ffile.excalidraw.svg?alt=media\&token=95719208-4142-42a1-8c38-e621c706bd27)

Expected output, for example:

```
front 0.84 m | left 0.35 m | behind 1.92 m | right inf m
```

<details>

<summary>Hints</summary>

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
