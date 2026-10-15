# ROS2 - Simulation - Turtlebot - Gazebo

_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/simulation/`._

---

## 1. Installation  `[ongewijzigd]`

<sub>installation.md</sub>


For the lab WSL should already be installed.

Start WSL or the selected Ubuntu distro by searching the windows start menu.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3JbsPADcSfJN3Ymg4Fqs%2Fimage.png?alt=media&amp;token=c2fe29f7-1b47-4029-b729-5cb3ae869028" alt=""><figcaption></figcaption></figure>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3ZxKU4oI7Wk0x6MF1A3y%2Fimage.png?alt=media&amp;token=d0def977-488e-4abb-9c78-c9615f0cc2bc" alt=""><figcaption></figcaption></figure>

Clone the docker image repo

```sh
git clone https://github.com/JeremyLebon/ros2-jazzy-gazebo-turtlebot
```

Go inside the directory

```sh
cd ros2-jazzy-gazebo-turtlebot
```

Build the docker image to a docker container with the docker compose command

```sh
docker compose build
```

{% hint style="info" %}
This can take while.&#x20;
{% endhint %}

When build without errors the docker container can be started.

```sh
docker compose up
```

This should start without any error.

Open a second wsl terminal and check if the docker container is active with

```sh
docker ps
```

You should see that one container is active with the name `gazebo_turtlebot_cont`

Output:

```
CONTAINER ID   IMAGE                              COMMAND                  CREATED        STATUS          PORTS     NAMES
86c4097429f9   ros2-jazzy-gazebo-turtlebot-ros2   "/ros_entrypoint.sh …"   15 hours ago   Up 18 seconds             gazebo_turtlebot_cont
```

Now in the second terminal make connection with the docker container by typing:

```sh
docker exec -it gazebo_turtlebot_cont bash
```

{% hint style="info" %}
The `docker exec` lets you make a connection with the docker container via bash. Important is that the container name should be correct. With `TAB` it is normally autocompleted.
{% endhint %}

---

## 2. Turtlebot in simulation  `[gewijzigd]`

<sub>turtlebot-in-simulation.md</sub>


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
4. [Moving the turtlebot](turtlebot-in-simulation/moving-the-turtlebot.md) - drive with the keyboard, look at `/cmd_vel`
5. [Show me the robot](turtlebot-in-simulation/show-me-the-robot.md) - the robot model and TF in RViz2
6. [Here come the sensors](turtlebot-in-simulation/here-come-the-sensors.md) - lidar, odometry and IMU in RViz2
7. [Theory: what the robot measures](turtlebot-in-simulation/theory.md) - scan, odometry, IMU, TF, `cmd_vel` and QoS

After this chapter you write your own ROS 2 nodes in
[The first ros2 node](the-first-ros2-node.md).

{% hint style="info" %}
Everything runs in the container `gazebo_turtlebot_cont` (see
[Installation](installation.md)). Open a terminal in it with
`docker exec -it gazebo_turtlebot_cont bash` - you will need several terminals
at the same time (Gazebo, teleop, RViz2, ...).
{% endhint %}

---

### 3. Objectives  `[gewijzigd]`

<sub>turtlebot-in-simulation/objectives.md</sub>


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
Turtlebot3 book, *Setup laptop (student)* (`git clone` of `turtlebot_vis` and
`docker compose pull`, about 4 GB).
{% endhint %}

---

### 4. Tools  `[gewijzigd]`

<sub>turtlebot-in-simulation/tools.md</sub>


### Gazebo

Gazebo is an open-source 3D robot simulator that allows users to accurately and efficiently simulate populations of robots in complex indoor and outdoor environments. It provides a robust physics engine and models for sensors and actuators. In the ROS 2 ecosystem, the newer version (Gazebo Sim) is the standard for testing robot autonomy, relying on the `ros_gz_bridge` for real-time communication with the ROS control stack.

<div data-full-width="false" data-with-frame="true"><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAqtGNSo6CAyvDoyLjVAR%2Fimage.png?alt=media&amp;token=9e38f2e4-8593-4c06-8139-dd1ecaa342b1" alt=""><figcaption></figcaption></figure></div>

### Rviz

RViz (ROS Visualization) isn't a simulator but a 3D visualization tool within the ROS ecosystem, used to display sensor data, robot models, and algorithm output (like navigation paths and maps) published on ROS topics. It's essential for debugging and monitoring the state of any robot—real or simulated—by aggregating and graphically rendering data streams in a unified 3D environment.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9MoVmrG1mIOWkqk0T8HC%2Fimage.png?alt=media&amp;token=8855bc88-bff9-46e6-a32c-03a46f5601fc" alt=""><figcaption></figcaption></figure>

---

### 5. Startup  `[gewijzigd]`

<sub>turtlebot-in-simulation/startup.md</sub>


Open a new terminal (Ubuntu 22.04).

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fsu1ojyU78ot109TUCruT%2Fimage.png?alt=media&amp;token=bd97d707-024e-45cb-b7f4-bdfc6f29c983" alt=""><figcaption></figcaption></figure>

Connect to the running Docker container with the command below.

```sh
docker exec -it gazebo_turtlebot_cont bash
```

Select the `burger` turtlebot3 as loaded model in Gazebo with the following command
(in this container it is already the default, but on other systems you need it)

```sh
export TURTLEBOT3_MODEL=burger
```

## Load the turtlebot in the turtlebot world

Start `ros2 launch` file with the command below. Normally, Gazebo should start with the standard turtle world.

{% hint style="info" %}
The  `ros2 launch` command lets you start several ros2 nodes with one command.&#x20;
{% endhint %}

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

Normally, the world below should be loaded. Try to find the turtlebot3 with the mouse and scrolling.

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAqtGNSo6CAyvDoyLjVAR%2Fimage.png?alt=media&amp;token=9e38f2e4-8593-4c06-8139-dd1ecaa342b1" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ45E9208uQDSv4e1ceNe%2Fimage.png?alt=media&amp;token=2833a4bb-a0e9-4f06-97a7-0efef922290c" alt=""><figcaption></figcaption></figure></div>

With `CTRL+C` in the terminal, Gazebo and the ros2 launch are stopped.

## Load the turtlebot in the house world

Try the following command to drop the turtle in the house environment.

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
</strong></code></pre>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FITbPVgiVyF6yDsQRFA21%2Fimage.png?alt=media&amp;token=986a0d24-241a-42b1-b2c8-73de09b6c412" alt=""><figcaption></figcaption></figure>

With `CTRL+C` in the terminal, Gazebo and the ros2 launch are stopped.

---

### 6. Moving the turtlebot  `[gewijzigd]`

<sub>turtlebot-in-simulation/moving-the-turtlebot.md</sub>


{% hint style="info" %}
Theory: [Driving the robot (/cmd_vel)](theory/cmd-vel.md).
{% endhint %}

Load the turtlebot again in the turtlebot world.

<pre><code><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

Open a new terminal and connect to the docker container. Try to find how many ros2 nodes are running.&#x20;

<details>

<summary>Solution</summary>

```
ros2 node list
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIEDot7g4vqcm8WO2u1Ya%2Fimage.png?alt=media&amp;token=ae0b6e4d-6ee9-4f88-8bfc-160905719838" alt=""><figcaption></figcaption></figure>

</details>

Open a new terminal and connect the docker container.

Add the following command to start the `teleop_twist_keyboard` ros2 node. This will publish the cmd\_vel (command\_velocity) topic. The turtlebot is subscribed to this topic. And will drive accordingly.

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

{% hint style="info" %}
Important the terminal should be selected when controlling the robot.
{% endhint %}

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FrxY13HeLjcAf3rG2FdHB%2Fimage.png?alt=media&amp;token=69ed0886-302c-4210-8a52-13db4aacc6d5" alt=""><figcaption></figcaption></figure>

Try to drive the robot around in the world. Maybe in the beginning, try to lower the speed by tapping z.

Open a new terminal and check with ros2 topic list which ros2 topics are available.

Try to show the actual `cmd_vel` topic. Important the robot should be driving to see the cmd\_vel topic.

<details>

<summary>Solution</summary>

