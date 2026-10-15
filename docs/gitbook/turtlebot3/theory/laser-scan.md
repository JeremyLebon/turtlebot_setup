# Laser scan (/scan)

## How a lidar works

On top of the TurtleBot is a **LDS-02** lidar (Laser Distance Sensor). Inside, a laser and a receiver turn around (about 5 rotations per second). For every small angle step the sensor measures the distance to the first object the laser hits. The result of one rotation is a **2D slice** of the world at the height of the lidar (about 18 cm above the floor).

```
                    0 rad (front, x)
                         ▲
                 ·  ·  · │ ·  ·  ·
             ·           │           ·
   +π/2   ·              │              ·    -π/2
  (left) ·───────────────●───────────────·  (right)
          ·            robot            ·
             ·                       ·
                 ·  ·  ·   ·  ·  ·
                       ±π (back)
```

{% hint style="warning" %}
The lidar only sees what is **at its own height**. A low object (a cable, a foot of a chair) or a table top above the robot is invisible to it. Glass and black, shiny surfaces can also give no (or a wrong) reflection.
{% endhint %}

## LDS-02 on our robot

|                      | LDS-02                                            |
| -------------------- | ------------------------------------------------- |
| rotations per second | \~5 Hz → `/scan` arrives about 5 times per second |
| points per rotation  | \~220-230 (not always exactly the same!)          |
| angular resolution   | \~1.6° per point                                  |
| range                | \~0.16 m to 8 m                                   |
| frame                | `base_scan` (see [TF](tf.md))                     |

## The LaserScan message

`/scan` is of type `sensor_msgs/msg/LaserScan`:

| field                    | meaning                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| `header.stamp`           | time of the measurement                                              |
| `header.frame_id`        | `base_scan`: the distances are measured from the centre of the lidar |
| `angle_min`, `angle_max` | angle of the first and the last point (rad)                          |
| `angle_increment`        | angle between two points (rad)                                       |
| `range_min`, `range_max` | limits of the sensor (m)                                             |
| `ranges[]`               | the distances (m), one per angle step                                |
| `intensities[]`          | strength of the reflection (here: the confidence of the point)       |

The **index** `i` in `ranges[]` belongs to the angle:

```
angle(i) = angle_min + i * angle_increment
```

and the other way around, the index for a given angle:

```
i = round((angle - angle_min) / angle_increment)
```

Index `0` is the **front** of the robot, the angle grows **counterclockwise**: a quarter of the array further is the **left** side, half way is the **back**, three quarters is the **right**.

{% hint style="info" %}
Because the number of points is not always the same (220, 221, ...), never use fixed indices like `ranges[55]` for "left". Calculate the index from `angle_increment`, or use `len(msg.ranges) // 4`.
{% endhint %}

## Invalid values

Not every angle gives a good measurement. In `ranges[]` you can find:

* `nan` - no measurement for that angle
* `inf` - nothing within range
* `0.0` or a value smaller than \~0.12 m - no valid echo

Always filter these before you calculate a mean or a minimum, for example:

```python
valid = [r for r in msg.ranges if math.isfinite(r) and r > 0.12]
```

## From distance and angle to a point (x, y)

A lidar point is given in **polar coordinates** (distance `r`, angle `θ`). To get the point in the frame of the lidar (`base_scan`):

```
x = r * cos(θ)        (forward)
y = r * sin(θ)        (left)
```

This is exactly what RViz2 does to draw the red dots. To place the points on the map, RViz2 also needs the position of the lidar on the robot and the position of the robot in the world: that is [TF](tf.md).

## QoS: Best Effort

The lidar publishes with **Best Effort** reliability: if a message is lost on the wifi, it is not sent again (the next scan arrives 0.2 s later anyway). With the standard DDS middleware a subscriber that asks for **Reliable** does not match and receives nothing (our robot uses Zenoh, which is less strict). That is why you set Best Effort in RViz2 and in your own node. More in [QoS](qos.md).

## Try it

```bash
ros2 topic hz /scan                     # how many scans per second?
ros2 topic echo /scan --once --field angle_increment
ros2 topic echo /scan --once --field ranges
```

<details>

<summary>Check yourself</summary>

1. `angle_increment` is 0.0283 rad. How many degrees is that, and how many points do you expect per rotation?
   * 0.0283 × 57.3 ≈ 1.6°; 2π / 0.0283 ≈ 222 points.
2. Which index (approximately) points to the left if `len(ranges)` is 224?
   * 224 / 4 = 56 (angle +π/2).
3. A chair leg is 0.10 m in front of the lidar. What do you see in `ranges`?
   * Nothing useful: it is below the minimum range, you get `0.0`/`nan`.

</details>

Next: [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic/).
