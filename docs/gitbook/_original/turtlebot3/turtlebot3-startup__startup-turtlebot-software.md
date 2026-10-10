> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/startup-turtlebot-software.md).

# Startup turtlebot software

Startup the turtlebot software inside the docker container onto the turtlebot.

Make a new SSH connection with the turtlebot

```
ssh turtlebot-rpi5@192.168.60.6x
```

password: turtlebot

Connect to the Docker container inside with the following command

```
docker exec -it turtlebot_x bash
```

{% hint style="warning" %}
`x` : is the number of the turtlebot
{% endhint %}

Start the basic turtlebot software

```
ros2 launch turtlebot3_bringup robot.launch.py
```

This starts up the following functionalities:

* Reading the Lidar sensor
* Calculation of the odometry
* Publishing the TF
* Connection with the OpenCR board
