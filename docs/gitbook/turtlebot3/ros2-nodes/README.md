# ROS2 nodes

You write your ROS 2 nodes **on your laptop**, in your own `turtlebot-vis`
container. The node talks to the robot over Zenoh, exactly like RViz2 and
teleop. The bringup must be running on the robot.

## Open the container in VS Code

VS Code > **Remote Explorer** > **WSL** (Ubuntu-22.04) > **Dev Containers** >
`turtlebot-vis` > attach. When asked to open a folder, choose `/root/ros2_ws`.

{% hint style="info" %}
Same steps as in the simulation ([The first ros2 node](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node)),
but now the container is `turtlebot-vis`. VS Code may ask to install the Python
extension in the container: say yes.
{% endhint %}

## Make and run a script

1. Make the script in `/root/ros2_ws`, for example `sub_scan.py`.
2. Open a terminal in VS Code (**Terminal > New Terminal**): it runs inside the container.
3. Run it:

```sh
cd /root/ros2_ws
python3 sub_scan.py
```

`CTRL + C` stops the node.

{% hint style="warning" %}
Store your code in `/root/ros2_ws`: that is the folder `turtlebot_vis/ros2_ws`
on your laptop (see [Location files on WSL](../location-files-on-wsl.md)).
Anything you store elsewhere in the container can be lost.
{% endhint %}

<details>

<summary>Advanced: run a node on the robot itself</summary>

The robot container `turtlebot_<nr>` also has a `/root/ros2_ws`
(`~/turtlebot_setup/ros2_ws` on the robot). It is **shared by everyone who uses
that robot**, and VS Code over SSH needs internet on the robot to install its
server. Only use it when your lecturer asks for it.

</details>
