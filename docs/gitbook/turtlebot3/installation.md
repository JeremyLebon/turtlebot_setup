# Installation

On your laptop you work in the **`turtlebot-vis`** container: RViz2, teleop and
your own ROS 2 nodes, connected to the robot over Zenoh. Install it **before the
lab, on a network with internet** (eduroam, at home).

{% hint style="danger" %}
The robot wifi `TB-AP-<nr>` has no (or only slow) internet. The container image
is about **4 GB**: download it before you connect to the robot.
{% endhint %}

You need the same as for the simulation: **WSL** (Ubuntu 22.04) with **Docker**.

## Clone the repository

Open a WSL terminal:

```sh
git clone https://github.com/JeremyLebon/turtlebot_vis.git
```

{% hint style="info" %}
Already cloned in a previous year? Update it: `cd turtlebot_vis`,
`git checkout .env` (throws away your old robot number, otherwise `git pull`
refuses), `git pull`, `git submodule update --init`. The old version (DDS) can't
talk to the robots anymore.
{% endhint %}

## Download the container image

```sh
cd turtlebot_vis
docker compose pull
```

This downloads the ready-made image (much faster than building it yourself).

Check that it is there:

```sh
docker images | grep turtlebot-rpi5-vis
```

You should see `nobel86/turtlebot-rpi5-vis` with tag `zenoh` (about 4 GB).

## Where your files are

Your own code goes in the folder `turtlebot_vis/ros2_ws`: inside the container
that is `/root/ros2_ws`. Files there survive a restart of the container. See
[Location files on WSL](location-files-on-wsl.md).

{% hint style="success" %}
Done? Read [Turtlebot3 in the real world](turtlebot3-in-the-real-world.md)
(the lab setup and the objectives). In the lab you continue with
[Turtlebot3 - startup](turtlebot3-startup/): setting your robot number and
starting the container happens in
[Setup laptop (student)](turtlebot3-startup/setup-laptop-student.md).
{% endhint %}
