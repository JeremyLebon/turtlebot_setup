# Turtlebot3

_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/turtlebot3/`._

---

## 1. Turtlebot3 in the real world  `[ongewijzigd]`

<sub>turtlebot3-in-the-real-world.md</sub>

# Turtlebot3 in the real world

---

## 2. Objectives  `[ongewijzigd]`

<sub>objectives.md</sub>


In this exercise, the objectives are the following:

* Learn to work with the real turtlebot
* Combine ROS2 and the turtlebot
* Learn to drive the robot in a real environment
* Make your ROS 2 node (subscribe and publish)
* Learn to map an environment with Cartographer
* Learn to navigate autonomously in a mapped environment

---

## 3. Turtlebot3 - startup  `[ongewijzigd]`

<sub>turtlebot3-startup.md</sub>


- [Connect to the WIFI](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/connect-to-the-wifi.md)
- [Startup of the turtlebot3](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/startup-of-the-turtlebot3.md)
- [Connect to the turtlebot3](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/connect-to-the-turtlebot3.md)
- [Startup docker](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/startup-docker.md): Startup the docker container inside the turtlebot
- [Startup turtlebot software](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/startup-turtlebot-software.md): Startup the turtlebot software inside the docker container onto the turtlebot.
- [Setup laptop (student)](https://vives-4.gitbook.io/turtlebot3/turtlebot3-startup/setup-laptop-student.md)

---

### 4. Connect to the WIFI  `[gewijzigd]`

<sub>turtlebot3-startup/connect-to-the-wifi.md</sub>


Every TurtleBot has its **own wifi network** (access point). This keeps the
connection fast and stable: you don't share the wifi with the other groups.

Check the number of your TurtleBot: see the sticker on the robot (and on its
access point). Connect your laptop to the wifi of **your** robot:

* Wifi name: `TB-AP-<nr>` (for example `TB-AP-05` for TurtleBot 5)
* Password: see lab notes

{% hint style="warning" %}
The robot wifi does not always have internet. Windows (and your phone) may then
silently switch to another network (eduroam, mobile data) - and the robot is
"gone".

* Windows: in the wifi list, untick **Connect automatically** for the other
  networks during the lab.
* Phone: when it says *"Wifi has no internet"*, choose **Stay connected**, or
  switch off mobile data.
{% endhint %}

Open a WSL terminal and check that you can reach your robot (replace `<nr>` by
the number of your robot, without a leading zero: robot 5 -> `10.0.5.10`):

```sh
ping 10.0.<nr>.10
```

You should get an answer every second. `CTRL + C` stops the ping.

---

### 5. Startup of the turtlebot3  `[gewijzigd]`

<sub>turtlebot3-startup/startup-of-the-turtlebot3.md</sub>


The TurtleBot3 can be powered in 2 ways:

* Via DC adapter
* Via battery

Connect the battery to the TurtleBot and switch it on.

* The OpenCR board plays a short melody.
* After about 1 minute the Raspberry Pi is ready: the robot software starts
  **automatically** (you don't have to start a Docker container yourself) and
  you hear a short startup beep.

{% hint style="info" %}
Everything runs in a Docker container on the robot (`turtlebot_<nr>`). It starts
by itself after every boot and keeps running.
{% endhint %}

Continue with [Connect to the turtlebot3](connect-to-the-turtlebot3.md) and check
the battery voltage and the **labo-check** on the status page.

---

### 6. Connect to the turtlebot3  `[gewijzigd]`

<sub>turtlebot3-startup/connect-to-the-turtlebot3.md</sub>


## The status page (Fenix)

Every robot serves its own web page. With your laptop (or phone) on the robot
wifi `TB-AP-<nr>`, open a browser:

```
http://10.0.<nr>.10:8080
```

Check in the header:

* the **robot name** (is this your robot?)
* the **battery** icon (hover over it: voltage; 0 % = 11.0 V, below that the
  OpenCR switches the motors off)
* the **labo-check** icon (tick): green = everything OK. Click it for the full list.

{% hint style="info" %}
Tabs: **Rijden** (drive, camera, make a map), **Navigatie** (navigate on a map),
**Projecten** (ready-made demos), **Info** (robot health, topics, logs).
The red **STOP** button stops everything that drives.
{% endhint %}

## A terminal on the robot

For the ROS 2 exercises you need a terminal **inside the robot container**.
Two ways:

### Option 1 - web terminal

Click the `>_` button in the header of the status page (opens
`http://10.0.<nr>.10:7681`). Login: see lab notes. You are directly inside the
robot container.

### Option 2 - SSH

Open a WSL terminal:

```sh
ssh turtlebot@10.0.<nr>.10
```

* username: `turtlebot`
* password: see lab notes

{% hint style="warning" %}
The password stays invisible while typing. Say `yes` when a fingerprint is
suggested the first time.
{% endhint %}

You are now on the Raspberry Pi of the robot. Go inside the robot container:

```sh
docker exec -it turtlebot_<nr> bash
```

{% hint style="warning" %}
`<nr>` is the robot number **without** a leading zero: robot 5 ->
`docker exec -it turtlebot_5 bash`. Press `TAB` to autocomplete.
{% endhint %}

---

### 7. Startup docker  `[gewijzigd]`

<sub>turtlebot3-startup/startup-docker.md</sub>


{% hint style="success" %}
Nothing to do here anymore: the Docker container on the robot (`turtlebot_<nr>`)
starts **automatically** when the robot boots, and restarts by itself if needed.
{% endhint %}

Check that it runs: on the status page `http://10.0.<nr>.10:8080` the
connection icon (plug) in the header is green, and the robot name is shown.

Or via SSH on the robot:

```sh
docker ps
```

You should see a container `turtlebot_<nr>`.

{% hint style="danger" %}
Don't run `docker compose pull` or `docker compose up/down` yourself. Updating
the robot software is done by the lecturer (status page > Beheer).
{% endhint %}

---

### 8. Startup turtlebot software  `[gewijzigd]`

<sub>turtlebot3-startup/startup-turtlebot-software.md</sub>


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

---

### 9. Setup laptop (student)  `[gewijzigd]`

<sub>turtlebot3-startup/setup-laptop-student.md</sub>


