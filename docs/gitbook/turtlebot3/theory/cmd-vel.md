# Driving the robot (/cmd_vel)

## A speed, not a position

You don't tell the robot **where** to go, you tell it **how fast** to move
*right now*. That is the job of the topic `/cmd_vel` ("command velocity").
The robot keeps that speed until it gets a new command.

So "drive 10 cm" always becomes: drive at speed `v` during a time `t`, then
send speed 0 (or: drive until [odometry](odometry.md) says you did 10 cm).

## The Twist message

On our robot (ROS 2 Humble) `/cmd_vel` is a `geometry_msgs/msg/Twist`:

```
linear:            angular:
  x: 0.1   ← forward (m/s)    x: 0.0
  y: 0.0                      y: 0.0
  z: 0.0                      z: 0.5   ← turn (rad/s), positive = left
```

A **differential drive** robot can only use two of the six numbers:

| field | meaning | Burger max |
|---|---|---|
| `linear.x` | forward (+) / backward (-) | 0.22 m/s |
| `angular.z` | turn left (+) / right (-) | 2.84 rad/s |
| `linear.y`, `linear.z`, `angular.x`, `angular.y` | ignored: the robot cannot drive sideways, fly or roll | - |

Combining both gives a **curve** with radius `R = v / ω`. For example
`linear.x = 0.1`, `angular.z = 0.5` → a circle with a radius of 0.2 m.

How the robot turns this into two wheel speeds is explained in
[Odometry](odometry.md): `v_left = v - ω·L/2`, `v_right = v + ω·L/2`.

{% hint style="info" %}
In the simulation (ROS 2 Jazzy) `/cmd_vel` is a `TwistStamped`: the same
`Twist` inside `msg.twist`, plus a `header` with a time stamp.
{% endhint %}

## The path of a command on our robot

```
 teleop_keyboard ─┐
 Nav2            ─┼─► /cmd_vel      (prio 10) ─┐
 your node       ─┘                            │
 status page ───────► /cmd_vel_web  (prio 50) ─┼─► twist_mux ─► /cmd_vel_out ─► turtlebot3_node ─► OpenCR ─► motors
 gamepad F710 ──────► /cmd_vel_joy  (prio 100)─┘
```

* **twist_mux** passes only the source with the highest priority that sent
  something in the last 0.5 s (see
  [Manual control by terminal](../controlling-the-robot/manual-control-by-terminal.md)).
* `turtlebot3_node` limits the speed to what the robot can do and sends it to
  the OpenCR, which controls the two motors.

## Good habits

* **Publish regularly** (e.g. 10-20 times per second), not just once: twist_mux
  forgets a source after 0.5 s, and a regular stream is safer.
* **Always stop explicitly**: publish a `Twist()` with everything 0 when you are
  done, and also when your node stops (Ctrl+C). Don't count on the robot
  stopping by itself.
* **Start slow**: test with 0.05 m/s and 0.3 rad/s, with the robot on the floor
  and room around it.
* Keep the gamepad nearby: with **LB** you always take over (highest priority).

## Try it

```bash
# Turn slowly to the left, 10 times per second (Ctrl+C to stop)
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.3}}"

# Stop
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"

# What arrives at the robot (after twist_mux)?
ros2 topic echo /cmd_vel_out
```

<details>

<summary>Check yourself</summary>

1. You publish `linear.y = 0.1`. What does the robot do?
   * Nothing: a differential drive robot cannot drive sideways.
2. Which command drives a circle with a radius of 0.5 m at 0.1 m/s, to the right?
   * `linear.x = 0.1`, `angular.z = -0.2` (ω = v / R = 0.1 / 0.5).
3. Your node publishes on `/cmd_vel`, but the robot does not react. A classmate is holding LB on the gamepad. Why?
   * `/cmd_vel_joy` has a higher priority in twist_mux; your commands are ignored.

</details>

Next: [Drive 10cm with a button](../ros2-nodes/drive-10cm-with-a-button.md).
