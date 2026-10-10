# Setup laptop (student)

Your laptop talks to the robot with ROS 2 over **Zenoh**: the `turtlebot-vis`
container on your laptop connects to the Zenoh router on the robot
(`10.0.<nr>.10`, TCP port 7447).

{% hint style="success" %}
With Zenoh the laptop makes the connection itself, so the Windows/Hyper-V
**firewall rules from previous years are no longer needed**.
{% endhint %}

## Docker container

Open a WSL terminal and clone the repository - the **`zenoh` branch**:

```sh
git clone -b zenoh https://github.com/JeremyLebon/turtlebot_vis.git
```

{% hint style="danger" %}
Don't forget `-b zenoh`. Without it you get the old version (DDS), which can't
talk to the robots anymore.
{% endhint %}

Go inside the directory:

```sh
cd turtlebot_vis
```

Download the ready-made image (much faster than building it yourself):

```sh
docker compose pull
```

## Set your robot number

Open the `.env` file:

```sh
nano .env
```

Change **both** lines to the number of your robot (example for TurtleBot 5):

```
ROS_DOMAIN_ID=5
ROBOT_ZENOH_IP=10.0.5.10
```

{% hint style="warning" %}
`ROS_DOMAIN_ID` must be exactly the robot number. With a wrong domain ID the
connection works, but you don't see a single topic.
{% endhint %}

Save with `CTRL + S`, close with `CTRL + X`.

## Start the container

```sh
docker compose up
```

Open a new WSL terminal and connect to the container:

```sh
docker exec -it turtlebot-vis bash
```

Check that you see the topics of your robot (the bringup must be running):

```sh
ros2 topic list
```

{% hint style="info" %}
Empty list? Run `ros2 daemon stop` and try again. Still nothing: is your laptop
on `TB-AP-<nr>`, are both numbers in `.env` correct, and is the bringup
running? The status page > **Info** shows the exact connect command for your robot.
{% endhint %}

Start RViz2:

```sh
rviz2
```

When clicking Fixed Frame, you should see several frames/links available.
Otherwise there is a problem.

## Where to store your code

Store your scripts in `/root/ros2_ws` inside the container. That directory is
the folder `turtlebot_vis/ros2_ws` on your laptop, so your files survive a
restart of the container. See [Location files on WSL](../location-files-on-wsl.md).
