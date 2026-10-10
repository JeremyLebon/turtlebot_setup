> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/controlling-the-robot/manual-control-by-terminal.md).

# Manual control by terminal

Open a new WSL terminal.

Connect to the turtlebot-vis container.

<details>

<summary>Solution</summary>

```
docker exec -it turtlebot-vis bash
```

</details>

Start the teleop command.

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

```sh
ros2 run turtlebot3_teleop teleop_keyboard
```

{% hint style="success" %}
Other keys are used for controlling the turtlebot, then the previous commands
{% endhint %}

You should see the turtlebot move in RViz2
