# ROS2 nodes

To make ROS 2 nodes in Python, 2 ways can be used:

1. **On your laptop** - in the `turtlebot-vis` container: VS Code > Remote
   Explorer > WSL > Dev Containers > `turtlebot-vis`. Store your code in
   `/root/ros2_ws`.
2. **On the robot** - in the robot container `turtlebot_<nr>`: VS Code > Remote
   Explorer > SSH (`turtlebot@10.0.<nr>.10`) > attach to the container. Store
   your code in `/root/ros2_ws` there as well (on the robot this is
   `~/turtlebot_setup/ros2_ws`).

{% hint style="info" %}
Both `ros2_ws` folders survive restarts and robot updates. Anything you store
elsewhere in a container can be lost.
{% endhint %}

{% hint style="warning" %}
On the robot: build your own packages with `colcon build` in `/root/ros2_ws`.
The overlay (`install/setup.bash`) is sourced automatically in every new terminal.
{% endhint %}