Your laptop talks to the robot with ROS 2 over **Zenoh**: the `turtlebot-vis`
container on your laptop connects to the Zenoh router on the robot
(`10.0.<nr>.10`, TCP port 7447).

{% hint style="success" %}
With Zenoh the laptop makes the connection itself, so the Windows/Hyper-V
**firewall rules from previous years are no longer needed**.
{% endhint %}

## Docker container

Open a WSL terminal and clone the repository:

```sh
git clone https://github.com/JeremyLebon/turtlebot_vis.git
```

{% hint style="info" %}
Already cloned in a previous year? Update it: `cd turtlebot_vis`,
`git checkout .env` (throws away your old robot number, otherwise `git pull`
refuses), `git pull`, `git submodule update --init`. The old version (DDS) can't
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

---

## 10. Visualise the robot  `[ongewijzigd]`

<sub>visualise-the-robot.md</sub>


Select as Fixed frame the odom frame.

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FIWLWvYorpN8ylreiH1lM%2Fimage.png?alt=media&amp;token=18f12e84-aa2a-4590-aec8-6bf47c307e74" alt=""><figcaption></figcaption></figure>

Try to show the RobotModel, odometry, TF and laserscan in RViz2

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2F6mYEBmeKnLrh8C6W5M8Y%2Fimage.png?alt=media&amp;token=f700b34e-308d-4445-b580-d844b375abd2" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
To see the laserscan in RViz2, the **reliability policy** should be changed to Best Effort. Otherwise, the scan isn't shown.

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FbmNIRml1AdtYoQZ0KFmX%2Fimage.png?alt=media\&token=279c9ddd-a69e-490d-af55-15ef51e869c6)
{% endhint %}

<details>

<summary>Solutions</summary>

**Robotmode**l

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FFX38RMI9NFq2kqvjaOeB%2Fimage.png?alt=media&amp;token=aa4a8c31-dfa1-49c5-8e02-45a46121de52" alt=""><figcaption></figcaption></figure>

Odometry

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2Fw8nCD0PTMebt5lEioLFK%2Fimage.png?alt=media&amp;token=bf460f68-146f-408f-a767-a348926a47b7" alt=""><figcaption></figcaption></figure>

**TF**

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FCJGWU9Gsh4SWVb0W7Kew%2Fimage.png?alt=media&amp;token=5c1aea42-d68b-4843-9b0e-9fc7e527f994" alt=""><figcaption></figcaption></figure>

Scan (lidar)

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FhKyV5wd0zcVavYQp73Cx%2Fimage.png?alt=media&amp;token=daacc3bf-f70e-4fa7-90df-e9b1806a012b" alt=""><figcaption></figcaption></figure>

</details>

---

## 11. Controlling the robot  `[ongewijzigd]`

<sub>controlling-the-robot.md</sub>


Manual controlling of the robot can be done in several ways:

* By keyboard
* By gamepad

---

### 12. Manual control by terminal  `[gewijzigd]`

<sub>controlling-the-robot/manual-control-by-terminal.md</sub>


Open a new WSL terminal and connect to the `turtlebot-vis` container.

Solution

```
docker exec -it turtlebot-vis bash
```

Start the teleop command.

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

```sh
ros2 run turtlebot3_teleop teleop_keyboard
```

{% hint style="success" %}
Other keys are used for controlling the TurtleBot than in the previous commands:
read the instructions in the terminal.
{% endhint %}

You should see the TurtleBot move in RViz2.

## Who is in control? (twist_mux)

Several things can drive the robot at the same time. The robot decides with
**twist_mux** - the highest priority wins:

| Source | Topic | Priority |
|---|---|---|
| Gamepad (F710) | `/cmd_vel_joy` | 100 (highest) |
| Status page (arrows on Rijden / Navigatie) | `/cmd_vel_web` | 50 |
| Your own nodes, Nav2, teleop_keyboard | `/cmd_vel` | 10 |

As long as a higher source sends commands, yours are ignored. 0.5 s after it
stops, the next one takes over again. So with the gamepad or the web page you
can **always** take over the robot.

{% hint style="info" %}
You can also drive from the status page: **Rijden**, arrows bottom-left (keep
pressed), or the keyboard (arrows / WASD, space = stop).
{% endhint %}

---

### 13. Manual control with gamepad  `[gewijzigd]`

<sub>controlling-the-robot/manual-control-with-gamepad.md</sub>


Plug the USB receiver of the Logitech F710 into the Raspberry Pi of the robot
and switch the gamepad on.

{% hint style="danger" %}
Ensure the robot is on the ground or its wheels are in contact with the ground.
{% endhint %}

Switch the gamepad on via the status page: **Rijden**, top right, gamepad
button. The button turns blue when the gamepad is active; hover over it to see
whether the receiver is detected.

How to control the TurtleBot:

1. Keep **LB** (left shoulder button) pressed - this is the enable button.
2. Use the **left stick** to drive forward/backward and the **right stick** to turn.
3. Keep **RB** pressed as well to drive faster.

{% hint style="info" %}
The gamepad has the highest priority: it always wins over the web page and over
your own nodes (see [Manual control by terminal](manual-control-by-terminal.md)).
{% endhint %}

Try to drive around. This can later be used to map the environment.

Show the progress to the lecturer.

---

## 14. See turtlebot3 topics  `[ongewijzigd]`

<sub>see-turtlebot3-topics.md</sub>


Get an overview of all available ROS 2 topics on the TurtleBot via terminal command.

Try to find the following information

* Battery voltage
* Value encoder left
* Value encoder right
* Button value on OpenCR
* odom
* Laserscan data (not needed in rqt)

Show it to the lecturer.

---

## 15. ROS2 nodes  `[gewijzigd]`

<sub>ros2-nodes.md</sub>


To make ROS 2 nodes in Python, 2 ways can be used:

1. **On your laptop** - in the `turtlebot-vis` container: VS Code > Remote
   Explorer > WSL > Dev Containers > `turtlebot-vis`. Store your code in
   `/root/ros2_ws`.
2. **On the robot** - in the robot container `turtlebot_<nr>`: VS Code > Remote
   Explorer > SSH (`turtlebot@10.0.<nr>.10`) > attach to the container. Store
   your code in `/root/ros2_ws` there as well (on the robot this is
   `~/turtlebot_setup/ros2_ws`).

