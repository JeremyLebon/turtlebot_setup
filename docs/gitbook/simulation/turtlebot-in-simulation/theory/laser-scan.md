# Laser scan (/scan)

## How a lidar works

On top of the TurtleBot is a lidar (Laser Distance Sensor). Inside, a laser and
a receiver turn around (about 5 rotations per second). For every small angle
step the sensor measures the distance to the first object the laser hits. The
result of one rotation is a **2D slice** of the world at the height of the lidar
(about 18 cm above the floor).

```
                    0 rad (front, x)
                         ▲
                 ·  ·  · │ ·  ·  ·
             ·           │           ·
   +π/2   ·              │              ·    3π/2 (or -π/2)
  (left) ·───────────────●───────────────·  (right)
          ·            robot            ·
             ·                       ·
                 ·  ·  ·   ·  ·  ·
                        π (back)
```

{% hint style="warning" %}
The lidar only sees what is **at its own height**. A low object or a table top
above the robot is invisible to it. On the real robot glass and black, shiny
surfaces can also give no (or a wrong) reflection - Gazebo does not simulate that.
{% endhint %}

## The lidar in Gazebo

| | simulation (Gazebo) | real robot (LDS-02) |
|---|---|---|
| scans per second | 5 Hz | ~5 Hz |
| points per rotation | **360**, always the same | ~220-230, varies |
| angular resolution | 1° (0.0175 rad) | ~1.6° |
| angles | 0 → 6.28 rad | |
| range | 0.12 m to **3.5 m** | ~0.16 m to 8 m |
| noise | ±1 cm (gaussian, added by Gazebo) | real noise |
| frame | `base_scan` (see [TF](tf.md)) | `base_scan` |

## The LaserScan message

`/scan` is of type `sensor_msgs/msg/LaserScan`:

| field | meaning |
|---|---|
| `header.stamp` | time of the measurement (simulation time) |
| `header.frame_id` | `base_scan`: the distances are measured from the centre of the lidar |
| `angle_min`, `angle_max` | angle of the first and the last point (rad) |
| `angle_increment` | angle between two points (rad) |
| `range_min`, `range_max` | limits of the sensor (m) |
| `ranges[]` | the distances (m), one per angle step |
| `intensities[]` | strength of the reflection |

The **index** `i` in `ranges[]` belongs to the angle:

```
angle(i) = angle_min + i * angle_increment
```

and the other way around, the index for a given angle:

```
i = round((angle - angle_min) / angle_increment)
```

Index `0` is the **front** of the robot, the angle grows **counterclockwise**:
in the simulation index 90 is the **left** side, 180 the **back**, 270 the **right**.

{% hint style="info" %}
On the real robot the number of points is not always the same (220, 221, ...).
Code with fixed indices like `ranges[90]` works in the simulation but not on
the real robot. Calculate the index from `angle_increment`, or use
`len(msg.ranges) // 4` - then your code works on both.
{% endhint %}

## Invalid values

Not every angle gives a good measurement. In `ranges[]` you can find:

* `inf` - nothing within range (in the simulation: nothing within 3.5 m)
* `nan` - no measurement for that angle (happens on the real robot)
* values below `range_min` - no valid echo

Always filter these before you calculate a mean or a minimum, for example:

```python
valid = [r for r in msg.ranges if math.isfinite(r) and r >= msg.range_min]
```

## From distance and angle to a point (x, y)

A lidar point is given in **polar coordinates** (distance `r`, angle `θ`). To
get the point in the frame of the lidar (`base_scan`):

```
x = r * cos(θ)        (forward)
y = r * sin(θ)        (left)
```

This is exactly what RViz2 does to draw the red dots. To place the points in the
world, RViz2 also needs the position of the lidar on the robot and the position
of the robot in the world: that is [TF](tf.md).

## Try it

```bash
ros2 topic hz /scan                     # how many scans per second?
ros2 topic echo /scan --once --field angle_increment
ros2 topic echo /scan --once --field ranges
```

Put the robot in front of a wall in Gazebo and look at `ranges[0]`. Then
drive 0.5 m back: does the value change by 0.5?

<details>

<summary>Check yourself</summary>

1. `angle_increment` is 0.0175 rad. How many degrees is that, and how many points per rotation?
   * 0.0175 × 57.3 ≈ 1°; 2π / 0.0175 ≈ 360 points.
2. Which index points to the right?
   * 270 (angle 3π/2, or -π/2).
3. The robot is in an empty part of the world. Most values in `ranges` are `inf`. Is the lidar broken?
   * No: there is nothing within 3.5 m.

</details>

Exercise: [Here come the sensors](../here-come-the-sensors.md).

Next: [Odometry (/odom) and wheels](odometry.md).
