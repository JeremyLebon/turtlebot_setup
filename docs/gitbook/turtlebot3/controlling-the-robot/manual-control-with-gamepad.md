# Manual control with gamepad

Plug the USB receiver of the Logitech F710 into the Raspberry Pi of the robot
and switch the gamepad on.

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

{% hint style="info" %}
The switch on the back of the gamepad must be on **X** (XInput mode).
{% endhint %}

Start the gamepad driver **on the robot**: open a terminal inside the robot
container (see [Connect to the turtlebot3](../turtlebot3-startup/connect-to-the-turtlebot3.md))
and run:

```sh
ros2 launch teleop_twist_joy teleop-launch.py joy_vel:=cmd_vel_joy config_filepath:=/root/turtlebot3_ws/joystick_f710.yaml
```

Keep this terminal open (`CTRL + C` stops the gamepad). The bringup must be
running as well.

{% hint style="info" %}
* `joy_vel:=cmd_vel_joy`: the gamepad publishes on `/cmd_vel_joy`, the input
  with the highest priority in twist_mux.
* `joystick_f710.yaml`: which buttons and sticks do what, and the speeds.
* Alternative: status page > **Rijden** > gamepad button (top right).
{% endhint %}

How to control the TurtleBot:

1. Keep **LB** (left shoulder button) pressed - this is the enable button.
2. Use the **left stick** to drive forward/backward and the **right stick** to turn.
3. Keep **RB** pressed as well to drive faster.

{% hint style="info" %}
The gamepad has the highest priority: it always wins over the web page and over
your own nodes (see [Manual control by terminal](manual-control-by-terminal.md)).
{% endhint %}

Try to drive around. This can later be used to map the environment.

Show the progress to the lecturer.