{% hint style="info" %}
Both `ros2_ws` folders survive restarts and robot updates. Anything you store
elsewhere in a container can be lost.
{% endhint %}

{% hint style="warning" %}
On the robot: build your own packages with `colcon build` in `/root/ros2_ws`.
The overlay (`install/setup.bash`) is sourced automatically in every new terminal.
{% endhint %}

---

### 16. Read in the scan topic  `[gewijzigd]`

<sub>ros2-nodes/read-in-the-scan-topic.md</sub>


Make a Python script (`sub_scan.py`) that is subscribed to the `/scan` topic. Make the script inside the `turtlebot-vis` container in the directory `/root/ros2_ws`.

Use the Remote explorer extension in VScode to make connection with the WSL and the running docker container. See the previous [session](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node) (there the container is `ros2-jazzy-gazebo-turtlebot`, here it is `turtlebot-vis`)

Sometimes the extension python has be installed in the docker container via VScode

## Add the needed libraries

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy
import numpy as np
import math
```

{% hint style="info" %}

* `rclpy`: ROS 2 Python library
* `Node`: Base class for ROS 2 nodes
* `LaserScan`: Message type published on `/scan`
* `QoSProfile` & `ReliabilityPolicy`: Needed to match subscriber QoS with publisher
* `numpy`: Calculate the mean of the laserscan
* `math`: check if something is finite
  {% endhint %}

## Main function and lifecycle

```python
def main(args=None):
    rclpy.init(args=args)
    node = ScanSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

* `rclpy.init(args=args)`: initializes the ROS 2 client library (must be called before creating nodes).
* `node = ScanSubscriber()`: instantiates the node (runs `__init__`).
* `rclpy.spin(node)`: enters the ROS event loop, processing incoming messages and calling callbacks until shutdown.
* `except KeyboardInterrupt`: lets the user stop the node with `Ctrl+C`.
* `node.destroy_node()`: cleans up node resources.
* `rclpy.shutdown()`: finalizes the rclpy library and releases network resources.

<pre class="language-python"><code class="lang-python"><strong>if __name__ == '__main__':
</strong>    main()
</code></pre>

* Standard Python guard so `main()` runs only if the file is executed as a script (not if imported as a module).

## Make a Node class

Add the class above the `main` function.

```python
class ScanSubscriber(Node):
    def __init__(self):
        super().__init__('sub_scan')
```

\
Change the QoS (Quality of Service)&#x20;

Add this to the `__init__` function

```python
qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    depth=10
)
```

* ROS 2 topics use Quality of Service (QoS).
* TurtleBot3 /scan LIDAR uses Best Effort, so we must match it.
* depth=10 sets the queue size.

Add the `create_subscription`  also to the `__init__` function.

```python
self.subscription = self.create_subscription(
    LaserScan,
    '/scan',
    self.scan_callback,
    qos_profile
)
```

* `create_subscription(...)` registers a subscriber on the node.
  * `LaserScan`: the message class expected.
  * `'/scan'`: topic to listen to.
  * `self.scan_callback`: function to call each time a message arrives.
  * `qos_profile`: ensures compatibility with the LIDAR publisher
* The returned subscription object is stored in `self.subscription` to keep a reference (prevents garbage collection).

{% hint style="info" %}
Make sure the indentation in Python is correct!
{% endhint %}

## Log vs. print

To print data to the terminal don't use the print statement. The print causes a significant delay. Use the logger instead. At this line below in the `__init__` function

```python
self.get_logger().info('LaserScan subscriber node started!')
```

## Callback function

Add the callback function to the class.

```python
def scan_callback(self, msg):
```

{% hint style="info" %}
This method is called each time a `LaserScan` message is received. `msg` is an instance of `sensor_msgs.msg.LaserScan`.
{% endhint %}

## Laserscan msg info

Explain fields of `LaserScan` (important to understand `msg.ranges`):

* `msg.header` — timestamp and frame id
* `msg.angle_min`, `msg.angle_max`, `msg.angle_increment` — describe the angular span and resolution of the scan
* `msg.range_min`, `msg.range_max` — valid range limits for the sensor
* `msg.ranges` — list (array) of distance measurements, usually one per angle step
* `msg.intensities` — (optional) reflectance / intensity values

Add the code below to the callback function

```python
# Filter out invalid (non-finite) values
msg.ranges = [r for r in msg.ranges if math.isfinite(r)]
```

This line removes any invalid values from msg.ranges.

* `msg.ranges` is typically a list of distance readings (for example, from a LIDAR sensor).
* `math.isfinite(r)` checks if a value is a real number — not `inf`, `-inf`, or `NaN`.
* The result is a cleaned list containing only valid distance measurements.

```python
# Log how many valid points we have
self.get_logger().info(f"Valid ranges: {len(msg.ranges)}")
```

This logs the number of valid range readings that remain after filtering.\
It helps you verify that the data is being received and processed correctly.

Below you see the build up of the laserscan. You get roughly 220-230 points per rotation (LDS-02 lidar, ~5 rotations per second)

<img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2Fjl07REjZyMmR6JgmDR3O%2Ffile.excalidraw.svg?alt=media&amp;token=22bfd257-79c7-429b-afb2-85ec2fa16979" alt="" class="gitbook-drawing">

```python
# Get front sector — for example, 15 readings on each side of the forward direction
n = 15
front_full = msg.ranges[:n] + msg.ranges[-n:]
```

This selects the **front part** of the sensor’s field of view.

* The first `n` values (`msg.ranges[:n]`) represent readings from one side of the front.
* The last `n` values (`msg.ranges[-n:]`) represent readings from the other side of the front.\
  By combining them, `front_full` contains readings that roughly correspond to what’s **in front of the robot**.

```python
# Compute mean safely (in case list is empty)
mean_front = np.mean(front_full) if front_full else float('nan')
```

This computes the **average distance** in the front sector.

* It uses `numpy.mean()` to calculate the mean.
* If `front_full` is empty (e.g., no valid readings), it safely returns `NaN` instead of causing an error.

```python
self.get_logger().info(f"Front ranges ({len(front_full)}): mean={mean_front:.3f}")
```

Finally, this logs how many front readings were used and what their average distance was — formatted to three decimal places.

---

#### 17. Exercise  `[ongewijzigd]`