```
ros2 topic echo /cmd_vel
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FEMWz3atS5skfBlaTVDRo%2Fimage.png?alt=media&amp;token=371b76d8-124a-4408-9f3e-9575a32f0a7e" alt=""><figcaption></figcaption></figure>

</details>

Try to lookup the location of the turtlebot with the `ros2 topic echo` command. Which topic has the location information?&#x20;

<details>

<summary>Solution</summary>

The /odom topic contains the location and the orientation of the turtlebot

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FqwYP0hPk3b74vzVfqxlc%2Fimage.png?alt=media&amp;token=d29b71eb-a7b0-40aa-88f5-9f50326c5f9b" alt=""><figcaption></figcaption></figure>

</details>

Try to ride around and look at the location. Start `rqt` and try to visualize the x and y coordinates in a graph.

<details>

<summary>Solution</summary>

Open a new terminal and add the command below to start rqt

```
rqt
```

Select the topic with Plugins > Topics > Topic monitor.

Select the graph with Plugins > Visualization > Plot. Type the field you want to
plot, for example `/odom/pose/pose/position/x`, and click **+** (do the same for `y`).

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FFDOM01gw9GcX0mVKRweZ%2Fimage.png?alt=media&amp;token=8ac28a21-6e1d-4b3a-870a-9acca6687e53" alt=""><figcaption></figcaption></figure>

</details>

Close rqt with `CTRL+C` in the terminal.

---

### 7. Show me the robot  `[gewijzigd]`

<sub>turtlebot-in-simulation/show-me-the-robot.md</sub>


{% hint style="info" %}
Theory: [TF - coordinate frames](theory/tf.md).
{% endhint %}

Make sure the turtlebot3 is still running in the Gazebo environment

Open a new terminal and connect to the running Docker container.

Add the following command

```
rviz2
```

The window below should pop up.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FhaAGPs4C7DjKS2qe2xN5%2Fimage.png?alt=media&amp;token=1ffda22a-0317-47ae-9aa7-c0af2c4cd625" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
In the current configuration, the map frame doesn't exist, which is why the Global Status gives an error
{% endhint %}

## Configuration Rviz

### Change fixed frame

Select `odom` as Fixed Frame.

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FKXOe51sV1ksvoZJN7nLr%2Fimage.png?alt=media&amp;token=87ae629c-6ccb-4e36-ba60-0f7b67f5cabf" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FO0rwUJ8wsFlfi24sITSz%2Fimage.png?alt=media&amp;token=e8ec05dc-f554-478c-add2-97a2c2a45ee6" alt=""><figcaption></figcaption></figure></div>

### Show the robot

Click Add and select *RobotModel*

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJe8X9yBRn1ZbRyZjsEtA%2Fimage.png?alt=media&amp;token=f12aca05-c6c9-4321-b22d-d102ac52b3ee" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FgMsWwphlAlfnWQS48yaA%2Fimage.png?alt=media&amp;token=2ec1ea03-4e8f-41f7-b71d-7c472b3b4651" alt=""><figcaption></figcaption></figure></div>

Collapse the item *RobotModel* and select the topic `/robot_description`

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F7FosZqIfyqronRM8un4I%2Fimage.png?alt=media&amp;token=7a2b0b76-c4f0-4e13-8244-3e121baa3172" alt=""><figcaption></figcaption></figure>

Normally, the robot should be visible when using the zoom in.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIdOCpZgS4iR4CyX1UwDd%2Fimage.png?alt=media&amp;token=ec1799b5-0c1e-4b87-a7a1-50f14569639d" alt=""><figcaption></figcaption></figure>

## TF

### Visualise the TF

Click Add and select *TF*

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJe8X9yBRn1ZbRyZjsEtA%2Fimage.png?alt=media&amp;token=f12aca05-c6c9-4321-b22d-d102ac52b3ee" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F4CuCZzvfQkOUeN4pBHE4%2Fimage.png?alt=media&amp;token=ce253cf7-07b8-4a69-a42a-181d4f7e78c6" alt=""><figcaption></figcaption></figure></div>

You can now see the different links/frames of the robot.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fr4W55Akx5O7qhX61T0Dz%2Fimage.png?alt=media&amp;token=15a60afc-ffca-4838-a745-3e6a5fb86b25" alt=""><figcaption></figcaption></figure>

Collapse the item *TF* and check the *Show Names* item.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FHyhk98CJoACIRjY363hE%2Fimage.png?alt=media&amp;token=82541c34-d3b7-4777-9f80-7573eeb0964a" alt=""><figcaption></figcaption></figure>

Collapse the item TF further to see the different frames (item *Frames*). Enable and disable them to see where the frames are located. Select the *Tree* item to see how the links/frames are connected.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FBFxig56bOl0d8oe7CKhm%2Fimage.png?alt=media&amp;token=f5ac1010-62f6-4795-ab86-a7484c82f80d" alt=""><figcaption></figcaption></figure>

Enable the *base\_link, base\_scan, odom, wheel\_left\_link and wheel\_right\_link*.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FLuhqFfFNhOJHb6C5RK2h%2Fimage.png?alt=media&amp;token=85e16ef5-74ee-4d00-8292-ae0669f78db7" alt=""><figcaption></figcaption></figure>

Drive around with the robot (with the teleop\_twist\_keyboard node). You should see the wheels/frames turning around. Also, look at the odom frame.

<details>

<summary>Controlling the robot command</summary>

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

</details>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F2km8tPYrLAF4FyaX5prX%2FRobot_tf_demo.gif?alt=media&amp;token=1a0cb1e7-8af4-4b0a-8cb9-e81d4828c1a1" alt=""><figcaption></figcaption></figure>

{% hint style="info" %}
The tf2 ros2 library calculates all the frames and joints at very high rate.
{% endhint %}

### Echo the /tf topic

Use the following command to see a list of the ros2 topics. Use a new terminal if needed.

```
ros2 topic list
```

Output

```
/clicked_point
/clock
/cmd_vel
/goal_pose
/imu
/initialpose
/joint_states
/odom
/parameter_events
/robot_description
/rosout
/scan
/tf
/tf_static
```

{% hint style="info" %}
The /tf topic stands for the transformations of all the frames/links.&#x20;
{% endhint %}

Visualise the /tf topic with ros2 topic echo.&#x20;

```
ros2 topic echo /tf
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FMtfF6pIU8gezOXSZeBKa%2Fimage.png?alt=media&amp;token=cca13828-5ef0-41f8-a399-38a096d6429e" alt=""><figcaption></figcaption></figure>

Use the ros2 topic hz command to see the update rate. Here, the message is sent 60 times per second!

```
ros2 topic hz /tf
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fx0MpAOaM8tbpBmtP8bqC%2Fimage.png?alt=media&amp;token=48a2b37c-4a71-4935-816a-2129fdfe68d3" alt=""><figcaption></figcaption></figure>

### Look at the /joint\_states topic

Echo the `/joint_states` topic and let the robot turn. You should see the joint state position and velocity change.&#x20;

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIf9Qd2kLikFoRpBieMgl%2Fimage.png?alt=media&amp;token=1c73090f-2dd6-49bf-af5b-439e6599b5cc" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fc7iuLHaMdenJRVFX2ogG%2Fimage.png?alt=media&amp;token=d87f8603-ba1e-4e0e-8fdd-d0c49bc318f2" alt=""><figcaption></figcaption></figure></div>

&#x20;          &#x20;

---

### 8. Here come the sensors  `[gewijzigd]`

<sub>turtlebot-in-simulation/here-come-the-sensors.md</sub>


{% hint style="info" %}
Theory: [Laser scan](theory/laser-scan.md), [Odometry](theory/odometry.md) and [IMU](theory/imu.md).
{% endhint %}

## 2D lidar

In this step, we want to visualise the 2D lidar present on the Turtlebot3.

Click Add and select the tab *By topic,* and select the topic */scan.*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FhlHmmQfmDfvpgPzvcWqY%2Fimage.png?alt=media&amp;token=784d5607-f955-4c5f-b470-93b0921d01fd" alt=""><figcaption></figcaption></figure>

Normally, the lidar output should be shown with red dots.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FDJBJ4zWBcTaBf32aMo7I%2Fimage.png?alt=media&amp;token=337d4a23-7afa-4593-a356-0eb23283e015" alt=""><figcaption></figcaption></figure>

By using the `ros2 topic echo` command, you can also see the /scan topic.

```
ros2 topic echo /scan
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FTL0iNXp2k9wGnX8iz2gj%2Fimage.png?alt=media&amp;token=87921f0c-cc7e-4008-85cb-67bc07ee92a6" alt=""><figcaption></figcaption></figure>

