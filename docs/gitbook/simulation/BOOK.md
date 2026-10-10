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

## 2. Turtlebot in simulation  `[ongewijzigd]`

<sub>turtlebot-in-simulation.md</sub>


## Tools

###

---

### 3. Objectives  `[ongewijzigd]`

<sub>turtlebot-in-simulation/objectives.md</sub>


In this exercise, the objectives are the following:

* Learn to work with Gazebo (simulator)
* Combine Gazebo with ROS 2
* Learn to drive the robot in a simulated environment
* Make your first ROS 2 node
* Learn to map an environment with slam\_toolbox
* Learn to navigate autonomously in a mapped environment

---

### 4. Tools  `[ongewijzigd]`

<sub>turtlebot-in-simulation/tools.md</sub>


###

### Gazebo

Gazebo is an open-source 3D robot simulator that allows users to accurately and efficiently simulate populations of robots in complex indoor and outdoor environments. It provides a robust physics engine and models for sensors and actuators. In the ROS 2 ecosystem, the newer version (Gazebo Sim) is the standard for testing robot autonomy, relying on the `ros_gz_bridge` for real-time communication with the ROS control stack.

<div data-full-width="false" data-with-frame="true"><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAqtGNSo6CAyvDoyLjVAR%2Fimage.png?alt=media&amp;token=9e38f2e4-8593-4c06-8139-dd1ecaa342b1" alt=""><figcaption></figcaption></figure></div>

### Rviz

RViz (ROS Visualization) isn't a simulator but a 3D visualization tool within the ROS ecosystem, used to display sensor data, robot models, and algorithm output (like navigation paths and maps) published on ROS topics. It's essential for debugging and monitoring the state of any robot—real or simulated—by aggregating and graphically rendering data streams in a unified 3D environment.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9MoVmrG1mIOWkqk0T8HC%2Fimage.png?alt=media&amp;token=8855bc88-bff9-46e6-a32c-03a46f5601fc" alt=""><figcaption></figcaption></figure>

---

### 5. Startup  `[ongewijzigd]`

<sub>turtlebot-in-simulation/startup.md</sub>


Open a new terminal (Ubuntu 22.04).

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fsu1ojyU78ot109TUCruT%2Fimage.png?alt=media&amp;token=bd97d707-024e-45cb-b7f4-bdfc6f29c983" alt=""><figcaption></figcaption></figure>

Connect to the running Docker container with the command below.

```sh
docker exec -it gazebo_turtlebot_cont bash
```

Select the `burger` turtlebot3 as loaded model in Gazebo with the following command

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

Normally, the world below should be loaded. Try the find the turtlebot3 with the mouse and scrolling.

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FAqtGNSo6CAyvDoyLjVAR%2Fimage.png?alt=media&amp;token=9e38f2e4-8593-4c06-8139-dd1ecaa342b1" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ45E9208uQDSv4e1ceNe%2Fimage.png?alt=media&amp;token=2833a4bb-a0e9-4f06-97a7-0efef922290c" alt=""><figcaption></figcaption></figure></div>

By clicking `CRTL+C` in the terminal gazebo and ros2 launch can be stopped.

## Load the turtlebot in the house world

Try the following command to drop the turtle in the house environment.

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
</strong></code></pre>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FITbPVgiVyF6yDsQRFA21%2Fimage.png?alt=media&amp;token=986a0d24-241a-42b1-b2c8-73de09b6c412" alt=""><figcaption></figcaption></figure>

By clicking `CRTL+C` in the terminal gazebo and ros2 launch can be stopped.

---

### 6. Moving the turtlebot  `[ongewijzigd]`

<sub>turtlebot-in-simulation/moving-the-turtlebot.md</sub>


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

Select the graph with Plugins > Visualisation> Plot

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FFDOM01gw9GcX0mVKRweZ%2Fimage.png?alt=media&amp;token=8ac28a21-6e1d-4b3a-870a-9acca6687e53" alt=""><figcaption></figcaption></figure>

</details>

Close rqt with CRTL + C in the terminal

---

### 7. Show me the robot  `[ongewijzigd]`

<sub>turtlebot-in-simulation/show-me-the-robot.md</sub>


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

Select as fixed frame as the odom frame

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

Use the following command to see a list op the ros2 topics. Use a new terminal if needed.

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