<sub>ros2-nodes/read-in-the-scan-topic/exercise.md</sub>


Try to filter out a right, back and left part. Try to print this in the terminal.

Show the result to the lecturer.

<img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FODudHqthpJTbo5FEnO7l%2Ffile.excalidraw.svg?alt=media&amp;token=95719208-4142-42a1-8c38-e621c706bd27" alt="" class="gitbook-drawing">

---

### 18. Read the battery level  `[ongewijzigd]`

<sub>ros2-nodes/read-the-battery-level.md</sub>


Make a new python script (`sub_battery_level.py`) in the docker container turtlebot-vis.

Check the ros2 msg typ of the `/battery_state` topic. Add this as a python library.

Try to subscribe to the `/battery_state` topic.

Check what data is available in the ros2 topic `/battery_state`.

Print the voltage value and SoC (state of charge) of the battery to the terminal.

Print a warning when the SoC is below the 50%

Show when ready to the lecturer.

---

### 19. Read the encoder value  `[ongewijzigd]`

<sub>ros2-nodes/read-the-encoder-value.md</sub>


Make a new python script (`sub_encoders.py`) in the docker container turtlebot-vis.

Check if there is a ros2 topic that contains the encoder values

Check the ros2 msg typ of the ros2 topic. Add this as a python library inside in the script.

Try to subscribe to the ros2 topic.

Print the encoder values to the terminal.

Try to calculate the average speed of the wheels.

Show when ready to the lecturer.

---

### 20. Drive 10cm with a button  `[gewijzigd]`

<sub>ros2-nodes/drive-10cm-with-a-button.md</sub>


Make a Python script (`pub_controlling_the_robot.py`). Make the script inside the `turtlebot-vis` container in the directory `/root/ros2_ws`.

## Imports and top-level setup

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import time
```

* `rclpy` — the ROS 2 Python client library. It provides node lifecycle, spinning, and other ROS 2 functions.
* `Node` — base class for creating ROS 2 nodes in Python.
* `Twist` — ROS message type used to send velocity commands (`linear` and `angular`) (commonly published on `/cmd_vel`).
* `Joy` — ROS message type published by joystick drivers; it contains `axes` and `buttons` arrays.
* `time` — Python standard library module, used here for simple time and sleeps.

### Class definition and constructor

```python
class MoveOnJoyButton(Node):
    def __init__(self):
        super().__init__('move_on_joy_button')

        # Publisher voor snelheid
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Abonneren op de joystick
        self.sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)

        self.last_button_state = 0
        self.get_logger().info("Druk op A (knop 0) op de controller om 10 cm vooruit te rijden")
```

* `MoveOnJoyButton` is a ROS 2 node class (inherits from `Node`).
* `super().__init__('move_on_joy_button')` sets the node name to `move_on_joy_button`.
* `self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)` creates a publisher that will publish `Twist` messages to the `/cmd_vel` topic. The `10` is the queue size (history depth) for the publisher.
* `self.sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)` subscribes to the joystick input on the `/joy` topic. When a `Joy` message arrives, `self.joy_callback` is called.
* `self.last_button_state = 0` stores the previous state of the A button so the code can detect the **rising edge** (press event).
* `self.get_logger().info(...)` logs an informational message. The logged text in your code is Dutch; it tells the user which button to press. (This is executed once when the node starts.)

### The joystick callback

```python
def joy_callback(self, msg: Joy):
    # Controleer of A is ingedrukt (index 0)
    if len(msg.buttons) > 0:
        pressed = msg.buttons[0]
        if pressed == 1 and self.last_button_state == 0:
            self.get_logger().info("A-knop ingedrukt → rijden 10 cm vooruit")
            self.drive_forward(0.10)
        self.last_button_state = pressed
```

* `joy_callback` is executed every time a `Joy` message arrives. `msg.buttons` is an array of integers (0 or 1), where `msg.buttons[0]` corresponds to the A button by convention in many controllers.
* `if len(msg.buttons) > 0:` ensures `msg.buttons[0]` exists before accessing it.
* `pressed = msg.buttons[0]` reads current state of button A.
* `if pressed == 1 and self.last_button_state == 0:` detects a **rising edge**: the button was previously unpressed (`0`) and is now pressed (`1`). That prevents repeated triggers while the button is held down.
* On that rising edge the node logs a message (Dutch: “A button pressed → drive 10 cm forward”) and calls `self.drive_forward(0.10)` to move 0.10 meters forward.
* `self.last_button_state = pressed` updates the stored state for the next callback.

### The drive routine

```python
def drive_forward(self, distance):
    speed = 0.05  # m/s
    duration = distance / speed

    twist = Twist()
    twist.linear.x = speed

    end_time = time.time() + duration
    while time.time() < end_time:
        self.cmd_pub.publish(twist)
        time.sleep(0.05)

    twist.linear.x = 0.0
    self.cmd_pub.publish(twist)
    self.get_logger().info("Beweging voltooid")
```

* `drive_forward(self, distance)` takes a distance in meters (here called with `0.10` for 10 cm).
* `speed = 0.05` sets a constant forward linear speed of 0.05 m/s.
* `duration = distance / speed` calculates how many seconds to publish that speed to cover the requested distance. Example: `0.10 / 0.05 = 2 seconds`.
* A `Twist()` message is created and `twist.linear.x = speed` sets forward velocity. (Other fields remain zero.)
* `end_time = time.time() + duration` sets a wall-clock time when motion should stop.
* The `while` loop repeatedly publishes the `Twist` message until the end time is reached. Inside the loop it sleeps `0.05` seconds between publishes — this effectively publishes at \~20 Hz.
* After the loop, the code sets `twist.linear.x = 0.0` and publishes once to stop the robot.
* It logs a message in Dutch: “Movement complete”.

**Important note about this implementation:** the `drive_forward` method is *blocking*. It uses `time.sleep()` and a while loop inside the callback chain. That blocks the node’s thread while driving and prevents other incoming callbacks from running on the same thread.

{% hint style="warning" %}
This node publishes on `/cmd_vel`: the lowest priority in **twist_mux**. While
someone drives with the gamepad or the arrows on the status page, your commands
are ignored (see [Manual control by terminal](../controlling-the-robot/manual-control-by-terminal.md)).
Try it: start your node, press A, and keep LB on the gamepad pressed at the same time.
{% endhint %}

{% hint style="info" %}
On the real robot (ROS 2 Humble) `/cmd_vel` is a `Twist`. In the simulation
(ROS 2 Jazzy) it is a `TwistStamped` - code from the simulation needs a small change.
{% endhint %}

### Node lifecycle / program entry point

```python
def main(args=None):
    rclpy.init(args=args)
    node = MoveOnJoyButton()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