You can see the following:

* the angle scan range (0-6.28 rad)
* The angle increment: 0.0175 rad or 1 degree (360 points per rotation)
* Minimum range detected: 0.1199 m
* Maximum range detected: 3.5m
* In the item *ranges,* you can see all distances of every point.

Try driving around and see the lidar scan change.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FMaXjRFrwHvgKRlsR0a3T%2FRobot_scan_demo.gif?alt=media&amp;token=3d835e48-bba3-4b98-b949-1d8553e7342c" alt=""><figcaption></figcaption></figure>

## Odometry

The odometry shows us the path that the robot has been driven based on the wheel rotation.

Click Add and select the tab *By topic,* and select the topic */odom.*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9LMmGp6LFrOXsNilUrMK%2Fimage.png?alt=media&amp;token=039c800b-c760-47af-b926-2650cd3df440" alt=""><figcaption></figcaption></figure>

Collapse the item Odometry on the left. And change the parameter to keep to 500. This means the last 500 locations will be visualised in RViz2.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZkYe8O1NTIsSyi5CcPxG%2Fimage.png?alt=media&amp;token=31694e11-6e09-4af2-bc71-fcccdb0ebc53" alt=""><figcaption></figcaption></figure>

&#x20;Then try driving around. You should get a collection of arrows showing the location and orientation of the robot.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FRyxHCooFUVTT1NJ48pNv%2FRobot_odom_demo.gif?alt=media&amp;token=182cad3a-930f-4f77-ad83-6552b5f2eef2" alt=""><figcaption></figcaption></figure>

## IMU

The Turtlebot3 has a built-in IMU sensor. This can't be directly shown in RViz2.&#x20;

With `ros2 topic echo`, the real-time value can be shown. Open a new terminal if needed. You can see the linear z acceleration is roughly the known 9.81 m/s².&#x20;

```
ros2 topic echo /imu
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FgwaDgaLqETpefgG11ng0%2Fimage.png?alt=media&amp;token=996d4617-b5d6-4fb5-85cb-761768b59c2b" alt=""><figcaption></figcaption></figure>

Next: [Theory: what the robot measures](theory.md) - what these topics mean.

---

### 9. Theory: what the robot measures  `[nieuw]`

<sub>turtlebot-in-simulation/theory.md</sub>


You have now seen the topics of the robot in Gazebo, RViz2 and the terminal.
Before you write your own nodes, this chapter explains **where the data comes
from** and **what it means**: a short piece of theory for each important topic,
applied to the TurtleBot3 Burger in Gazebo. Keep the simulation running: every
page has a few commands to try.

* [Laser scan (`/scan`)](theory/laser-scan.md) - what the lidar sees
* [Odometry (`/odom`) and wheels](theory/odometry.md) - where the robot thinks it is
* [IMU (`/imu`)](theory/imu.md) - rotation and acceleration
* [TF - coordinate frames](theory/tf.md) - how everything fits together
* [Driving the robot (`/cmd_vel`)](theory/cmd-vel.md) - speed commands
* [QoS - Quality of Service](theory/qos.md) - why you sometimes receive nothing

## Where does the data come from?

In the simulation there is no real hardware: **Gazebo** calculates the physics
(wheels, floor, walls) and simulates the sensors. A **bridge** turns the Gazebo
messages into ROS 2 topics.

```
            Docker container gazebo_turtlebot_cont (your laptop)
 ┌──────────────────────────────────────────────────────────────────────┐
 │  Gazebo (gz sim)                    ros_gz_bridge         ROS 2      │
 │  ┌──────────────────────────┐                                         │
 │  │ lidar sensor   ──────────┼──────────────────────────►  /scan       │
 │  │ IMU sensor     ──────────┼──────────────────────────►  /imu        │
 │  │ DiffDrive plugin ────────┼──────────────────────────►  /odom, /tf  │
 │  │ JointState plugin ───────┼──────────────────────────►  /joint_states
 │  │ simulation time ─────────┼──────────────────────────►  /clock      │
 │  │ DiffDrive plugin ◄───────┼───────────────────────────  /cmd_vel    │
 │  └──────────────────────────┘                                         │
 │                                                                       │
 │  robot_state_publisher (URDF + /joint_states) ───────►  /tf, /tf_static,
 │                                                          /robot_description
 │  RViz2, teleop_twist_keyboard, your nodes                             │
 └──────────────────────────────────────────────────────────────────────┘
```

* The **DiffDrive plugin** moves the wheels when you send `/cmd_vel` and
  **calculates the odometry**.
* The sensors in Gazebo get a bit of **noise** on purpose, so the data looks
  like real sensor data.
* Gazebo has its own clock (`/clock`). That is why nodes in the simulation use
  `use_sim_time:=True`: they follow the simulation time, not the clock of your laptop.

On the real robot the same topics come from real hardware (see
[Simulation vs. real robot](../simulation-vs-real-robot.md)). That is the strength
of ROS: your code does not see the difference.

## Conventions used by all ROS robots

ROS uses fixed conventions (REP-103), so every robot and every tool agrees:

| Quantity | Unit | |
|---|---|---|
| distance | metre (m) | not cm or mm! |
| angle | radian (rad) | 1 rad ≈ 57.3°, 90° = π/2 ≈ 1.571 rad |
| linear speed | m/s | |
| angular speed | rad/s | |
| time | seconds (ROS time stamp in the `header`) | |

Axes of the robot (right-hand rule):

```
            x (forward)
            ▲
            │
   y ◄──────●        z points up, out of the screen
  (left)   robot
```

* **x** = forward, **y** = left, **z** = up.
* A **positive rotation** around z is **counterclockwise** (to the left).
  So `angular.z = +0.5` in `/cmd_vel` turns the robot to the left.

{% hint style="info" %}
Try it: start the simulation, then `ros2 topic list` and `ros2 topic info /odom`.
Which node publishes `/odom`? (Hint: it is the bridge.)
{% endhint %}

---

#### 10. Laser scan (/scan)  `[nieuw]`

<sub>turtlebot-in-simulation/theory/laser-scan.md</sub>


## How a lidar works

On top of the TurtleBot is a lidar (Laser Distance Sensor). Inside, a laser and
a receiver turn around (about 5 rotations per second). For every small angle
step the sensor measures the distance to the first object the laser hits. The
result of one rotation is a **2D slice** of the world at the height of the lidar
(about 18 cm above the floor).

```
                    0 rad (front, x)
                         ▲
                 ·  ·  · │ ·  ·  ·
             ·           │           ·
   +π/2   ·              │              ·    3π/2 (or -π/2)
  (left) ·───────────────●───────────────·  (right)
          ·            robot            ·
             ·                       ·
                 ·  ·  ·   ·  ·  ·
                        π (back)
```

{% hint style="warning" %}
The lidar only sees what is **at its own height**. A low object or a table top
above the robot is invisible to it. On the real robot glass and black, shiny
surfaces can also give no (or a wrong) reflection - Gazebo does not simulate that.
{% endhint %}

## The lidar in Gazebo

| | simulation (Gazebo) | real robot (LDS-02) |
|---|---|---|
| scans per second | 5 Hz | ~5 Hz |
| points per rotation | **360**, always the same | ~220-230, varies |
| angular resolution | 1° (0.0175 rad) | ~1.6° |
| angles | 0 → 6.28 rad | |
| range | 0.12 m to **3.5 m** | ~0.16 m to 8 m |
| noise | ±1 cm (gaussian, added by Gazebo) | real noise |
| frame | `base_scan` (see [TF](tf.md)) | `base_scan` |

## The LaserScan message

`/scan` is of type `sensor_msgs/msg/LaserScan`:

| field | meaning |
|---|---|
| `header.stamp` | time of the measurement (simulation time) |
| `header.frame_id` | `base_scan`: the distances are measured from the centre of the lidar |
| `angle_min`, `angle_max` | angle of the first and the last point (rad) |
| `angle_increment` | angle between two points (rad) |
| `range_min`, `range_max` | limits of the sensor (m) |
| `ranges[]` | the distances (m), one per angle step |
| `intensities[]` | strength of the reflection |

The **index** `i` in `ranges[]` belongs to the angle:

```
angle(i) = angle_min + i * angle_increment
```

and the other way around, the index for a given angle:

```
i = round((angle - angle_min) / angle_increment)
```

Index `0` is the **front** of the robot, the angle grows **counterclockwise**:
in the simulation index 90 is the **left** side, 180 the **back**, 270 the **right**.

{% hint style="info" %}
On the real robot the number of points is not always the same (220, 221, ...).
Code with fixed indices like `ranges[90]` works in the simulation but not on
the real robot. Calculate the index from `angle_increment`, or use
`len(msg.ranges) // 4` - then your code works on both.
{% endhint %}

