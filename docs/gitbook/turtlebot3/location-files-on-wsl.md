# Location files on wsl

{% hint style="warning" %}
Store all files in the `/root/ros2_ws` directory, otherwise you can lose them
when the container is recreated.
{% endhint %}

`/root/ros2_ws` in the `turtlebot-vis` container is the folder `ros2_ws` inside
the cloned `turtlebot_vis` repository on WSL.

In Windows Explorer: **Linux** > your distro (e.g. `Ubuntu-22.04`) > `home` >
your user name > `turtlebot_vis` > `ros2_ws`.

Or type in the address bar of Windows Explorer:

```
\\wsl$\Ubuntu-22.04\home\<user>\turtlebot_vis\ros2_ws
```

{% hint style="info" %}
On the robot there is a `/root/ros2_ws` as well (in the robot container). It is
stored on the robot itself (`~/turtlebot_setup/ros2_ws`) and survives robot
updates - but it is shared by everyone who uses that robot.
{% endhint %}
