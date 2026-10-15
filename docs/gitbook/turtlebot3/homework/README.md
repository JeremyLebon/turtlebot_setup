# Homework

Finish these tasks **at home, before the next session**. You have no robot at
home, so you work in the **simulation**: the container `gazebo_turtlebot_cont`
from the simulation book (Gazebo + ROS 2 Jazzy).

{% hint style="warning" %}
* Store your scripts in `/home/dockeruser/dev_ws` (the `dev_ws` folder of the
  `ros2-jazzy-gazebo-turtlebot` repository), not in the `turtlebot-vis` container:
  without a robot, the `turtlebot-vis` container has no Zenoh router to talk to.
* Simulation vs. real robot: in the simulation `/cmd_vel` is a `TwistStamped`,
  the lidar has 360 points, and there is no `/battery_state`.
{% endhint %}

## Overview

1. [Startup at home](startup-at-home.md) - start the simulation and VS Code
2. [Task 1 - Obstacle alarm](task-1-obstacle-alarm.md) - warning when something is close in front (extension: four sectors)
3. [Task 2 - Battery warning](task-2-battery-warning.md) - with fake sensors (`/sim/battery_state`)
4. [Task 3 - Drive exactly 1 m with odometry](task-3-drive-1-m-with-odometry.md) - `/odom` instead of time
5. [Task 4 - Theory](task-4-theory.md) - the Check yourself questions

## Hand in

Upload on Toledo, before the next session:

* your Python scripts of task 1, 2 and 3;
* a screenshot of the terminal output of each script;
* your answers of task 4.

{% hint style="success" %}
Next session: SLAM (make a map) and autonomous navigation with the real robot.
{% endhint %}