## Invalid values

Not every angle gives a good measurement. In `ranges[]` you can find:

* `inf` - nothing within range (in the simulation: nothing within 3.5 m)
* `nan` - no measurement for that angle (happens on the real robot)
* values below `range_min` - no valid echo

Always filter these before you calculate a mean or a minimum, for example:

```python
valid = [r for r in msg.ranges if math.isfinite(r) and r >= msg.range_min]
```

## From distance and angle to a point (x, y)

A lidar point is given in **polar coordinates** (distance `r`, angle `θ`). To
get the point in the frame of the lidar (`base_scan`):

```
x = r * cos(θ)        (forward)
y = r * sin(θ)        (left)
```

This is exactly what RViz2 does to draw the red dots. To place the points in the
world, RViz2 also needs the position of the lidar on the robot and the position
of the robot in the world: that is [TF](tf.md).

## Try it

```bash
ros2 topic hz /scan                     # how many scans per second?
ros2 topic echo /scan --once --field angle_increment
ros2 topic echo /scan --once --field ranges
```

Put the robot in front of a wall in Gazebo and look at `ranges[0]`. Then
drive 0.5 m back: does the value change by 0.5?

<details>

<summary>Check yourself</summary>

1. `angle_increment` is 0.0175 rad. How many degrees is that, and how many points per rotation?
   * 0.0175 × 57.3 ≈ 1°; 2π / 0.0175 ≈ 360 points.
2. Which index points to the right?
   * 270 (angle 3π/2, or -π/2).
3. The robot is in an empty part of the world. Most values in `ranges` are `inf`. Is the lidar broken?
   * No: there is nothing within 3.5 m.

</details>

Exercise: [Here come the sensors](../here-come-the-sensors.md).

Next: [Odometry (/odom) and wheels](odometry.md).

---

#### 11. Odometry (/odom) and wheels  `[nieuw]`

<sub>turtlebot-in-simulation/theory/odometry.md</sub>


## What is odometry?

**Odometry** is estimating the position of the robot by **counting how far the
wheels have turned**. It is like walking with your eyes closed and counting your
steps: it works well for a short time, but small errors add up.

The robot starts at `(x, y, θ) = (0, 0, 0)` when the simulation starts. From
then on every small movement is added to that position.

## The wheels of the TurtleBot3 Burger

| | Burger |
|---|---|
| wheel radius `r` | 0.033 m |
| distance between the wheels `L` | 0.160 m |
| wheel circumference `2πr` | 0.207 m |

The topic `/joint_states` (`sensor_msgs/msg/JointState`) shows the wheels:

* `name[]`: `wheel_left_joint`, `wheel_right_joint`
* `position[]`: how far each wheel has turned, in **radians** (keeps counting)
* `velocity[]`: rotation speed of each wheel in rad/s

From wheel rotation to distance:

```
distance     = position * r          [m]
speed_wheel  = velocity * r          [m/s]
```

{% hint style="info" %}
The real robot has **encoders** on the motors: 4096 ticks per wheel rotation,
in the topic `/sensor_state`. The simulation only has `/joint_states`, which the
real robot also has.
{% endhint %}

## From two wheels to the position of the robot

The TurtleBot3 is a **differential drive** robot: two driven wheels and a
caster at the back. It cannot drive sideways. Every small time step:

```
d_left, d_right = distance of each wheel since the last step

d     = (d_right + d_left) / 2          distance of the robot centre
dθ    = (d_right - d_left) / L          rotation of the robot

x    += d * cos(θ + dθ/2)
y    += d * sin(θ + dθ/2)
θ    += dθ
```

* Both wheels the same distance → driving straight (`dθ = 0`).
* Wheels in opposite directions → turning on the spot (`d = 0`).

The same formulas the other way around turn a command on `/cmd_vel`
(`linear.x = v`, `angular.z = ω`) into wheel speeds:

```
v_left  = v - ω * L / 2
v_right = v + ω * L / 2
```

In Gazebo the **DiffDrive plugin** does both: it turns `/cmd_vel` into wheel
speeds, and it calculates `/odom` from the wheels (30 times per second).

## The Odometry message

`/odom` is of type `nav_msgs/msg/Odometry`:

| field | meaning |
|---|---|
| `header.frame_id` | `odom` - the position is relative to the start point |
| `child_frame_id` | `base_footprint` - the robot |
| `pose.pose.position` | `x`, `y` (m), `z` is always 0 |
| `pose.pose.orientation` | rotation as a **quaternion** (`x, y, z, w`) - see [IMU](imu.md) |
| `twist.twist.linear.x` | forward speed (m/s) |
| `twist.twist.angular.z` | rotation speed (rad/s) |
| `pose.covariance`, `twist.covariance` | how uncertain the estimate is |

The same position is also published as the transform `odom -> base_footprint` on
`/tf` (see [TF](tf.md)).

## Why does odometry drift?

On a real robot:

* the wheels **slip** (smooth floor, accelerating, turning)
* the wheel radius is not exactly 0.033 m (wear, dust)
* bumps, thresholds, cables
* small errors in θ become large errors in x, y after a few metres

In **Gazebo** the floor is perfect and the wheel radius is exact, so the odometry
is almost perfect. Don't be fooled: on the real robot it drifts much more. That
is why SLAM or AMCL compares the [laser scan](laser-scan.md) with a map and
publishes a correction (`map -> odom`, see [TF](tf.md)).

## Try it

```bash
ros2 topic echo /odom --field pose.pose.position
ros2 topic echo /joint_states
```

Drive straight ahead with `teleop_twist_keyboard` and compare the change of `x`
in `/odom` with the change of `position` × 0.033 in `/joint_states`.

<details>

<summary>Check yourself</summary>

1. The left wheel `position` went from 10.0 to 28.85 rad. How far did the left wheel drive?
   * 18.85 rad × 0.033 m ≈ 0.62 m (= 3 wheel rotations).
2. `/cmd_vel` has `linear.x = 0`, `angular.z = 1.0` rad/s. What are the wheel speeds?
   * v_left = -0.08 m/s, v_right = +0.08 m/s: turning left on the spot.
3. In the simulation `/odom` stays correct for minutes. Will that also be the case on the real robot?
   * No: slip and small errors make the real odometry drift.

</details>

Exercise: [The first ros2 node](../../the-first-ros2-node.md) (subscribe to `/odom`).

Next: [IMU (/imu)](imu.md).

---

#### 12. IMU (/imu)  `[nieuw]`

<sub>turtlebot-in-simulation/theory/imu.md</sub>


## What is an IMU?

An **IMU** (Inertial Measurement Unit) is a small chip that measures how the
robot **moves and rotates**. On the real TurtleBot3 it is on the OpenCR board;
in Gazebo it is a simulated sensor in the frame `imu_link`. It contains:

* a **gyroscope**: rotation speed around x, y and z (rad/s)
* an **accelerometer**: acceleration along x, y and z (m/s²)

(You know these sensors from your phone and from the flight controller of a drone.)

From both, the **orientation** of the robot is calculated: how it is turned in space.

```
          z (yaw)
          ▲
          │
          │
          ●─────► x (roll)      roll  = rotation around x (tilt left/right)
         ╱                      pitch = rotation around y (nose up/down)
        ╱                       yaw   = rotation around z (heading)
       ▼
      y (pitch)
```