* `rclpy.init()` initializes the ROS 2 client library.
* `node = MoveOnJoyButton()` creates your node instance.
* `rclpy.spin(node)` starts the ROS 2 event loop: it listens for messages and calls callbacks (like `joy_callback`). `spin` blocks until the node is shut down.
* On `KeyboardInterrupt` (Ctrl+C) the code continues to shutdown gracefully: `node.destroy_node()` and `rclpy.shutdown()`.

---

## 21. SLAM  `[gewijzigd]`

<sub>slam.md</sub>


Make a map of the classroom.

There are two ways. Do **way 1 first** - that's where you learn what happens.

## Way 1 - yourself, with ROS 2 commands

Make sure the bringup runs on the robot and the `turtlebot-vis` container on
your laptop is started (see [Turtlebot3 - startup](turtlebot3-startup.md)).

In the **robot** container (web terminal or SSH):

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

In a new WSL terminal, in the **turtlebot-vis** container on your laptop:

```sh
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

RViz2 opens with the map being built. Drive around (gamepad, status page or
`teleop_keyboard`) and try to map the whole room. Drive slowly and turn slowly:
Cartographer needs time to match the lidar scans.

When ready, save the map. Make the directory first:

```sh
mkdir -p /root/ros2_ws/maps
ros2 run nav2_map_server map_saver_cli -f /root/ros2_ws/maps/classroom --free 0.196 --occ 0.65
```

{% hint style="warning" %}
* Don't stop the mapping (Cartographer) before the map is saved.
* `--free 0.196`: otherwise grey (unknown) cells are loaded as free later on,
  and Nav2 plans paths through unexplored space.
{% endhint %}

You get two files: `classroom.pgm` (the image) and `classroom.yaml` (resolution,
origin, thresholds). Open the `.pgm` in VS Code or Windows to look at it.

{% hint style="info" %}
Here Cartographer runs on your laptop and receives all lidar data over the wifi.
That works, but it is heavy for the wifi and your laptop.
{% endhint %}

## Way 2 - with the status page

Status page > **Rijden** > **Kaart maken**: the bringup and Cartographer start
**on the robot**. You see the map grow live with the robot and the lidar points.
Give the map a name and click the save button (disk icon).

The map is stored **on the robot** and can be chosen directly on the
**Navigatie** tab.

Show the map to the lecturer.

---

## 22. Autonomous driving  `[gewijzigd]`

<sub>autonomous-driving.md</sub>


{% hint style="danger" %}
Stop the SLAM of the previous step first (`CTRL + C`, or the stop button of
**kaart maken** under **Actief** on the status page). SLAM and navigation
cannot run at the same time.
{% endhint %}

Again two ways - do way 1 first.

## Way 1 - Nav2 yourself (on your laptop)

In the **turtlebot-vis** container, start Nav2 with **your** map:

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=/root/ros2_ws/maps/classroom.yaml
```

{% hint style="danger" %}
On a real robot **never** add `use_sim_time:=True`. That is only for the
simulation (Gazebo publishes a simulated clock). On the real robot Nav2 would
wait forever for a clock that never comes.
{% endhint %}

## Way 2 - Nav2 on the robot (status page)

Status page > **Navigatie**: choose your map, click **Start**. Nav2 runs on the
robot, you see the map, the robot, the planned path and the camera.

## Set the initial position of the TurtleBot3

The robot doesn't know where it is on the map yet.

* RViz2: set the fixed frame to `map`, then use the **2D Pose Estimate** button:
  click where the robot is and drag in the direction it looks.
* Status page: **Navigatie**, tool **Beginpositie** (crosshair icon), same idea.

{% hint style="info" %}
Check: do the lidar points (red) lie on the walls of the map? Then the position
is correct. Otherwise set it again. The first time loading RViz2 the map may
not be visible - wait a few seconds.
{% endhint %}

## Navigate

* RViz2: **Nav2 Goal** button - click the goal, drag for the final direction.
* Status page: tool **Doel** (flag icon).

The TurtleBot3 should start navigating to the desired point.

Demonstrate to the lecturer.

Try to put an obstacle in front of the TurtleBot3 while it is navigating: does
it plan a new path?

{% hint style="info" %}
Something goes wrong while navigating? Correct with the arrows on the status
page (**Navigatie**, gamepad icon on the right) or the gamepad: as long as you press,
you are in control; release and Nav2 continues.
{% endhint %}

---

## 23. Autonomous driving with python library  `[gewijzigd]`

<sub>autonomous-driving-with-python-library.md</sub>


Make a nav2\_simple.py script via VScode > WSL > docker container (Remote Explorer)

