# QoS - Quality of Service

## Why QoS?

Not every topic needs the same kind of delivery:

* A **laser scan** arrives 5 times per second. If one is lost on the wifi, it is
  no use sending it again: the next one is newer anyway.
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

When you write `self.create_subscription(Imu, '/imu', self.cb, 10)`, the `10`
is the depth, and you get the **default** QoS: `RELIABLE`, `VOLATILE`, `KEEP_LAST 10`.

## Publisher and subscriber must match

In standard ROS 2 (DDS middleware, as in the **simulation**) a subscriber only
receives messages if it asks for **the same or less** than the publisher offers:

| publisher offers | subscriber asks | works? |
|---|---|---|
| RELIABLE | RELIABLE | ✅ |
| RELIABLE | BEST_EFFORT | ✅ |
| BEST_EFFORT | BEST_EFFORT | ✅ |
| BEST_EFFORT | **RELIABLE** | ❌ no messages |
| TRANSIENT_LOCAL | VOLATILE or TRANSIENT_LOCAL | ✅ |
| VOLATILE | **TRANSIENT_LOCAL** | ❌ no messages |

The nasty part: there is **no error**, you simply get nothing (at most a warning
*"incompatible QoS"*). That is the classic "RViz2 does not show my laser scan".

{% hint style="info" %}
**Our real robot uses Zenoh** (`rmw_zenoh_cpp`) instead of DDS. Zenoh is less
strict: a `RELIABLE` subscriber still receives a `BEST_EFFORT` topic. But code
and RViz2 settings must also work in the simulation and on other robots, so
**always match the QoS of the publisher**. For sensor data: use Best Effort.
{% endhint %}

## QoS of the TurtleBot3 topics

| topic | reliability | durability | why |
|---|---|---|---|
| `/scan` | **BEST_EFFORT** | VOLATILE | sensor data (`SensorDataQoS`), newest is most important |
| `/odom`, `/imu`, `/joint_states`, `/battery_state`, `/sensor_state` | RELIABLE | VOLATILE | default QoS of `turtlebot3_node` |
| `/cmd_vel` | RELIABLE | VOLATILE | default QoS |
| `/tf` | RELIABLE | VOLATILE | changes all the time |
| `/tf_static` | RELIABLE | **TRANSIENT_LOCAL** | sent once; nodes that start later must still get it |
| `/map` (map server, Nav2) | RELIABLE | **TRANSIENT_LOCAL** | sent once; RViz2 started later must still see the map |

Check it yourself: `ros2 topic info -v /scan` shows the QoS of every publisher
and subscriber.

## QoS in Python

For sensor data there is a ready-made profile:

```python
from rclpy.qos import qos_profile_sensor_data

self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data)
```

Or set it yourself, as in [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic.md):

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
ros2 topic info -v /odom
ros2 topic echo --qos-reliability best_effort /scan --field ranges
```

<details>

<summary>Check yourself</summary>

1. Why is `/scan` Best Effort and not Reliable?
   * Resending an old scan over the wifi is useless (the next one arrives 0.2 s later) and causes extra traffic and delay.
2. In the simulation, your subscriber on `/scan` uses `10` as QoS. What happens?
   * Default = RELIABLE, publisher offers BEST_EFFORT → incompatible, no messages.
3. You start RViz2 after the map server. Which durability do you need to see `/map`?
   * TRANSIENT_LOCAL.

</details>
