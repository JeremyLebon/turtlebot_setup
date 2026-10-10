> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/slam.md).

# SLAM

Make a map of the classroom

Make sure that the turtlebot container (turtlebot\_setup) and the turtlebot\_vis container are correctly started. See [Turtlebot3 - startup](/turtlebot3/turtlebot3-startup.md)

Excute the command below in the turtlebot container **on** the turtlebot!

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FFWDwQQKKlT3dIqRxHRzT%2Fimage.png?alt=media&amp;token=e34698e4-a9eb-44a8-a708-ba2859001ccf" alt=""><figcaption></figcaption></figure>

Use a new WSL terminal and connect to the turtlebot-vis container.

Start the command below

```sh
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

Start driving around with the TurtleBot and try to map the room.

When ready, you can save the map with the command below.

{% hint style="warning" %}
It is important not to stop the mapping node of the previous step.
{% endhint %}

```sh
ros2 run nav2_map_server map_saver_cli -f /root/ros_ws/map
```

{% hint style="info" %}
Make sure the selected directory exists.
{% endhint %}

If you want to save the map as a png-file use&#x20;

```sh
ros2 run nav2_map_server map_saver_cli -f /root/ros_ws/map --fmt png
```

Show the map to the lecturer
