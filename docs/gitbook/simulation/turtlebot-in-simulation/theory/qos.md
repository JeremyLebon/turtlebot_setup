# QoS - Quality of Service

## Why QoS?

Not every topic needs the same kind of delivery:

* A **laser scan** arrives 5 times per second. If one is lost on the network, it
  is no use sending it again: the next one is newer anyway.
* A **map** is published once. A node that starts later must still get it.
* A **command** that has to arrive should be sent again when it gets lost.

With **QoS** (Quality of Service) every publisher and subscriber says how it
wants to send or receive messages.

## The three settings you need

| setting | options | meaning |
|---|---|---|
| **Reliability** | `RELIABLE` | a lost message is sent again (like TCP) |
| | `BEST_EFFORT` | a lost message is lost, no waiting (like UDP) - good for sensors |
| **Durability** | `VOLATILE` | you only get messages sent **after** you subscribed |
| | `TRANSIENT_LOCAL` | the publisher keeps the last message(s); a **late** subscriber still gets them ("latched") |
| **History + depth** | `KEEP_LAST` + `depth` | how many messages are kept in the queue (e.g. 10) |

There are more settings (deadline, lifespan, liveliness), but you won't need
them in this lab.

When you write `self.create_subscription(Odometry, '/odom', self.cb, 10)`, the
`10` is the depth, and you get the **default** QoS: `RELIABLE`, `VOLATILE`, `KEEP_LAST 10`.

## Publisher and subscriber must match

The simulation uses the DDS middleware (CycloneDDS). A subscriber only receives
messages if it asks for **the same or less** than the publisher offers:

| publisher offers | subscriber asks | works? |
|---|---|---|
| RELIABLE | RELIABLE | ✅ |
| RELIABLE | BEST_EFFORT | ✅ |
| BEST_EFFORT | BEST_EFFORT | ✅ |
| BEST_EFFORT | **RELIABLE** | ❌ no messages |
| TRANSIENT_LOCAL | VOLATILE or TRANSIENT_LOCAL | ✅ |
| VOLATILE | **TRANSIENT_LOCAL** | ❌ no messages |

The nasty part: there is **no error**, you simply get nothing (at most a warning
*"incompatible QoS"*).

{% hint style="success" %}
**Rule of thumb:** subscribe to sensor data (`/scan`, `/imu`, ...) with
**Best Effort**. A Best Effort subscriber works with a Reliable *and* a Best
Effort publisher, so your code works in the simulation **and** on the real robot.
{% endhint %}

## QoS of the topics in the simulation

| topic | reliability | durability | published by |
|---|---|---|---|
| `/scan`, `/imu`, `/odom`, `/joint_states`, `/tf`, `/clock` | RELIABLE | VOLATILE | `ros_gz_bridge` (default QoS) |
| `/tf_static`, `/robot_description` | RELIABLE | **TRANSIENT_LOCAL** | `robot_state_publisher`: sent once, nodes that start later still get it |
| `/map` (SLAM / Nav2, later in this book) | RELIABLE | **TRANSIENT_LOCAL** | sent once, RViz2 started later must still see it |

{% hint style="info" %}
On the real robot the lidar driver publishes `/scan` as **BEST_EFFORT**. In the
simulation the bridge publishes it as RELIABLE. That is why the real-robot
tutorial tells you to set Best Effort in RViz2 - following the rule of thumb
above, you do that in the simulation as well.
{% endhint %}

Check it yourself: `ros2 topic info -v /scan` shows the QoS of every publisher
and subscriber.

## QoS in Python

For sensor data there is a ready-made profile:

```python
from rclpy.qos import qos_profile_sensor_data

self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data)
```

Or set it yourself:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(depth=10,
                 reliability=ReliabilityPolicy.BEST_EFFORT)

map_qos = QoSProfile(depth=1,
                     reliability=ReliabilityPolicy.RELIABLE,
                     durability=DurabilityPolicy.TRANSIENT_LOCAL)
```

In RViz2 you find the same settings per display under **Topic**: *Reliability
Policy*, *Durability Policy*, *Depth*.

## Try it

```bash
ros2 topic info -v /scan
ros2 topic info -v /tf_static
ros2 topic echo --qos-durability transient_local /scan --once    # what happens?
```

<details>

<summary>Check yourself</summary>

1. Why would you use Best Effort for a laser scan?
   * Resending an old scan is useless (the next one arrives 0.2 s later) and causes extra traffic and delay.
2. The last command above (`transient_local` on `/scan`) waits forever. Why?
   * The bridge offers VOLATILE, the subscriber asks TRANSIENT_LOCAL → incompatible, no messages.
3. You start RViz2 after `robot_state_publisher`. Why do you still see the robot model?
   * `/robot_description` and `/tf_static` are TRANSIENT_LOCAL: a late subscriber still gets them.

</details>
