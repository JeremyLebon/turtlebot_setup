# Driving the robot (/cmd_vel)

## A speed, not a position

You don't tell the robot **where** to go, you tell it **how fast** to move
*right now*. That is the job of the topic `/cmd_vel` ("command velocity").

So "drive 10 cm" always becomes: drive at speed `v` during a time `t`, then
send speed 0 (or: drive until [odometry](odometry.md) says you did 10 cm).

## The TwistStamped message

In the simulation (ROS 2 Jazzy) `/cmd_vel` is a `geometry_msgs/msg/TwistStamped`:
a `header` (time stamp + frame) and a `twist` with the speeds.

```
header:
  stamp: ...
  frame_id: base_link
twist:
  linear:            angular:
    x: 0.1   ← forward (m/s)    x: 0.0
    y: 0.0                      y: 0.0
    z: 0.0                      z: 0.5   ← turn (rad/s), positive = left
```

That is why `teleop_twist_keyboard` is started with `-p stamped:=true`.

A **differential drive** robot can only use two of the six numbers:

| field | meaning | real Burger max |
|---|---|---|
| `twist.linear.x` | forward (+) / backward (-) | 0.22 m/s |
| `twist.angular.z` | turn left (+) / right (-) | 2.84 rad/s |
| other fields | ignored: the robot cannot drive sideways, fly or roll | - |

{% hint style="warning" %}
Gazebo does **not** limit the speed: you can drive the simulated robot at 1 m/s.
The real Burger can do at most 0.22 m/s. Keep your code within the real limits.
{% endhint %}

Combining both gives a **curve** with radius `R = v / ω`. For example
`linear.x = 0.1`, `angular.z = 0.5` → a circle with a radius of 0.2 m.

How this becomes two wheel speeds is explained in [Odometry](odometry.md):
`v_left = v - ω·L/2`, `v_right = v + ω·L/2`.

## The path of a command

```
 teleop_twist_keyboard ─┐
 Nav2                  ─┼─► /cmd_vel ─► ros_gz_bridge ─► Gazebo DiffDrive plugin ─► wheels
 your node             ─┘   (TwistStamped)
```

In the simulation **everyone publishes on the same topic**: if two nodes send
`/cmd_vel` at the same time, the robot jerks between both commands. On the real
robot a *twist_mux* decides who is in control (see
[Simulation vs. real robot](../../simulation-vs-real-robot.md)).

{% hint style="info" %}
On the real robot (ROS 2 Humble) `/cmd_vel` is a plain `Twist`, without header.
Code from the simulation needs a small change.
{% endhint %}

## Good habits

* **Publish regularly** (e.g. 10-20 times per second), not just once.
* **Always stop explicitly**: publish a message with all speeds 0 when you are
  done, and also when your node stops (Ctrl+C).
* **Start slow** and stay within the real limits (0.22 m/s, 2.84 rad/s): then your
  code also works on the real robot.

## Try it

```bash
# Turn slowly to the left, 10 times per second (Ctrl+C to stop)
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/TwistStamped "{twist: {angular: {z: 0.3}}}"

# Stop
ros2 topic pub --once /cmd_vel geometry_msgs/msg/TwistStamped "{}"

# Which type does the robot expect?
ros2 topic info /cmd_vel
```

<details>

<summary>Check yourself</summary>

1. You publish `twist.linear.y = 0.1`. What does the robot do?
   * Nothing: a differential drive robot cannot drive sideways.
2. Which command drives a circle with a radius of 0.5 m at 0.1 m/s, to the right?
   * `linear.x = 0.1`, `angular.z = -0.2` (ω = v / R = 0.1 / 0.5).
3. Your node publishes a `Twist` (without header) on `/cmd_vel` in the simulation. What happens?
   * Nothing, or an error about the type: the simulation expects `TwistStamped`.

</details>

Exercise: [Moving the turtlebot](../moving-the-turtlebot.md).

Next: [QoS - Quality of Service](qos.md).