The script utilises the [nav2\_simple\_commander](https://docs.nav2.org/commander_api/index.html) library.

{% hint style="info" %}
The positions in the list will have to be adjusted according to the own map.

Use rviz and publish point to see the location.

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2F9gvtB2821YqYVnyn8SDn%2Fimage.png?alt=media\&token=3e20cf0a-68f2-4366-b4fc-b5dde0e7b2cd)
{% endhint %}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nav2 Simple Commander 
"""

from copy import deepcopy

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def main():
    rclpy.init()

    # Maak de Navigator 
    navigator = BasicNavigator()

    # Route: (x, y, yaw)
    inspection_route = [
        [2.0, -0.55, 1.57],
        [0.0, -0.55, 1.57],
        [1.5, -0.55, -1.57],
    ]

    navigator.waitUntilNav2Active()

    # Door elk waypoint lopen
    for idx, pt in enumerate(inspection_route):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pt[0]
        pose.pose.position.y = pt[1]
        pose.pose.orientation.z = 0.707 if pt[2] > 0 else -0.707
        pose.pose.orientation.w = 0.707

        print(f"\n➡️  Ga naar punt {idx + 1}: (x={pt[0]}, y={pt[1]}, yaw={pt[2]})")
        navigator.goToPose(pose)

        # Wachten tot doel bereikt
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print(f"  afstand over: {feedback.distance_remaining:.2f} m", end="\r")
           
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"\n✅ Punt {idx + 1} bereikt. Batterijmeting uitvoeren...")
        elif result == TaskResult.CANCELED:
            print(f"⚠️ Navigatie naar punt {idx + 1} geannuleerd.")
        elif result == TaskResult.FAILED:
            print(f"❌ Navigatie naar punt {idx + 1} mislukt.")

    print("\n✅ Alle waypoints voltooid.")

    #navigator.lifecycleShutdown()
  
    rclpy.shutdown()

if __name__ == "__main__":
    main()

```

Place an obstacle in front of the turtlebot3 and check if the path planning is rerouted.

Demonstrate to the lecturer.

{% hint style="info" %}
Nav2 can run on your laptop (Autonomous driving, way 1) or on the robot (status
page > Navigatie): this script works with both. The robot must have a correct
initial position first.
{% endhint %}

**Change max speed.**

Don't edit the installed files (`/opt/ros/...`): they are overwritten at every
update, and the robot runs ROS 2 **Humble** (not Jazzy). Make your **own copy**
of the parameters in your workspace, in the `turtlebot-vis` container:

```sh
cp $(ros2 pkg prefix turtlebot3_navigation2)/share/turtlebot3_navigation2/param/burger.yaml /root/ros2_ws/burger_slow.yaml
nano /root/ros2_ws/burger_slow.yaml
```

Go to the `FollowPath` section of the `controller_server`:

```yaml
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      min_vel_x: 0.0
      max_vel_x: 0.22
      max_vel_theta: 1.0
      max_speed_xy: 0.22
```

Change `max_vel_x`, `max_vel_theta` and `max_speed_xy` (the TurtleBot3 burger
can do at most 0.22 m/s and 2.84 rad/s) and start Nav2 with your file:

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py map:=/root/ros2_ws/maps/classroom.yaml params_file:=/root/ros2_ws/burger_slow.yaml
```

{% hint style="warning" %}
Nav2 on the status page must be stopped for this (only one Nav2 at a time).
{% endhint %}

---

## 24. Compare planners and controllers  `[nieuw]`

<sub>compare-planners-and-controllers.md</sub>


**New exercise.** Nav2 has two "brains":

* the **planner** (global): calculates a path over the whole map, from the
  robot to the goal;
* the **controller** (local): follows that path, a few times per second, and
  avoids obstacles that are not on the map.

On the status page > **Navigatie** > **Algoritmes** you can choose both; the
choice counts for the next goal or route.

| Planner | Idea |
|---|---|
| NavFn (Dijkstra) | standard of TurtleBot3; shortest path over the grid |
| NavFn (A\*) | same paths, calculated faster (heuristic towards the goal) |
| Smac 2D | A\* on the grid, smoother paths |
| Theta\* | straight lines between corners ("any-angle") |

| Controller | Idea |
|---|---|
| DWB | tries many speeds and picks the best (standard) |
| Regulated Pure Pursuit | follows a point some distance ahead on the path, calm |
| MPPI | simulates ~1000 possible trajectories per step and picks the best; smooth but heavy for the Pi |

## Exercise

1. Start Navigatie with your map and set the initial position.
2. Choose 2 points far apart, with a corner or an obstacle in between.
3. Drive from A to B with every **planner** (controller: DWB). Note for each:
   the shape of the path (screenshot), the time, does it reach the goal?
4. Same route with every **controller** (planner: NavFn). Note: the time, how
   smooth it drives, how close it passes obstacles, does it wiggle at the goal?
5. Put a box on the path while driving. Which controller reacts best?
6. Look at **Info** > logs and the CPU load in the header: which combination is
   heavy for the Raspberry Pi?

Explain your results to the lecturer: which combination would you choose for a
narrow classroom, and which for a large hall?

{% hint style="info" %}
**Nauwkeurigheid** (accuracy) decides when the robot is "there". More accurate
than the localisation (5-10 cm) makes no sense: then the robot keeps wiggling
at the goal.
{% endhint %}

---

## 25. Zones  `[nieuw]`

<sub>zones.md</sub>


**New exercise.** Not everything the robot should avoid is visible for the lidar:
a staircase, a cable on the floor, a glass wall, an area where people work.
Nav2 solves this with **costmap filters**: extra layers on top of the map.

Status page > **Navigatie** > tool **Zones** (dashed square icon):

| Zone | Effect |
|---|---|
| verboden zone (no-go) | the robot never enters it (planner and controller) |
| virtuele muur (virtual wall) | a line the robot doesn't cross |
| voorkeurszone (preferred lane) | the planner prefers paths through it; outside is allowed but costs more |
| snelheidszone (speed zone) | maximum speed in that zone, in % of the normal top speed |

Click the corner points on the map, finish the shape (double click or the check
button), then **save & apply**. The zones are stored with the map.

## Exercise

1. Start Navigatie and set the initial position.
2. Draw a **no-go zone** in the middle of an open area. Send a goal behind it:
   which path does the robot take now?
3. Draw a **virtual wall** across a passage. Can the robot still reach the
   other side?
4. Make a **speed zone** of 30 % near the door. Drive through it and watch the
   speed (Info > logs, or `ros2 topic echo /cmd_vel` in turtlebot-vis).
5. Turn on the **global costmap** layer (icon on the right of the map): how do
   your zones appear in it?

{% hint style="info" %}
Behind the scenes the status page publishes a mask (an image like the map) and
Nav2 uses it in the `KeepoutFilter` and `SpeedFilter`. Find these filters in the
Nav2 documentation: https://docs.nav2.org
{% endhint %}

Show your zones and the result to the lecturer.

---

## 26. Simulation of sensors  `[gewijzigd]`

<sub>simulation-of-sensors.md</sub>


Make a script `simulation_sensors.py` and add the code below. This code will simulate the following parameters. These parameters will be published on ROS 2 topics under `/sim/...`:

* battery state
* battery percentage
* temperature
* humidty
* gas sensor

{% hint style="danger" %}
The topics start with `/sim/`. The real robot already publishes `/battery_state`:
a second publisher on the same topic would mix fake and real values (battery
icon, labo-check and *Measure while driving* would show nonsense).
{% endhint %}

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import random
import time

from sensor_msgs.msg import BatteryState, Temperature, RelativeHumidity, JointState
from std_msgs.msg import Float32


class RandomSensorNode(Node):
    def __init__(self):
        super().__init__("random_sensor_node")
        self.get_logger().info('Random sensors node started!')

        # Publishers
        self.pub_battery = self.create_publisher(BatteryState, "/sim/battery_state", 10)
        self.pub_temp = self.create_publisher(Temperature, "/sim/temperature", 10)
        self.pub_humidity = self.create_publisher(RelativeHumidity, "/sim/humidity", 10)
        self.pub_gas = self.create_publisher(Float32, "/sim/gas_value", 10)

        # Timer (10 Hz)
        self.timer = self.create_timer(0.1, self.publish_random_values)

    def publish_random_values(self):
        now = self.get_clock().now().to_msg()

        # --- Battery (sensor_msgs/BatteryState) ---
        batt = BatteryState()
        batt.header.stamp = now
        batt.voltage = random.uniform(10.5, 12.6)
        batt.percentage = random.uniform(0.0, 1.0)  # 0–1 (niet 0–100)
        self.pub_battery.publish(batt)

        # --- Temperature ---
        temp = Temperature()
        temp.header.stamp = now
        temp.temperature = random.uniform(18.0, 35.0)
        temp.variance = 0.1
        self.pub_temp.publish(temp)

        # --- Humidity (sensor_msgs/RelativeHumidity) ---
        hum = RelativeHumidity()
        hum.header.stamp = now
        hum.relative_humidity = random.uniform(0.20, 0.80)  # 0–1
        hum.variance = 0.02
        self.pub_humidity.publish(hum)

        # --- Gaswaarde ---
        gas = Float32()
        gas.data = random.uniform(0.0, 1024.0)
        self.pub_gas.publish(gas)

        self.get_logger().info(f'Bat Volt: {batt.voltage:.2f} | Bat perctage: {batt.percentage:.2f}  | Temp: {temp.temperature:.2f}  |  Hum: {hum.relative_humidity:.2f}  |  Gas: { gas.data:.2f} ')

def main(args=None):
    rclpy.init(args=args)
    node = RandomSensorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

```

Start the Python script with the following command:

```shellscript
python3 simulation_sensors.py
```

Use the ros2 command to echo the published topics, e.g. `ros2 topic echo /sim/battery_state`.

---

## 27. Measure while driving  `[ongewijzigd]`

<sub>measure-while-driving.md</sub>


Make a nav2\_simple\_battery.py script via VScode > WSL > docker container (Remote Explorer)

At every waypoint the battery voltage should be measured. And printed to the terminal. Try to code below. But add the asked functionalities.

Make your own class (`BatteryInspector`) that subscribes to the topic `/battery_state`

Make an object of your class  and call it  `inspector_node`

Make sure the battery voltage is stored in the class attribute `battery_voltage`

{% hint style="info" %}
There is already some code added to integrate the class correctly. See lines with `## ADDED`
{% endhint %}

<pre class="language-python"><code class="lang-python">#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nav2 Simple Commander – TurtleBot3 batterijmeting per waypoint

Elke keer dat de robot een waypoint bereikt:
 - wordt de batterijspanning gemeten via /battery_state
"""