For a ground robot, **yaw** (the heading) is by far the most important one.
Roll and pitch stay almost 0 on a flat floor.

## The IMU in Gazebo

| | simulation | real robot |
|---|---|---|
| rate | 200 Hz | lower (check with `ros2 topic hz /imu`) |
| noise | gaussian, added by Gazebo | real noise and drift |
| frame | `imu_link` | `imu_link` |

## The Imu message

`/imu` is of type `sensor_msgs/msg/Imu`:

| field | meaning | robot standing still on the floor |
|---|---|---|
| `orientation` | rotation as a quaternion (`x, y, z, w`) | depends on the heading |
| `angular_velocity` | rad/s around x, y, z | ≈ 0, 0, 0 (+ noise) |
| `linear_acceleration` | m/s² along x, y, z | ≈ 0, 0, **9.81** |

{% hint style="info" %}
Standing still, the accelerometer measures **9.81 m/s² upwards**: it measures
gravity. That is how the IMU knows which way is down (roll and pitch). For yaw
there is no such reference, so on a real robot yaw slowly **drifts**.
{% endhint %}

## Quaternions

ROS does not store orientation as three angles, but as a **quaternion**: four
numbers `(x, y, z, w)`. Quaternions have no problems with angles that jump from
+180° to -180° and are easy to combine. You don't have to understand the
maths, just remember:

* no rotation: `(0, 0, 0, 1)`
* for a ground robot only `z` and `w` change
* convert to **yaw** (in rad) like this (you will see this code again in
  [The first ros2 node](../../the-first-ros2-node.md)):

```python
import math

q = msg.orientation          # also works for msg.pose.pose.orientation of /odom
yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
print(math.degrees(yaw))
```

## IMU and wheels

| | wheels (odometry) | IMU (gyroscope) |
|---|---|---|
| distance | ✅ good | ❌ (double integration of acceleration → very large drift) |
| rotation | ⚠️ errors from slip | ✅ good, slow drift over time |

That is why the real TurtleBot3 combines both: distance from the wheels, heading
from the IMU. Combining sensors to get a better result than each sensor alone
is called **sensor fusion**. (In the simulation `/odom` only uses the wheels -
the perfect Gazebo floor makes that good enough.)

## Try it

```bash
ros2 topic hz /imu
ros2 topic echo /imu --field angular_velocity
ros2 topic echo /imu --field linear_acceleration
```

* Turn the robot left with `teleop_twist_keyboard`: which value of `angular_velocity` changes? Positive or negative?
* Compare `angular_velocity.z` of `/imu` with `twist.twist.angular.z` of `/odom`.

<details>

<summary>Check yourself</summary>

1. The robot turns left at 0.5 rad/s. What does `angular_velocity.z` show?
   * About +0.5 (counterclockwise is positive).
2. The quaternion is `(0, 0, 0.707, 0.707)`. What is the yaw?
   * atan2(2·0.707·0.707, 1 − 2·0.707²) = atan2(1, 0) = π/2 → 90°, turned to the left.
3. Why can't we calculate the position of the robot from the accelerometer?
   * Acceleration has to be integrated twice; every small error grows very fast (quadratically in time).

</details>

Exercise: [Here come the sensors](../here-come-the-sensors.md) (IMU part).

Next: [TF - coordinate frames](tf.md).

---

#### 13. TF - coordinate frames  `[nieuw]`

<sub>turtlebot-in-simulation/theory/tf.md</sub>


## The problem

Every sensor measures in **its own coordinate frame**:

* the lidar says "there is a wall 1.0 m in front of **me**" (frame `base_scan`)
* the IMU measures in **its** frame (`imu_link`)
* odometry says where the **robot** is relative to the **start point** (`odom`)

To draw the wall in the world, or to drive to it, we have to know how these
frames are positioned relative to each other. That is the job of **TF** (the
`tf2` library).

## Frames and transforms

A **frame** is a coordinate system with a name. A **transform** between two
frames is a translation (x, y, z) + a rotation (quaternion). All transforms
together form a **tree**: every frame has exactly one parent.

The TF tree of the TurtleBot3 Burger in the simulation:

```
map                     ← only with SLAM or Nav2 (later in this book)
 └── odom               ← start point of the odometry
      └── base_footprint     ← the robot, on the floor (dynamic: Gazebo DiffDrive)
           └── base_link          ← centre of the robot, 1 cm higher (static)
                ├── base_scan          ← the lidar        (static)
                ├── imu_link           ← the IMU          (static)
                ├── caster_back_link   ← caster           (static)
                ├── wheel_left_link    ← left wheel  (turns: robot_state_publisher)
                └── wheel_right_link   ← right wheel (turns: robot_state_publisher)
```

| transform | published by | kind |
|---|---|---|
| `map -> odom` | slam_toolbox (SLAM) or AMCL (Nav2) | dynamic, correction of the drift |
| `odom -> base_footprint` | Gazebo DiffDrive plugin (via the bridge) | dynamic, changes when driving |
| `base_footprint -> base_link -> base_scan, imu_link, ...` | `robot_state_publisher` (from the URDF) | **static**, fixed on the robot |
| `base_link -> wheel_*_link` | `robot_state_publisher` (from `/joint_states`) | dynamic, the wheels turn |

* **Dynamic** transforms are published on `/tf` many times per second.
* **Static** transforms are published once on `/tf_static` (they never change).

On the real robot the tree is exactly the same; only `odom -> base_footprint`
comes from the robot driver instead of Gazebo.

## Positions on the Burger (from the URDF)

| from `base_link` to | x | y | z |
|---|---|---|---|
| `base_scan` (lidar) | -0.032 m | 0 | 0.172 m |
| `imu_link` | -0.032 m | 0 | 0.068 m |
| `wheel_left_link` | 0 | +0.080 m | 0.023 m |
| `wheel_right_link` | 0 | -0.080 m | 0.023 m |

`base_link` is 0.010 m above `base_footprint` (the floor).

So the lidar is **3.2 cm behind** the centre between the wheels. A wall at
1.000 m in the scan is at 1.000 - 0.032 = 0.968 m in front of `base_link`. TF
does this calculation for you.

## Why both `map` and `odom`?

* `odom` is **smooth** (no jumps) but **drifts** - good for the controller that drives.
* `map` is **correct** (SLAM/AMCL compares the scan with the map) but **can jump** - good for "where am I".
* SLAM/AMCL publishes `map -> odom` so that `map -> odom -> base_footprint`
  gives the corrected position, without changing the odometry itself.

## Fixed frame in RViz2

In RViz2 the **Fixed Frame** is the frame in which everything is drawn:

* `base_link` - the robot stands still, the world moves around it
* `odom` - the world stands still, the robot drives
* `map` - the robot drives on the map (only with SLAM / Nav2)

If RViz2 says *"No transform from [base_scan] to [map]"*, a link in the tree is
missing: for example SLAM is not running, so there is no `map -> odom`. That is
the Global Status error you see in [Show me the robot](../show-me-the-robot.md).

## Try it

```bash
# Show the TF tree as a PDF (frames_<date>.pdf in the current folder)
ros2 run tf2_tools view_frames

# Position of the robot relative to odom, live
ros2 run tf2_ros tf2_echo odom base_footprint

# Fixed offset of the lidar
ros2 run tf2_ros tf2_echo base_link base_scan
```

In RViz2: add the **TF** display and enable *Show Names*.

In Python you can ask TF for a transform with a `tf2_ros.Buffer` and a
`tf2_ros.TransformListener`:

```python
from tf2_ros import Buffer, TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
...
t = self.tf_buffer.lookup_transform('odom', 'base_footprint', rclpy.time.Time())
self.get_logger().info(f"x={t.transform.translation.x:.2f} y={t.transform.translation.y:.2f}")
```

<details>

<summary>Check yourself</summary>

1. Who publishes `odom -> base_footprint` in the simulation? And on the real robot?
   * Simulation: the Gazebo DiffDrive plugin (via `ros_gz_bridge`). Real robot: the robot driver `turtlebot3_node`.
