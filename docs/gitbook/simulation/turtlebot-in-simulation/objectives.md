# Objectives

In this session, the objectives are the following:

* Install and start the simulation container (Gazebo + ROS 2 Jazzy)
* Learn to work with Gazebo (simulator) and load the TurtleBot3 in a world
* Combine Gazebo with ROS 2: nodes, topics and the bridge
* Drive the robot in a simulated environment with `teleop_twist_keyboard`
* Visualise the robot in RViz2: robot model, TF, laser scan, odometry and IMU
* Understand what the robot measures (theory: scan, odometry, IMU, TF, `cmd_vel`, QoS)
* Make your first ROS 2 nodes: subscribe to `/odom` and publish on `/cmd_vel`

{% hint style="info" %}
Next session: map an environment with slam\_toolbox (SLAM) and navigate
autonomously in the mapped environment.
{% endhint %}

{% hint style="warning" %}
**This afternoon you work on the real TurtleBot.** While you still have internet
(eduroam), already download the laptop container for the real robot: see the
Turtlebot3 book, *Installation* (`git clone` of `turtlebot_vis` and
`docker compose pull`, about 4 GB).
{% endhint %}