from copy import deepcopy
import csv
from datetime import datetime

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from sensor_msgs.msg import BatteryState

# ADD CLASS HERE

<strong>
</strong>



def main():
    rclpy.init()

    # Maak de Navigator en de batterij-subscriptie
    navigator = BasicNavigator()
    inspector_node = BatteryInspector()    # ADDED

    # Route: (x, y, yaw)
    inspection_route = [
        [2.0, -0.55, 1.57],
        [0.0, -0.55, 1.57],
        [1.5, -0.55, -1.57],
    ]

    navigator.waitUntilNav2Active()

    # Door elk waypoint lopen
    for idx, pt in enumerate(inspection_route):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pt[0]
        pose.pose.position.y = pt[1]
        pose.pose.orientation.z = 0.707 if pt[2] > 0 else -0.707
        pose.pose.orientation.w = 0.707

        print(f"\n➡️  Ga naar punt {idx + 1}: (x={pt[0]}, y={pt[1]}, yaw={pt[2]})")
        navigator.goToPose(pose)

        # Wachten tot doel bereikt
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print(f"  afstand over: {feedback.distance_remaining:.2f} m", end="\r")
            rclpy.spin_once(inspector_node, timeout_sec=0.1)    # ADDED

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"\n✅ Punt {idx + 1} bereikt. Batterijmeting uitvoeren...")

            # Wacht even om een verse batterijwaarde te krijgen
            rclpy.spin_once(inspector_node, timeout_sec=0.5)    # ADDED
            voltage = inspector_node.battery_voltage            # ADDED

            if voltage is None:                                 # ADDED
                print("⚠️ Geen batterijdata ontvangen!")
                voltage = 0.0

    
            print(f"🔋 Batterijspanning: {voltage:.2f} V")      # ADDED

        elif result == TaskResult.CANCELED:
            print(f"⚠️ Navigatie naar punt {idx + 1} geannuleerd.")
        elif result == TaskResult.FAILED:
            print(f"❌ Navigatie naar punt {idx + 1} mislukt.")

    print("\n✅ Alle waypoints voltooid.")

    #navigator.lifecycleShutdown()
    inspector_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

</code></pre>

---

## 28. Install python libraries in container  `[gewijzigd]`

<sub>install-python-libraries-in-container.md</sub>


Needed to install libraries (Matplotlib, reportlab, ...).

Go inside the `turtlebot-vis` container (ROS 2 Humble, Ubuntu 22.04, Python 3.10):

```sh
docker exec -it turtlebot-vis bash
apt update
apt install -y python3-venv
```

Make a virtual environment **in your workspace** (so it survives a restart of
the container) **with** the system packages (otherwise `rclpy` and the ROS
message types are not found):

```sh
python3 -m venv --system-site-packages /root/ros2_ws/.venv
```

Activate the venv:

```sh
source /root/ros2_ws/.venv/bin/activate
```

Install the specific libraries with:

```sh
python -m pip install matplotlib reportlab PyYAML pandas seaborn
```

