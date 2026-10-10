# Manual control by terminal

Open a new WSL terminal and connect to the `turtlebot-vis` container.

Solution

```
docker exec -it turtlebot-vis bash
```

Start the teleop command.

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

```sh
ros2 run turtlebot3_teleop teleop_keyboard
```

{% hint style="success" %}
Other keys are used for controlling the TurtleBot than in the previous commands:
read the instructions in the terminal.
{% endhint %}

You should see the TurtleBot move in RViz2.

## Who is in control? (twist_mux)

Several things can drive the robot at the same time. The robot decides with
**twist_mux** - the highest priority wins:

| Source | Topic | Priority |
|---|---|---|
| Gamepad (F710) | `/cmd_vel_joy` | 100 (highest) |
| Status page (arrows on Rijden / Navigatie) | `/cmd_vel_web` | 50 |
| Your own nodes, Nav2, teleop_keyboard | `/cmd_vel` | 10 |

As long as a higher source sends commands, yours are ignored. 0.5 s after it
stops, the next one takes over again. So with the gamepad or the web page you
can **always** take over the robot.

{% hint style="info" %}
You can also drive from the status page: **Rijden**, arrows bottom-left (keep
pressed), or the keyboard (arrows / WASD, space = stop).
{% endhint %}
