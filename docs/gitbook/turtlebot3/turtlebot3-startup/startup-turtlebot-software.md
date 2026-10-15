# Startup turtlebot software

Start the basic TurtleBot software ("bringup") inside the robot container.

Open a terminal inside the robot container (SSH + `docker exec -it turtlebot_<nr> bash`,
see [Connect to the turtlebot3](connect-to-the-turtlebot3.md)) and start:

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

{% hint style="info" %}
First the message `[usb_power] USB-stroom was uit (spaarstand) - aanzetten...`
can appear: the USB power is switched on, the lidar starts turning and the
bringup continues after a few seconds. That is normal.
{% endhint %}

This starts up the following functionalities:

* Reading the lidar sensor (`/scan`)
* Connection with the OpenCR board: motors, encoders, IMU, battery, buttons
* Calculation of the odometry (`/odom`)
* Publishing the TF (`/tf`, `/tf_static`)

{% hint style="warning" %}
**Keep this terminal open.** `CTRL + C` - or closing the terminal / SSH window -
stops the bringup, and the robot stops publishing.
{% endhint %}

## Check

Open a **second** robot terminal (new WSL terminal, `ssh ...`,
`docker exec -it turtlebot_<nr> bash`) and check:

```sh
ros2 topic list
ros2 topic hz /scan
```

You should see `/scan`, `/odom`, `/imu`, `/battery_state`, ... and about 5 scans
per second.

{% hint style="warning" %}
Error `could not open port /dev/ttyACM0` or `device busy`? The bringup is
probably already running (another terminal, a classmate, or the status page).
Check with `ros2 node list` - you only need one bringup per robot.
{% endhint %}
