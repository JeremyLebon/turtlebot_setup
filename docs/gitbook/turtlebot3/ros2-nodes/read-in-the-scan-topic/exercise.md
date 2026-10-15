# Exercise

## Exercise 1 - Obstacle alarm

Extend your `sub_scan.py` (or make `obstacle_alarm.py`): when something is
**closer than 0.30 m in front of the robot**, print a warning and let the robot
**play a sound**. The robot doesn't drive: test it by holding your hand or foot
in front of the lidar.

1. Take the front part of the scan, as in the guided part (`ranges[:n] + ranges[-n:]`).
2. Use the **closest** distance (`min`) instead of the mean. Why is the mean not good for an alarm?
3. Ignore invalid values: keep only finite values **larger than 0.12 m** (the
   real lidar gives `0.0` when there is no echo).
4. Closest distance below 0.30 m: log a warning with `self.get_logger().warn(...)`.
5. Play a sound with the `/sound` service (see [Play a sound](../../play-a-sound.md)),
   value `3` (error melody) - but **only once** when the obstacle appears, not 5
   times per second.

<details>

<summary>Hints</summary>

* A single chair leg in front of the robot hardly changes the **mean** of 30
  values; the **minimum** shows it immediately.
* "Only once": remember in `self.alarm` whether the obstacle was already there in
  the previous scan - the same idea as the rising edge of the A button in
  [Drive 10cm with a button](../drive-10cm-with-a-button.md).
* Make the service client in `__init__` (`self.create_client(Sound, '/sound')`)
  and use `call_async(...)` in the callback. Never wait for the answer inside a
  callback: that blocks your node.

</details>

<details>

<summary>Solution</summary>

```python
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from turtlebot3_msgs.srv import Sound

ALARM_DISTANCE = 0.30   # m
MIN_VALID = 0.12        # m: smaller values (0.0) = no echo


class ObstacleAlarm(Node):
    def __init__(self):
        super().__init__('obstacle_alarm')
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, qos)
        self.sound_client = self.create_client(Sound, '/sound')
        self.alarm = False   # was the obstacle already there in the previous scan?
        self.get_logger().info('Obstacle alarm started')

    def scan_callback(self, msg):
        n = 15
        front = list(msg.ranges[:n]) + list(msg.ranges[-n:])
        front = [r for r in front if math.isfinite(r) and r > MIN_VALID]
        if not front:
            return
        closest = min(front)

        if closest < ALARM_DISTANCE:
            self.get_logger().warn(f'Obstacle at {closest:.2f} m!')
            if not self.alarm:             # only once, when the obstacle appears
                self.play_sound(3)         # 3 = error melody
            self.alarm = True
        else:
            self.alarm = False

    def play_sound(self, value):
        if not self.sound_client.service_is_ready():
            self.get_logger().warn('/sound service not available')
            return
        request = Sound.Request()
        request.value = value
        self.sound_client.call_async(request)   # don't wait inside a callback


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAlarm()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

</details>

Show the result to the lecturer.

{% hint style="info" %}
Extra: also warn for obstacles **behind** the robot. Which part of `ranges` is
that? (Tip: see [Laser scan](../../theory/laser-scan.md).)
{% endhint %}

## Exercise 2 - Scan sectors

Front, left, behind and right at the same time: that is
[Task 1](../../homework/task-1-scan-sectors.md) of the homework.