{% hint style="info" %}
`apt install` is lost when the container is recreated (e.g. after
`docker compose pull`); the venv in `/root/ros2_ws` stays. After a recreate,
only `apt install -y python3-venv` is needed again before using pip.
{% endhint %}

{% hint style="warning" %}
The robot wifi may have no internet: install libraries at home or when the
access point has internet.
{% endhint %}

---

## 29. Solution: Measure while driving  `[ongewijzigd]`

<sub>solution-measure-while-driving.md</sub>


Make a nav2\_simple\_battery.py script via VScode > WSL > docker container (Remote Explorer)

At every waypoint, the battery voltage is measured. And printed to the terminal. Try to code below.

Make your own class (`BatteryInspector`) that subscribes to the topic `/battery_state`

Make an object of your class  and call it  `inspector_node`

Make sure the battery voltage is stored in the class attribute `battery_voltage`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Nav2 Simple Commander – TurtleBot3 batterijmeting per waypoint

Elke keer dat de robot een waypoint bereikt:
 - wordt de batterijspanning gemeten via /battery_state
"""

from copy import deepcopy
import csv
from datetime import datetime

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from sensor_msgs.msg import BatteryState


class BatteryInspector(Node):
    """Kleine helpernode om batterijmetingen op te slaan"""

    def __init__(self):
        super().__init__('battery_inspector')
        self.battery_voltage = None
        self.subscription = self.create_subscription(
            BatteryState,
            '/battery_state',
            self.battery_callback,
            10
        )

    def battery_callback(self, msg: BatteryState):
        """Callback die de laatste batterijspanning bewaart"""
        self.battery_voltage = msg.voltage

def main():
    rclpy.init()

    # Maak de Navigator en de batterij-subscriptie
    navigator = BasicNavigator()
    inspector_node = BatteryInspector()    # ADDED

    # Route: (x, y, yaw)
    inspection_route = [
        [2.0, -0.55, 1.57],
        [0.0, -0.55, 1.57],
        [1.5, -0.55, -1.57],
    ]

    navigator.waitUntilNav2Active()

    # Door elk waypoint lopen
    for idx, pt in enumerate(inspection_route):
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pt[0]
        pose.pose.position.y = pt[1]
        pose.pose.orientation.z = 0.707 if pt[2] > 0 else -0.707
        pose.pose.orientation.w = 0.707

        print(f"\n➡️  Ga naar punt {idx + 1}: (x={pt[0]}, y={pt[1]}, yaw={pt[2]})")
        navigator.goToPose(pose)

        # Wachten tot doel bereikt
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print(f"  afstand over: {feedback.distance_remaining:.2f} m", end="\r")
            rclpy.spin_once(inspector_node, timeout_sec=0.1)    # ADDED

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f"\n✅ Punt {idx + 1} bereikt. Batterijmeting uitvoeren...")

            # Wacht even om een verse batterijwaarde te krijgen
            rclpy.spin_once(inspector_node, timeout_sec=0.5)    # ADDED
            voltage = inspector_node.battery_voltage            # ADDED

            if voltage is None:                                 # ADDED
                print("⚠️ Geen batterijdata ontvangen!")
                voltage = 0.0

    
            print(f"🔋 Batterijspanning: {voltage:.2f} V")      # ADDED

        elif result == TaskResult.CANCELED:
            print(f"⚠️ Navigatie naar punt {idx + 1} geannuleerd.")
        elif result == TaskResult.FAILED:
            print(f"❌ Navigatie naar punt {idx + 1} mislukt.")

    print("\n✅ Alle waypoints voltooid.")

    #navigator.lifecycleShutdown()
    inspector_node.destroy_node()
    rclpy.shutdown()

```

---

## 30. Play a sound  `[ongewijzigd]`

<sub>play-a-sound.md</sub>


## Play a sound by terminal

The turtlebot can play a sound when sending a specific ros2 service.

```
ros2 service call /sound turtlebot3_msgs/srv/Sound value:\ 2
```

{% hint style="info" %}
Only value 0,1, 2 and 3 are implemented.
{% endhint %}

## Play a sound with rqt

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FcP4tbpiXSomyXAWwtjVJ%2Fimage.png?alt=media&amp;token=30733453-b8af-45da-8b5a-917d9f71af3c" alt=""><figcaption></figcaption></figure>

Play a sound with ros2 node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlebot3_msgs.srv import Sound  # Service type for TB3 sound
import sys
class SoundClientNode(Node):
    def __init__(self):
        super().__init__('turtlebot3_sound_client')
        # create the client
        self.cli = self.create_client(Sound, '/sound')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('/sound service not available, waiting...')
        self.req = Sound.Request()

    def play_sound(self, sound: int):
        self.req.value = sound
        self.get_logger().info(f'Calling /sound with value={sound}')
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future, timeout_sec=5.0)

        if self.future.done() and not self.future.cancelled():
            resp = self.future.result()
            if resp is not None:
                self.get_logger().info(f'Sound service call succeeded: {resp}')
            else:
                self.get_logger().error('Service call returned None')
        else:
            self.get_logger().error('Service call failed or timed out')

def main(args=None):
    rclpy.init(args=args)
    node = SoundClientNode()
    # Example: play sound #1 (turtlebot3 built-in sound). You can change number.
    node.play_sound(sound=int(sys.argv[1]))
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```

Try to start the command.

---

## 31. Location files on wsl  `[gewijzigd]`

<sub>location-files-on-wsl.md</sub>


{% hint style="warning" %}
Store all files in the `/root/ros2_ws` directory, otherwise you can lose them
when the container is recreated.
{% endhint %}

`/root/ros2_ws` in the `turtlebot-vis` container is the folder `ros2_ws` inside
the cloned `turtlebot_vis` repository on WSL.

In Windows Explorer: **Linux** > your distro (e.g. `Ubuntu-22.04`) > `home` >
your user name > `turtlebot_vis` > `ros2_ws`.

Or type in the address bar of Windows Explorer:

```
\\wsl$\Ubuntu-22.04\home\<user>\turtlebot_vis\ros2_ws
```

{% hint style="info" %}
On the robot there is a `/root/ros2_ws` as well (in the robot container). It is
stored on the robot itself (`~/turtlebot_setup/ros2_ws`) and survives robot
updates - but it is shared by everyone who uses that robot.
{% endhint %}