### Look at the /joint\_state topic

If you echo the `/joint_states` And you let the robot turn. You should see the joint state position and velocity change.&#x20;

<div><figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FIf9Qd2kLikFoRpBieMgl%2Fimage.png?alt=media&amp;token=1c73090f-2dd6-49bf-af5b-439e6599b5cc" alt=""><figcaption></figcaption></figure> <figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fc7iuLHaMdenJRVFX2ogG%2Fimage.png?alt=media&amp;token=d87f8603-ba1e-4e0e-8fdd-d0c49bc318f2" alt=""><figcaption></figcaption></figure></div>

&#x20;          &#x20;

---

### 8. Here come the sensors  `[ongewijzigd]`

<sub>turtlebot-in-simulation/here-come-the-sensors.md</sub>


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
* The angle increment: 0.017 rad or 0.1 degree
* Minimum range detected: 0.1199 m
* Maximum range detected: 3.5m
* In the item *ranges,* you can see all distances of every point.

Try driving around and see the lidar scan change.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FMaXjRFrwHvgKRlsR0a3T%2FRobot_scan_demo.gif?alt=media&amp;token=3d835e48-bba3-4b98-b949-1d8553e7342c" alt=""><figcaption></figcaption></figure>

## Odometry

The odometry shows us the path that the robot has been driven based on the wheel rotation.

Click Add and select the tab *By topic,* and select the topic */odom.*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9LMmGp6LFrOXsNilUrMK%2Fimage.png?alt=media&amp;token=039c800b-c760-47af-b926-2650cd3df440" alt=""><figcaption></figcaption></figure>

Collapse the item Odometry on the left. And change the parameter to keep to 500. This means the last 500 locations will be visualised in Rviz2. Then try driving around.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZkYe8O1NTIsSyi5CcPxG%2Fimage.png?alt=media&amp;token=31694e11-6e09-4af2-bc71-fcccdb0ebc53" alt=""><figcaption></figcaption></figure>

&#x20;Then try driving around. You should get a collection of arrows showing the location and orientation of the robot.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FRyxHCooFUVTT1NJ48pNv%2FRobot_odom_demo.gif?alt=media&amp;token=182cad3a-930f-4f77-ad83-6552b5f2eef2" alt=""><figcaption></figcaption></figure>

## IMU

The Turtlebot3 has a build in imu sensor. This can't be directly shown in RViz2.&#x20;

With `ros2 topic echo`, the real-time value can be shown. Open a new terminal if needed. You can see the linear z acceleration is roughly the known 9.81 m/s².&#x20;

```
ros2 topic echo /imu
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FgwaDgaLqETpefgG11ng0%2Fimage.png?alt=media&amp;token=996d4617-b5d6-4fb5-85cb-761768b59c2b" alt=""><figcaption></figcaption></figure>

---

## 9. The first ros2 node  `[ongewijzigd]`

<sub>the-first-ros2-node.md</sub>


## Connect to the container via VScode

Make sure the `turtlebot3_gazebo` node and t`eleop_twist_keyboard` is running.

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

You should now be inside the Docker container. You may be asked to select a directory in the Docker container.

## Make your first ROS 2 node

### Subscribe to /odom

The objective is to read out the location of the turtlebot with our own written Python script.

Make a new directory, `turtlebot` and make a `turtlebot_subscribe.py` script.

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
        
        self.get_logger().info("Publishing TwistStamped messages on /cmd_vel_stamped")

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

## 10. SLAM / Mapping  `[ongewijzigd]`

<sub>slam-mapping.md</sub>


- [Startup](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/startup.md)
- [Start mapping](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/start-mapping.md)
- [Save map](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/slam-mapping/save-map.md)

---

### 11. Startup  `[ongewijzigd]`

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

### 12. Start mapping  `[ongewijzigd]`

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

### 13. Save map  `[gewijzigd]`

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

## 14. Autonomous Navigation  `[gewijzigd]`

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

### 15. Autonomous driving with python library  `[ongewijzigd]`

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

## 16. Simulation vs. real robot  `[nieuw]`

<sub>simulation-vs-real-robot.md</sub>


**New page** (suggested at the end of this book, before going to the real
TurtleBot3). What you learned here works on the real robot, but a few things
differ:

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