2. You start RViz2 with Fixed Frame `map` but without SLAM. What do you see?
   * An error: there is no transform `map -> odom`, nothing is drawn.
3. You mount a camera 5 cm in front of the lidar. What do you need to add to the TF tree?
   * A static transform, e.g. `base_link -> camera_link` with x = -0.032 + 0.05 = 0.018 m (and the height):
     `ros2 run tf2_ros static_transform_publisher --x 0.018 --z 0.17 --frame-id base_link --child-frame-id camera_link`

</details>

Exercise: [Show me the robot](../show-me-the-robot.md).

Next: [Driving the robot (/cmd_vel)](cmd-vel.md).

---

#### 14. Driving the robot (/cmd_vel)  `[nieuw]`

<sub>turtlebot-in-simulation/theory/cmd-vel.md</sub>


## A speed, not a position

You don't tell the robot **where** to go, you tell it **how fast** to move
*right now*. That is the job of the topic `/cmd_vel` ("command velocity").

So "drive 10 cm" always becomes: drive at speed `v` during a time `t`, then
send speed 0 (or: drive until [odometry](odometry.md) says you did 10 cm).

## The TwistStamped message

In the simulation (ROS 2 Jazzy) `/cmd_vel` is a `geometry_msgs/msg/TwistStamped`:
a `header` (time stamp + frame) and a `twist` with the speeds.

```
header:
  stamp: ...
  frame_id: base_link
twist:
  linear:            angular:
    x: 0.1   ← forward (m/s)    x: 0.0
    y: 0.0                      y: 0.0
    z: 0.0                      z: 0.5   ← turn (rad/s), positive = left
```

That is why `teleop_twist_keyboard` is started with `-p stamped:=true`.

A **differential drive** robot can only use two of the six numbers:

| field | meaning | real Burger max |
|---|---|---|
| `twist.linear.x` | forward (+) / backward (-) | 0.22 m/s |
| `twist.angular.z` | turn left (+) / right (-) | 2.84 rad/s |
| other fields | ignored: the robot cannot drive sideways, fly or roll | - |

{% hint style="warning" %}
Gazebo does **not** limit the speed: you can drive the simulated robot at 1 m/s.
The real Burger can do at most 0.22 m/s. Keep your code within the real limits.
{% endhint %}

Combining both gives a **curve** with radius `R = v / ω`. For example
`linear.x = 0.1`, `angular.z = 0.5` → a circle with a radius of 0.2 m.

How this becomes two wheel speeds is explained in [Odometry](odometry.md):
`v_left = v - ω·L/2`, `v_right = v + ω·L/2`.

## The path of a command

```
 teleop_twist_keyboard ─┐
 Nav2                  ─┼─► /cmd_vel ─► ros_gz_bridge ─► Gazebo DiffDrive plugin ─► wheels
 your node             ─┘   (TwistStamped)
```

In the simulation **everyone publishes on the same topic**: if two nodes send
`/cmd_vel` at the same time, the robot jerks between both commands. On the real
robot a *twist_mux* decides who is in control (see
[Simulation vs. real robot](../../simulation-vs-real-robot.md)).

{% hint style="info" %}
On the real robot (ROS 2 Humble) `/cmd_vel` is a plain `Twist`, without header.
Code from the simulation needs a small change.
{% endhint %}

## Good habits

* **Publish regularly** (e.g. 10-20 times per second), not just once.
* **Always stop explicitly**: publish a message with all speeds 0 when you are
  done, and also when your node stops (Ctrl+C).
* **Start slow** and stay within the real limits (0.22 m/s, 2.84 rad/s): then your
  code also works on the real robot.

## Try it

```bash
# Turn slowly to the left, 10 times per second (Ctrl+C to stop)
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/TwistStamped "{twist: {angular: {z: 0.3}}}"

# Stop
ros2 topic pub --once /cmd_vel geometry_msgs/msg/TwistStamped "{}"

# Which type does the robot expect?
ros2 topic info /cmd_vel
```

<details>

<summary>Check yourself</summary>

1. You publish `twist.linear.y = 0.1`. What does the robot do?
   * Nothing: a differential drive robot cannot drive sideways.
2. Which command drives a circle with a radius of 0.5 m at 0.1 m/s, to the right?
   * `linear.x = 0.1`, `angular.z = -0.2` (ω = v / R = 0.1 / 0.5).
3. Your node publishes a `Twist` (without header) on `/cmd_vel` in the simulation. What happens?
   * Nothing, or an error about the type: the simulation expects `TwistStamped`.

</details>

Exercise: [Moving the turtlebot](../moving-the-turtlebot.md).

Next: [QoS - Quality of Service](qos.md).

---

#### 15. QoS - Quality of Service  `[nieuw]`

<sub>turtlebot-in-simulation/theory/qos.md</sub>


## Why QoS?

Not every topic needs the same kind of delivery:

* A **laser scan** arrives 5 times per second. If one is lost on the network, it
  is no use sending it again: the next one is newer anyway.
* A **map** is published once. A node that starts later must still get it.
* A **command** that has to arrive should be sent again when it gets lost.

With **QoS** (Quality of Service) every publisher and subscriber says how it
wants to send or receive messages.

## The three settings you need

| setting | options | meaning |
|---|---|---|
| **Reliability** | `RELIABLE` | a lost message is sent again (like TCP) |
| | `BEST_EFFORT` | a lost message is lost, no waiting (like UDP) - good for sensors |
| **Durability** | `VOLATILE` | you only get messages sent **after** you subscribed |
| | `TRANSIENT_LOCAL` | the publisher keeps the last message(s); a **late** subscriber still gets them ("latched") |
| **History + depth** | `KEEP_LAST` + `depth` | how many messages are kept in the queue (e.g. 10) |

There are more settings (deadline, lifespan, liveliness), but you won't need
them in this lab.

When you write `self.create_subscription(Odometry, '/odom', self.cb, 10)`, the
`10` is the depth, and you get the **default** QoS: `RELIABLE`, `VOLATILE`, `KEEP_LAST 10`.

## Publisher and subscriber must match

The simulation uses the DDS middleware (CycloneDDS). A subscriber only receives
messages if it asks for **the same or less** than the publisher offers:

| publisher offers | subscriber asks | works? |
|---|---|---|
| RELIABLE | RELIABLE | ✅ |
| RELIABLE | BEST_EFFORT | ✅ |
| BEST_EFFORT | BEST_EFFORT | ✅ |
| BEST_EFFORT | **RELIABLE** | ❌ no messages |
| TRANSIENT_LOCAL | VOLATILE or TRANSIENT_LOCAL | ✅ |
| VOLATILE | **TRANSIENT_LOCAL** | ❌ no messages |

The nasty part: there is **no error**, you simply get nothing (at most a warning
*"incompatible QoS"*).

{% hint style="success" %}
**Rule of thumb:** subscribe to sensor data (`/scan`, `/imu`, ...) with
**Best Effort**. A Best Effort subscriber works with a Reliable *and* a Best
Effort publisher, so your code works in the simulation **and** on the real robot.
{% endhint %}

## QoS of the topics in the simulation

| topic | reliability | durability | published by |
|---|---|---|---|
| `/scan`, `/imu`, `/odom`, `/joint_states`, `/tf`, `/clock` | RELIABLE | VOLATILE | `ros_gz_bridge` (default QoS) |
| `/tf_static`, `/robot_description` | RELIABLE | **TRANSIENT_LOCAL** | `robot_state_publisher`: sent once, nodes that start later still get it |
| `/map` (SLAM / Nav2, later in this book) | RELIABLE | **TRANSIENT_LOCAL** | sent once, RViz2 started later must still see it |

{% hint style="info" %}
On the real robot the lidar driver publishes `/scan` as **BEST_EFFORT**. In the
simulation the bridge publishes it as RELIABLE. That is why the real-robot
tutorial tells you to set Best Effort in RViz2 - following the rule of thumb
above, you do that in the simulation as well.
{% endhint %}

Check it yourself: `ros2 topic info -v /scan` shows the QoS of every publisher
and subscriber.

## QoS in Python

For sensor data there is a ready-made profile:

```python
from rclpy.qos import qos_profile_sensor_data

self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data)
```

