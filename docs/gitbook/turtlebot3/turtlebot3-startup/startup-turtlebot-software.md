# Startup turtlebot software

Start the basic TurtleBot software ("bringup") inside the robot container.

Open a terminal inside the robot container (web terminal or SSH +
`docker exec -it turtlebot_<nr> bash`, see
[Connect to the turtlebot3](connect-to-the-turtlebot3.md)) and start:

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

This starts up the following functionalities:

* Reading the lidar sensor
* Calculation of the odometry
* Publishing the TF
* Connection with the OpenCR board (motors, IMU, battery, buttons, buzzer)

Keep this terminal open: `CTRL + C` stops the bringup again.

{% hint style="info" %}
The first time, start the bringup yourself in the terminal - that's how you
learn it. Later you can also use the status page: **Rijden > Kaart maken** and
**Navigatie > Start** start the bringup automatically. Running launches are shown
under **Actief** in the header, each with its own stop button.
{% endhint %}

{% hint style="warning" %}
Is the bringup already running (started from the status page)? Then a second
`ros2 launch ... robot.launch.py` gives errors (the serial port of the OpenCR is
busy). Check **Actief** on the status page first.
{% endhint %}
