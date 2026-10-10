# SLAM

Make a map of the classroom.

There are two ways. Do **way 1 first** - that's where you learn what happens.

## Way 1 - yourself, with ROS 2 commands

Make sure the bringup runs on the robot and the `turtlebot-vis` container on
your laptop is started (see [Turtlebot3 - startup](turtlebot3-startup.md)).

In the **robot** container (web terminal or SSH):

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

In a new WSL terminal, in the **turtlebot-vis** container on your laptop:

```sh
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

RViz2 opens with the map being built. Drive around (gamepad, status page or
`teleop_keyboard`) and try to map the whole room. Drive slowly and turn slowly:
Cartographer needs time to match the lidar scans.

When ready, save the map. Make the directory first:

```sh
mkdir -p /root/ros2_ws/maps
ros2 run nav2_map_server map_saver_cli -f /root/ros2_ws/maps/classroom --free 0.196 --occ 0.65
```

{% hint style="warning" %}
* Don't stop the mapping (Cartographer) before the map is saved.
* `--free 0.196`: otherwise grey (unknown) cells are loaded as free later on,
  and Nav2 plans paths through unexplored space.
{% endhint %}

You get two files: `classroom.pgm` (the image) and `classroom.yaml` (resolution,
origin, thresholds). Open the `.pgm` in VS Code or Windows to look at it.

{% hint style="info" %}
Here Cartographer runs on your laptop and receives all lidar data over the wifi.
That works, but it is heavy for the wifi and your laptop.
{% endhint %}

## Way 2 - with the status page

Status page > **Rijden** > **Kaart maken**: the bringup and Cartographer start
**on the robot**. You see the map grow live with the robot and the lidar points.
Give the map a name and click the save button (disk icon).

The map is stored **on the robot** and can be chosen directly on the
**Navigatie** tab.

Show the map to the lecturer.