Or set it yourself:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(depth=10,
                 reliability=ReliabilityPolicy.BEST_EFFORT)

map_qos = QoSProfile(depth=1,
                     reliability=ReliabilityPolicy.RELIABLE,
                     durability=DurabilityPolicy.TRANSIENT_LOCAL)
```

In RViz2 you find the same settings per display under **Topic**: *Reliability
Policy*, *Durability Policy*, *Depth*.

## Try it

```bash
ros2 topic info -v /scan
ros2 topic info -v /tf_static
ros2 topic echo --qos-durability transient_local /scan --once    # what happens?
```

<details>

<summary>Check yourself</summary>

1. Why would you use Best Effort for a laser scan?
   * Resending an old scan is useless (the next one arrives 0.2 s later) and causes extra traffic and delay.
2. The last command above (`transient_local` on `/scan`) waits forever. Why?
   * The bridge offers VOLATILE, the subscriber asks TRANSIENT_LOCAL → incompatible, no messages.
3. You start RViz2 after `robot_state_publisher`. Why do you still see the robot model?
   * `/robot_description` and `/tf_static` are TRANSIENT_LOCAL: a late subscriber still gets them.

</details>

Next: [The first ros2 node](../../the-first-ros2-node.md) - write your own nodes.

---

## 16. The first ros2 node  `[gewijzigd]`

<sub>the-first-ros2-node.md</sub>


{% hint style="info" %}
Theory: [Odometry](turtlebot-in-simulation/theory/odometry.md) (quaternion to yaw: [IMU](turtlebot-in-simulation/theory/imu.md)), [Driving the robot (/cmd_vel)](turtlebot-in-simulation/theory/cmd-vel.md) and [QoS](turtlebot-in-simulation/theory/qos.md).
{% endhint %}

## Connect to the container via VScode

Make sure Gazebo (`turtlebot3_world.launch.py`) and `teleop_twist_keyboard` are running.

Open VScode and use the Remote Explorer in VScode.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F4gVfVBGdrmG81hQkuGaE%2Fimage.png?alt=media&amp;token=489d161f-750e-4197-a858-84cdc20b5720" alt=""><figcaption></figcaption></figure>

Select *WSL Targets* and select *Ubuntu-22.04*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fuql0D1fIp2NdALC78tim%2Fimage.png?alt=media&amp;token=61074534-e4a7-4997-91a2-115772b1304e" alt=""><figcaption></figcaption></figure>

After connecting, you should see below that you are connected to the WSL target.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FmZIjktpamZ37ACKqxlor%2Fimage.png?alt=media&amp;token=1a59cc5c-6be0-486a-a229-efa23eb14bb2" alt=""><figcaption></figcaption></figure>

After the connection, select Dev Containers again in the remote explorer dropdown menu.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJ0t6nXGbRSHsmkPxDwln%2Fimage.png?alt=media&amp;token=25c48d15-72f7-4eae-bf56-457ff220b78d" alt=""><figcaption></figcaption></figure>

Select the ros2-jazzy-gazebo-turtlebot. Click on the arrow to connect.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F5IyrVViWo3rFjiKEcBAO%2Fimage.png?alt=media&amp;token=2d99fee1-609f-4cb6-afb1-8a3b14c35ae7" alt=""><figcaption></figcaption></figure>

You should now be inside the Docker container. When asked to open a folder,
choose `/home/dockeruser/dev_ws`.

{% hint style="warning" %}
Store your scripts in `/home/dockeruser/dev_ws`: that folder is the `dev_ws`
folder of the cloned `ros2-jazzy-gazebo-turtlebot` repository on WSL, so your
files survive when the container is recreated. Files elsewhere in the
container can be lost.
{% endhint %}

## Make your first ROS 2 node

### Subscribe to /odom

The objective is to read out the location of the turtlebot with our own written Python script.

Make a new directory `turtlebot` in `/home/dockeruser/dev_ws` and make a `turtlebot_subscribe.py` script in it.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9VzjsmJr7wkCoOzcnJVM%2Fimage.png?alt=media&amp;token=5159afc2-8983-4a66-8615-616ca03a4ea0" alt=""><figcaption></figcaption></figure>

Paste the code below in the `turtlebot_subscribe.py`

<details>

<summary>Python script</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from math import atan2, asin

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_listener')
        # Subscribe to the /odom topic
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.get_logger().info("Subscribed to /odom topic.")

    def odom_callback(self, msg):
        # Extract position
        pos = msg.pose.pose.position
        # Extract orientation (quaternion)
        ori = msg.pose.pose.orientation

        # Convert quaternion to yaw (2D orientation)
        siny_cosp = 2 * (ori.w * ori.z + ori.x * ori.y)
        cosy_cosp = 1 - 2 * (ori.y * ori.y + ori.z * ori.z)
        yaw = atan2(siny_cosp, cosy_cosp)

        # Log position and yaw
        self.get_logger().info(
            f"Position -> x: {pos.x:.3f}, y: {pos.y:.3f}, "
            f"Yaw: {yaw:.3f} rad"
        )

def main(args=None):
    rclpy.init(args=args)
    node = OdomSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

```

</details>

Analyse the Python code. And try to understand what is happening.

Run the code with the following command in VScode terminal.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FizQRvsCKr4Yakbz52Psb%2Fimage.png?alt=media&amp;token=7258d38e-4be6-4ee6-b058-f1a22de88a15" alt=""><figcaption></figcaption></figure>

Make sure you are in the directory of the python script.

```
python turtlebot_subscribe.py
```

Then drive the turtlebot around. You see, the position and orientation should change.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fxd1mgaz95dHeLv8FhaWX%2Fimage.png?alt=media&amp;token=022a1449-c9cf-417c-94a4-ec7a6412eefd" alt=""><figcaption></figcaption></figure>

### Publish the cmd\_vel

The objective is to control the turtlebot with our own written Python script. To make it easy, the turtlebot will just be turning around.

Make a `turtlebot_publish.py` script.

{% hint style="info" %}
Stop `teleop_twist_keyboard` first (`CTRL+C`): two nodes publishing on
`/cmd_vel` at the same time fight for the robot.
{% endhint %}

Paste the code below in the `turtlebot_publish.py`

Analyse the Python code. And try to understand what is happening.

<details>

