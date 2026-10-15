# Turtlebot in simulation

Before you work with the real TurtleBot3, you start with a **simulated** one.
In the simulator **Gazebo** a virtual TurtleBot3 Burger drives around in a
virtual world, with a simulated lidar, IMU and wheels. ROS 2 can't see the
difference: the robot publishes the same topics (`/scan`, `/odom`, `/imu`,
`/tf`, ...) and listens to `/cmd_vel`, just like the real robot.

Why first in simulation?

* **No hardware needed**: everything runs in a Docker container on your laptop.
* **Safe**: a crash into a wall costs nothing.
* **Repeatable**: the same world, the same start position, every time.
* **Same ROS 2 skills**: the commands, tools and nodes you learn here work on
  the real robot as well (with a few differences, see
  [Simulation vs. real robot](simulation-vs-real-robot.md)).

## What you will do in this chapter

1. [Objectives](turtlebot-in-simulation/objectives.md) - what you should be able to do at the end
2. [Tools](turtlebot-in-simulation/tools.md) - Gazebo and RViz2: what is the difference?
3. [Startup](turtlebot-in-simulation/startup.md) - load the TurtleBot3 in a Gazebo world
4. [Theory: what the robot measures](turtlebot-in-simulation/theory.md) - scan, odometry, IMU, TF, `cmd_vel` and QoS
5. [Moving the turtlebot](turtlebot-in-simulation/moving-the-turtlebot.md) - drive with the keyboard, look at `/cmd_vel`
6. [Show me the robot](turtlebot-in-simulation/show-me-the-robot.md) - the robot model and TF in RViz2
7. [Here come the sensors](turtlebot-in-simulation/here-come-the-sensors.md) - lidar, odometry and IMU in RViz2

After this chapter you write your own ROS 2 nodes in
[The first ros2 node](the-first-ros2-node.md).

{% hint style="info" %}
Everything runs in the container `gazebo_turtlebot_cont` (see
[Installation](installation.md)). Open a terminal in it with
`docker exec -it gazebo_turtlebot_cont bash` - you will need several terminals
at the same time (Gazebo, teleop, RViz2, ...).
{% endhint %}
