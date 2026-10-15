# Session 3 - SLAM and navigation

In this session the robot learns its environment and drives on its own:

* **SLAM** (Simultaneous Localization And Mapping): the robot makes a **map**
  of the room with its lidar, while it keeps track of where it is on that map.
* **Navigation** with **Nav2**: on that map you give a goal, the robot plans a
  path and drives there by itself, around obstacles.

You do it twice: first in the **simulation** (safe, the same world every time),
then on the **real robot**.

1. [Part 1 - In simulation](simulation/README.md) - slam\_toolbox and Nav2 in Gazebo
2. [Part 2 - On the real robot](real-robot/README.md) - Cartographer and Nav2 on the TurtleBot3

{% hint style="info" %}
Theory you need: **TF - map and odom** (why there is a `map` frame next to
`odom`) and **Odometry - why it drifts**, in the theory chapter of the
simulation and Turtlebot3 books.
{% endhint %}