<summary>Python script</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CmdVelStampedPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_stamped_publisher')
        
        # Publisher for TwistStamped messages
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        
        # Timer to publish at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_velocity)
        
        # Example motion parameters
        self.linear_speed = 0.0   # m/s forward
        self.angular_speed = 0.2  # rad/s rotation
        
        self.get_logger().info("Publishing TwistStamped messages on /cmd_vel")

    def publish_velocity(self):
        msg = TwistStamped()
        
        # Stamp message with current ROS time
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        # Set linear and angular velocity
        msg.twist.linear.x = self.linear_speed
        msg.twist.angular.z = self.angular_speed
        
        self.publisher.publish(msg)
        self.get_logger().info(
            f"Published TwistStamped: linear.x={msg.twist.linear.x:.2f}, angular.z={msg.twist.angular.z:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelStampedPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

```

</details>

Run the code with the following command in VScode terminal.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FHJhni9phH0g7pYedLbm8%2Fimage.png?alt=media&amp;token=93f92315-13f8-4ff3-b701-7b817c5690c7" alt=""><figcaption></figcaption></figure>

The Turtlebot3 should be turning slowly.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FNrd3Jm5t1AYtYX3qXPd2%2Fimage.png?alt=media&amp;token=cbf1e1de-e207-43b7-a0bd-2c46b7c2d07a" alt=""><figcaption></figcaption></figure>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3TfIOrCA9Q9lyppz4Py5%2F20251019-1330-11.4924500.gif?alt=media&amp;token=fdf77290-1e74-48a9-85e5-44478f62de47" alt=""><figcaption></figcaption></figure>

Change the Python code so that the Turtlebot:&#x20;

* can turn faster&#x20;
* or even drive straight.

---

## 17. SLAM / Mapping  `[gewijzigd]`

<sub>slam-mapping.md</sub>


- [Startup](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/startup.md)
- [Start mapping](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/start-mapping.md)
- [Save map](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/save-map.md)

---

### 18. Startup  `[gewijzigd]`

<sub>slam-mapping/startup.md</sub>


Go the terminal where docker compose up is used. And stop it with CRTL + C

Restart the container with docker compose up.&#x20;

Open a new terminal and connect with&#x20;

```sh
docker exec -it gazebo_turtlebot_cont bash
```

Select the `burger` turtlebot3 as loaded model in Gazebo with the following command

```sh
export TURTLEBOT3_MODEL=burger
```

Use extra terminals to start the following ros2 nodes

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

Make sure the `turtlebot3_gazebo` node and t`eleop_twist_keyboard` are running.

---

### 19. Start mapping  `[gewijzigd]`

<sub>slam-mapping/start-mapping.md</sub>


Open a new terminal and connect to the docker container.

Add the following command

```sh
export TURTLEBOT3_MODEL=burger
```

Start the mapping script

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py slam:=True
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ1g74ImNk5Yt3xcrBrxs%2Fimage.png?alt=media&amp;token=4dfb77c9-0802-4d96-b259-77edadf94dad" alt=""><figcaption></figcaption></figure>

Rviz2 should be started.

You can see that a partially obstacle map is generated.&#x20;

Try to ride, move around and map the entire world.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FGdexf1LRrE5fHolpf73i%2Fimage.png?alt=media&amp;token=699a5a01-1eec-4580-bfdc-eacc7e79a9ec" alt=""><figcaption></figcaption></figure>

---

### 20. Save map  `[gewijzigd]`

<sub>slam-mapping/save-map.md</sub>


With the following command in a new terminal the map can be saved.

{% hint style="warning" %}
It is important not to stop the mapping node of the previous step.
{% endhint %}

{% code overflow="wrap" %}
```sh
ros2 run nav2_map_server map_saver_cli -f /home/dockeruserjazzy/my_map --free 0.196 --occ 0.65
```
{% endcode %}

You get two files: `my_map.pgm` (the image) and `my_map.yaml` (resolution,
origin, thresholds). The `.yaml` is what Nav2 needs in the next step.

{% hint style="info" %}
`--free 0.196`: otherwise grey (unknown) cells are loaded as free space later on,
and Nav2 plans paths through unexplored areas. Want a PNG to put in a report?
Add `--fmt png` (the `.yaml` then points to the `.png`).
{% endhint %}

If you look in the directory with VS Code inside the container, you can find the
image of the map. This map will be used as base map for the autonomous navigation.

---

## 21. Autonomous Navigation  `[gewijzigd]`

<sub>autonomous-navigation.md</sub>


{% hint style="danger" %}
Cancel the SLAM command of the previous step with `CTRL + C` !!!!
{% endhint %}

Start Nav2 with **your** map from the previous step:

{% code overflow="wrap" %}
```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/dockeruserjazzy/my_map.yaml
```
{% endcode %}

{% hint style="warning" %}
* Without `map:=...` Nav2 loads the default map of the TurtleBot3 package, not yours.
* `use_sim_time:=True` is needed here because Gazebo publishes a simulated
  clock. On the **real** robot you leave it out (see the TurtleBot3 book).
{% endhint %}

## Set the initial position of the turtlebot3

Set the initial pose of the TurtleBot3 with the **2D Pose Estimate** button.

After the pose is set, autonomous navigation should be possible.

Use the **Nav2 Goal** button to set a desired goal. After setting it, the
TurtleBot3 should start navigating.

Try to navigate to a point and drop an obstacle in Gazebo. You see the
calculated path will change when the obstacle is detected.

---

### 22. Autonomous driving with python library  `[gewijzigd]`

<sub>autonomous-navigation/autonomous-driving-with-python-library.md</sub>


Make a nav2\_simple.py script via VScode  > WSL > docker container (See The first ros2 node)

The script makes use of the [nav2\_simple\_commander](https://docs.nav2.org/commander_api/index.html) library

```python
#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import deepcopy

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

"""
Basic stock inspection demo. In this demonstration, the expectation
is that there are cameras or RFID sensors mounted on the robots
collecting information about stock quantity and location.
"""


def main():
    rclpy.init()

    navigator = BasicNavigator()

    # Inspection route, probably read in from a file for a real application
    # from either a map or drive and repeat. (x, y, yaw)
    inspection_route = [
        [2.0, -0.55, 1.57],
        [0.0, -0.55, 1.57],
        [1.5, -0.55, -1.57],
        
    ]

    # Set our demo's initial pose
    # initial_pose = PoseStamped()
    # initial_pose.header.frame_id = 'map'
    # initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    # initial_pose.pose.position.x = 0.0
    # initial_pose.pose.position.y = 0.0
    # initial_pose.pose.orientation.z = 0.0
    # initial_pose.pose.orientation.w = 1.0
    # navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    navigator.waitUntilNav2Active()

    # Send our route
    inspection_points = []
    inspection_pose = PoseStamped()
    inspection_pose.header.frame_id = 'map'
    inspection_pose.header.stamp = navigator.get_clock().now().to_msg()
    for pt in inspection_route:
        inspection_pose.pose.position.x = pt[0]
        inspection_pose.pose.position.y = pt[1]
        # Simplification of angle handling for demonstration purposes
        if pt[2] > 0:
            inspection_pose.pose.orientation.z = 0.707
            inspection_pose.pose.orientation.w = 0.707
        else:
            inspection_pose.pose.orientation.z = -0.707
            inspection_pose.pose.orientation.w = 0.707
        inspection_points.append(deepcopy(inspection_pose))

    navigator.followWaypoints(inspection_points)

    # Do something during our route (e.x. AI to analyze stock information or upload to the cloud)
    # Simply the current waypoint ID for the demonstation
    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(
                'Executing current waypoint: '
                + str(feedback.current_waypoint + 1)
                + '/'
                + str(len(inspection_points))
            )

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Inspection of shelves complete! Returning to start...')
    elif result == TaskResult.CANCELED:
        print('Inspection of shelving was canceled. Returning to start...')
    elif result == TaskResult.FAILED:
        print('Inspection of shelving failed! Returning to start...')

    # go back to start
    #initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    #navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        pass

    exit(0)


if __name__ == '__main__':
    main()
```

---

## 23. Simulation vs. real robot  `[nieuw]`

<sub>simulation-vs-real-robot.md</sub>


What you learned here works on the real TurtleBot3, but a few things differ.
Read this page before you start with the real robot:

| | Simulation (this book) | Real TurtleBot3 (lab) |
|---|---|---|
| ROS 2 version | **Jazzy** (Ubuntu 24.04) | **Humble** (Ubuntu 22.04) |
| Container | `gazebo_turtlebot_cont` (on your laptop) | `turtlebot_<nr>` on the robot + `turtlebot-vis` on your laptop |
| Communication | everything in one container | **Zenoh**: laptop <-> robot over the robot's own wifi `TB-AP-<nr>` |
| `/cmd_vel` message | `geometry_msgs/TwistStamped` | `geometry_msgs/Twist` |
| Teleop | `teleop_twist_keyboard ... -p stamped:=true` | `turtlebot3_teleop teleop_keyboard`, gamepad, or the status page |
| SLAM | `slam_toolbox` (`navigation2.launch.py slam:=True`) | **Cartographer** |
| Clock | `use_sim_time:=True` (Gazebo clock) | real clock: **no** `use_sim_time` |
| Who drives? | only you | twist_mux: gamepad > web page > `/cmd_vel` (your code, Nav2) |
| Your files | in the simulation container | `/root/ros2_ws` (laptop: `turtlebot_vis/ros2_ws`) |

## Example: publish cmd_vel

Simulation (Jazzy):

```python
from geometry_msgs.msg import TwistStamped
msg = TwistStamped()
msg.header.stamp = self.get_clock().now().to_msg()
msg.header.frame_id = 'base_link'
msg.twist.angular.z = 0.2
self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
```

Real robot (Humble):

```python
from geometry_msgs.msg import Twist
msg = Twist()
msg.angular.z = 0.2
self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
```

{% hint style="info" %}
A node that publishes the wrong type often gives no clear error: the robot simply
doesn't move. Check with `ros2 topic info /cmd_vel` which type is expected.
{% endhint %}

