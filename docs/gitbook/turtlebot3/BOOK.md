# Turtlebot3

_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/turtlebot3/`._

---

## 1. Installation  `[nieuw]`

<sub>installation.md</sub>


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

---

## 2. Turtlebot3 in the real world  `[gewijzigd]`

<sub>turtlebot3-in-the-real-world.md</sub>


In the simulation you drove a virtual TurtleBot3 in Gazebo. Now you work with the **real robot**. The ROS 2 topics are the same (`/scan`, `/odom`, `/imu`, `/cmd_vel`, ...), so most of what you learned still works - but the real world has a battery, a wifi connection, wheel slip and sensor noise.

How the lab is set up:

* Every TurtleBot has its **own wifi network** `TB-AP-<nr>`.
* The robot software runs in a **Docker container** on the Raspberry Pi of the robot (`turtlebot_<nr>`). It starts by itself when the robot boots.
* On your laptop you use the **`turtlebot-vis`** container (RViz2, teleop and your own nodes). It talks to the robot with ROS 2 over **Zenoh**.

## Objectives

In this session, the objectives are the following:

* Start up the real TurtleBot3 and connect to it (own wifi, SSH, robot container)
* Start the robot software (bringup) and connect your laptop over Zenoh
* Visualise the real robot in RViz2: robot model, TF, odometry and laser scan
* Drive the robot in a real environment with the keyboard and the gamepad
* Find and read the topics of the robot (battery, encoders, lidar, odometry)
* Make your own ROS 2 nodes on the real robot (subscribe and publish)

{% hint style="info" %}
Next session: map an environment with Cartographer (SLAM) and navigate
autonomously in the mapped environment.
{% endhint %}

{% hint style="warning" %}
**Before the lab, with internet** (eduroam, at home): do the
[Installation](installation.md) of the laptop container. It is about 4 GB, and
the robot wifi has no (or only slow) internet.
{% endhint %}

{% hint style="info" %}
New to the topics, TF, odometry or QoS? Read the [Theory: what the robot measures](theory/) first.
{% endhint %}

---

## 3. Turtlebot3 - startup  `[gewijzigd]`

<sub>turtlebot3-startup/README.md</sub>


First make sure the [Installation](../installation.md) is done (with internet). Then follow these steps in this order:

1. [Connect to the WIFI](connect-to-the-wifi.md) - your laptop on `TB-AP-<nr>`
2. [Startup of the turtlebot3](startup-of-the-turtlebot3.md) - battery on, wait for the beep
3. [Connect to the turtlebot3](connect-to-the-turtlebot3.md) - a terminal inside the robot container
4. [Startup docker](startup-docker.md) - check that the robot container runs (nothing to start)
5. [Startup turtlebot software](startup-turtlebot-software.md) - start the bringup
6. [Setup laptop (student)](setup-laptop-student.md) - the `turtlebot-vis` container on your laptop

{% hint style="info" %}
Replace `<nr>` everywhere by the number of **your** robot, without a leading zero: robot 5 -> `TB-AP-05`, `10.0.5.10`, `turtlebot_5`, `ROS_DOMAIN_ID=5`.
{% endhint %}

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

* Via DC adapter (on the table, for programming)
* Via battery (for driving)

Connect the battery to the TurtleBot and switch it on.

* The OpenCR board plays a short melody.
* After about 1 minute the Raspberry Pi is ready: the robot software starts
  **automatically** in a Docker container (`turtlebot_<nr>`) and you hear a
  second short melody. You don't have to start anything yourself yet.

{% hint style="info" %}
**The lidar does not turn yet?** That is normal. To spare the lidar, the USB
power of the robot is switched off when nothing uses it. It switches on by
itself when you start the bringup (see
[Startup turtlebot software](startup-turtlebot-software.md)).
{% endhint %}

{% hint style="danger" %}
**Battery**: below **11.0 V** the OpenCR switches the motors off and the robot
beeps. Below about 11.2 V: charge or swap the battery. You can read the voltage
with `ros2 topic echo /battery_state --field voltage` (after the bringup) or on
the status page.
{% endhint %}

Continue with [Connect to the turtlebot3](connect-to-the-turtlebot3.md).

---

### 6. Connect to the turtlebot3  `[gewijzigd]`

<sub>turtlebot3-startup/connect-to-the-turtlebot3.md</sub>


For the exercises you need a terminal **inside the robot container**. Two ways:

## Option 1 - SSH (recommended)

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

{% hint style="info" %}
`WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`? The robot was reinstalled
since your last visit. Remove the old key and try again:

```sh
ssh-keygen -R 10.0.<nr>.10
```
{% endhint %}

You are now on the Raspberry Pi of the robot. Go inside the robot container:

```sh
docker exec -it turtlebot_<nr> bash
```

{% hint style="warning" %}
`<nr>` is the robot number **without** a leading zero: robot 5 ->
`docker exec -it turtlebot_5 bash`. Press `TAB` to autocomplete.
{% endhint %}

You need a robot terminal more than once (bringup, gamepad, ...): open a new WSL
terminal and repeat both commands.

## Option 2 - web terminal

Open `http://10.0.<nr>.10:7681` in a browser (laptop on `TB-AP-<nr>`).
Login: see lab notes. You are directly inside the robot container.

## The status page (optional)

Every robot also serves a web page: `http://10.0.<nr>.10:8080`. It is handy
to check the **battery**, to see what is running, and for the **STOP** button,
which stops everything that drives. For the exercises you don't need it: you
work in the terminal.

---

### 7. Startup docker  `[gewijzigd]`

<sub>turtlebot3-startup/startup-docker.md</sub>


{% hint style="success" %}
Nothing to do here anymore: the Docker container on the robot (`turtlebot_<nr>`)
starts **automatically** when the robot boots, and restarts by itself if needed.
{% endhint %}

Check that it runs. Via SSH on the robot (not inside the container):

```sh
docker ps
```

You should see a container `turtlebot_<nr>` with status `Up`.

{% hint style="danger" %}
Don't run `docker compose pull`, `docker compose up/down` or `docker rm`
yourself on the robot. Updating the robot software is done by the lecturer.
{% endhint %}

---

### 8. Startup turtlebot software  `[gewijzigd]`

<sub>turtlebot3-startup/startup-turtlebot-software.md</sub>


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

{% hint style="warning" %}
First do the [Installation](../installation.md) (clone + `docker compose pull`),
**with internet**. On the robot wifi you can't download the 4 GB image.
{% endhint %}

Open a WSL terminal and go to the cloned repository:

```sh
cd turtlebot_vis
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

{% hint style="info" %}
Changed `.env` while the container was already running (other robot)? Run
`docker compose up` again: the container is recreated with the new values.
{% endhint %}

## Start the container

```sh
docker compose up
```

Open a new WSL terminal and connect to the container:

```sh
docker exec -it turtlebot-vis bash
```

Check that you see the topics of your robot (the bringup must be running, see
[Startup turtlebot software](startup-turtlebot-software.md)):

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

## 10. Visualise the robot  `[gewijzigd]`

<sub>visualise-the-robot.md</sub>


{% hint style="info" %}
Theory first? See [TF - coordinate frames](theory/tf.md), [Odometry](theory/odometry.md) and [Laser scan](theory/laser-scan.md).
{% endhint %}

Select as Fixed frame the odom frame.

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FIWLWvYorpN8ylreiH1lM%2Fimage.png?alt=media&amp;token=18f12e84-aa2a-4590-aec8-6bf47c307e74" alt=""><figcaption></figcaption></figure>

Try to show the RobotModel, odometry, TF and laserscan in RViz2

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2F6mYEBmeKnLrh8C6W5M8Y%2Fimage.png?alt=media&amp;token=f700b34e-308d-4445-b580-d844b375abd2" alt=""><figcaption></figcaption></figure>

{% hint style="warning" %}
To see the laserscan in RViz2, set the **reliability policy** to Best Effort: the lidar publishes Best Effort. With the standard DDS middleware the scan isn't shown otherwise; on our robot (Zenoh) it works anyway, but match it all the same. See [QoS](theory/qos.md).

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

<sub>controlling-the-robot/README.md</sub>


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

The bringup must be running on the robot (see
[Startup turtlebot software](../turtlebot3-startup/startup-turtlebot-software.md)).

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

{% hint style="info" %}
The switch on the back of the gamepad must be on **X** (XInput mode).
{% endhint %}

Start the gamepad driver **on the robot**: open a terminal inside the robot
container (see [Connect to the turtlebot3](../turtlebot3-startup/connect-to-the-turtlebot3.md))
and run:

```sh
ros2 launch teleop_twist_joy teleop-launch.py joy_vel:=cmd_vel_joy config_filepath:=/root/turtlebot3_ws/joystick_f710.yaml
```

Keep this terminal open (`CTRL + C` stops the gamepad). The bringup must be
running as well.

{% hint style="info" %}
* `joy_vel:=cmd_vel_joy`: the gamepad publishes on `/cmd_vel_joy`, the input
  with the highest priority in twist_mux.
* `joystick_f710.yaml`: which buttons and sticks do what, and the speeds.
* Alternative: status page > **Rijden** > gamepad button (top right).
{% endhint %}

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

## 14. See turtlebot3 topics  `[gewijzigd]`

<sub>see-turtlebot3-topics.md</sub>


{% hint style="info" %}
What do these topics mean? See [Theory: what the robot measures](theory/).
{% endhint %}

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

## 15. Play a sound  `[gewijzigd]`

<sub>play-a-sound.md</sub>


{% hint style="info" %}
The terminal and rqt parts work right away (the bringup must be running). For the last part, a ROS 2 node in Python, first read [ROS2 nodes](ros2-nodes/): where to write your code (`/root/ros2_ws`) and how to connect with VS Code.
{% endhint %}

## Play a sound by terminal

The turtlebot can play a sound when sending a specific ros2 service.

```
ros2 service call /sound turtlebot3_msgs/srv/Sound value:\ 2
```

{% hint style="info" %}
Only value 0,1, 2 and 3 are implemented.
{% endhint %}

## Play a sound with rqt

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FcP4tbpiXSomyXAWwtjVJ%2Fimage.png?alt=media&#x26;token=30733453-b8af-45da-8b5a-917d9f71af3c" alt=""><figcaption></figcaption></figure>

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

## 16. ROS2 nodes  `[gewijzigd]`

<sub>ros2-nodes/README.md</sub>


You write your ROS 2 nodes **on your laptop**, in your own `turtlebot-vis`
container. The node talks to the robot over Zenoh, exactly like RViz2 and
teleop. The bringup must be running on the robot.

## Open the container in VS Code

VS Code > **Remote Explorer** > **WSL** (Ubuntu-22.04) > **Dev Containers** >
`turtlebot-vis` > attach. When asked to open a folder, choose `/root/ros2_ws`.

{% hint style="info" %}
Same steps as in the simulation ([The first ros2 node](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node)),
but now the container is `turtlebot-vis`. VS Code may ask to install the Python
extension in the container: say yes.
{% endhint %}

## Make and run a script

1. Make the script in `/root/ros2_ws`, for example `sub_scan.py`.
2. Open a terminal in VS Code (**Terminal > New Terminal**): it runs inside the container.
3. Run it:

```sh
cd /root/ros2_ws
python3 sub_scan.py
```

`CTRL + C` stops the node.

{% hint style="warning" %}
Store your code in `/root/ros2_ws`: that is the folder `turtlebot_vis/ros2_ws`
on your laptop (see [Location files on WSL](../location-files-on-wsl.md)).
Anything you store elsewhere in the container can be lost.
{% endhint %}

<details>

<summary>Advanced: run a node on the robot itself</summary>

The robot container `turtlebot_<nr>` also has a `/root/ros2_ws`
(`~/turtlebot_setup/ros2_ws` on the robot). It is **shared by everyone who uses
that robot**, and VS Code over SSH needs internet on the robot to install its
server. Only use it when your lecturer asks for it.

</details>

---

### 17. Read in the scan topic  `[gewijzigd]`

<sub>ros2-nodes/read-in-the-scan-topic/README.md</sub>


{% hint style="info" %}
Theory: [Laser scan (/scan)](../../theory/laser-scan.md) - angles, indices, invalid values and QoS.
{% endhint %}

Make a Python script (`sub_scan.py`) that is subscribed to the `/scan` topic. Make the script inside the `turtlebot-vis` container in the directory `/root/ros2_ws`.

How to open the container in VS Code and run your script: see [ROS2 nodes](../).

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
Change the QoS (Quality of Service)

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

Add the `create_subscription` also to the `__init__` function.

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

Below you see the build up of the laserscan. You get roughly 220-230 points per rotation (LDS-02 lidar, \~5 rotations per second)

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2Fjl07REjZyMmR6JgmDR3O%2Ffile.excalidraw.svg?alt=media\&token=22bfd257-79c7-429b-afb2-85ec2fa16979)

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

#### 18. Exercise  `[gewijzigd]`

<sub>ros2-nodes/read-in-the-scan-topic/exercise.md</sub>


The exercise on the scan topic is part of the homework:
[Task 1 - Obstacle alarm](../../homework/task-1-obstacle-alarm.md) (with the
scan sectors as extension). Test your `sub_scan.py` first: hold your hand in
front of the lidar and check that the front distance changes.

---

### 19. Read the battery level  `[gewijzigd]`

<sub>ros2-nodes/read-the-battery-level.md</sub>


Make a new python script (`sub_battery_level.py`) in the `turtlebot-vis` container, in `/root/ros2_ws`.

Check the ros2 msg typ of the `/battery_state` topic. Add this as a python library.

Try to subscribe to the `/battery_state` topic.

Check what data is available in the ros2 topic `/battery_state`.

Print the voltage value and SoC (state of charge) of the battery to the terminal.

Print a warning when the SoC is below the 50%

{% hint style="info" %}
* Is `percentage` a value between 0 and 1, or between 0 and 100? Check it with
  `ros2 topic echo /battery_state --once`.
* The percentage of the OpenCR is optimistic: the motors already stop at
  **11.0 V**. Extra: also print a warning when the **voltage** is below 11.2 V.
{% endhint %}

Show when ready to the lecturer.

---

### 20. Read the encoder value  `[gewijzigd]`

<sub>ros2-nodes/read-the-encoder-value.md</sub>


{% hint style="info" %}
Theory: [Odometry (/odom) and encoders](../theory/odometry.md) - ticks, wheel radius and the formulas.
{% endhint %}

Make a new python script (`sub_encoders.py`) in the `turtlebot-vis` container, in `/root/ros2_ws`.

Check if there is a ros2 topic that contains the encoder values

Check the ros2 msg typ of the ros2 topic. Add this as a python library inside in the script.

Try to subscribe to the ros2 topic.

Print the encoder values to the terminal.

Try to calculate the average speed of the wheels.

Show when ready to the lecturer.

---

### 21. Drive 10cm with a button  `[gewijzigd]`

<sub>ros2-nodes/drive-10cm-with-a-button.md</sub>


{% hint style="info" %}
Theory: [Driving the robot (/cmd_vel)](../theory/cmd-vel.md) - Twist, units and twist_mux.
{% endhint %}

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

## 22. Homework  `[nieuw]`

<sub>homework/README.md</sub>


Finish these tasks **at home, before the next session**. You have no robot at
home, so you work in the **simulation**: the container `gazebo_turtlebot_cont`
from the simulation book (Gazebo + ROS 2 Jazzy).

{% hint style="warning" %}
* Store your scripts in `/home/dockeruser/dev_ws` (the `dev_ws` folder of the
  `ros2-jazzy-gazebo-turtlebot` repository), not in the `turtlebot-vis` container:
  without a robot, the `turtlebot-vis` container has no Zenoh router to talk to.
* Simulation vs. real robot: in the simulation `/cmd_vel` is a `TwistStamped`,
  the lidar has 360 points, and there is no `/battery_state`.
{% endhint %}

## Overview

1. [Startup at home](startup-at-home.md) - start the simulation and VS Code
2. [Task 1 - Obstacle alarm](task-1-obstacle-alarm.md) - warning when something is close in front (extension: four sectors)
3. [Task 2 - Battery warning](task-2-battery-warning.md) - with fake sensors (`/sim/battery_state`)
4. [Task 3 - Turn exactly 90°](task-3-turn-90-degrees.md) - yaw from `/odom` (extension: drive a square)
5. [Task 4 - Theory](task-4-theory.md) - the Check yourself questions

## Hand in

Upload on Toledo, before the next session:

* your Python scripts of task 1, 2 and 3;
* a screenshot of the terminal output of each script;
* your answers of task 4.

{% hint style="success" %}
Next session: SLAM (make a map) and autonomous navigation with the real robot.
{% endhint %}

---

### 23. Startup at home  `[nieuw]`

<sub>homework/startup-at-home.md</sub>


The same steps as in the simulation book
([Installation](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/installation), [Startup](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/turtlebot-in-simulation/startup),
[The first ros2 node](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node)):

1. Open a WSL terminal and start the simulation container:

   ```sh
   cd ros2-jazzy-gazebo-turtlebot
   docker compose up
   ```

2. Open a **second** WSL terminal, go inside the container and start Gazebo with the robot:

   ```sh
   docker exec -it gazebo_turtlebot_cont bash
   ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

3. Open **VS Code** > Remote Explorer > WSL > Dev Containers >
   `ros2-jazzy-gazebo-turtlebot` > attach, folder `/home/dockeruser/dev_ws`.
   Make your scripts there and run them in the VS Code terminal
   (`python3 <script>.py`).

4. **Only for task 2:** start the fake sensors, see
   [Simulation of sensors](task-2-battery-warning.md#simulation-of-sensors) in task 2.

5. Drive the robot (for task 1) in another terminal:

   ```sh
   ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
   ```

{% hint style="info" %}
Check: `ros2 topic list` in the container shows `/scan`, `/odom`, `/cmd_vel`,
... (and `/sim/battery_state` when step 4 runs).
{% endhint %}

---

### 24. Task 1 - Obstacle alarm  `[nieuw]`

<sub>homework/task-1-obstacle-alarm.md</sub>


Make `obstacle_alarm.py`, based on your `sub_scan.py` from the lab: when
something is **closer than 0.30 m in front of the robot**, print a warning.
Work in the simulation (`turtlebot3_world.launch.py`) and drive towards a wall or
a pillar with teleop.

1. Take the front part of the scan, as in [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic/): `ranges[:n] + ranges[-n:]`.
2. Use the **closest** distance (`min`) instead of the mean. Why is the mean not good for an alarm?
3. Ignore invalid values: keep only finite values **larger than 0.12 m** (the
   real lidar gives `0.0` when there is no echo, the simulation gives `inf`).
4. Closest distance below 0.30 m: log a warning with `self.get_logger().warn(...)`,
   but print **"obstacle!" only once** when the obstacle appears, and
   **"free again"** when it is gone.

Expected output, for example:

```
[WARN] [obstacle_alarm]: obstacle at 0.27 m!
[INFO] [obstacle_alarm]: free again
```

<details>

<summary>Hints</summary>

* A single chair leg in front of the robot hardly changes the **mean** of 30
  values; the **minimum** shows it immediately.
* "Only once": remember in `self.alarm` whether the obstacle was already there in
  the previous scan - the same idea as the rising edge of the A button in
  [Drive 10cm with a button](../ros2-nodes/drive-10cm-with-a-button.md).
* Sound (extra, real robot): make the service client in `__init__`
  (`self.create_client(Sound, '/sound')`) and use `call_async(...)` in the
  callback. Never wait for the answer inside a callback: that blocks your node.

</details>

{% hint style="info" %}
**Extra for the next lab (real robot):** let the robot play a sound when the
obstacle appears: service `/sound`, type `turtlebot3_msgs/srv/Sound`, value `3`
(see [Play a sound](../play-a-sound.md)). The simulation has no `/sound` service.
{% endhint %}

## Extension - scan sectors

Do the same for **four** directions: print the closest distance **in front**,
**left**, **behind** and **right** of the robot.

![](https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FODudHqthpJTbo5FEnO7l%2Ffile.excalidraw.svg?alt=media\&token=95719208-4142-42a1-8c38-e621c706bd27)

Expected output, for example:

```
front 0.84 m | left 0.35 m | behind 1.92 m | right inf m
```

<details>

<summary>Hints for the extension</summary>

* Index 0 is in front, the angle grows counterclockwise: a quarter of the
  array further is **left**, half way is **behind**, three quarters is **right**
  (see [Laser scan](../theory/laser-scan.md)).
* Don't use fixed numbers: calculate them, then the same script works in the
  simulation (360 points) and on the real robot (about 220-230 points):

  ```python
  n = len(msg.ranges)
  quarter = n // 4
  k = int(math.radians(15) / msg.angle_increment)   # +-15 degrees around each direction
  left = msg.ranges[quarter - k : quarter + k]
  ```

* **Front** is special: it is at the start **and** at the end of the array
  (`ranges[:k] + ranges[-k:]`).
* Filter invalid values (`inf`, `nan`, values below 0.12 m) before `min()`,
  and handle an empty list.

</details>

Extra: also print the **angle** (in degrees) of the closest obstacle of the whole scan.

---

### 25. Task 2 - Battery warning  `[nieuw]`

<sub>homework/task-2-battery-warning.md</sub>


At home there is no robot battery: first start fake sensors, then write your node.

## Simulation of sensors

At home there is no robot battery. The script `simulation_sensors.py` publishes
**random** values once per second, on topics that start with `/sim/`:

| topic | type |
|---|---|
| `/sim/battery_state` | `sensor_msgs/msg/BatteryState` (voltage 10.5-12.6 V, percentage 0-1) |
| `/sim/temperature` | `sensor_msgs/msg/Temperature` |
| `/sim/humidity` | `sensor_msgs/msg/RelativeHumidity` |
| `/sim/gas_value` | `std_msgs/msg/Float32` |

### Download

{% file src="../.gitbook/assets/simulation_sensors.py" %}
simulation_sensors.py
{% endfile %}

Put it in the `dev_ws` folder of the simulation repository:

| where | path |
|---|---|
| WSL | `~/ros2-jazzy-gazebo-turtlebot/dev_ws/simulation_sensors.py` |
| Windows Explorer | `\\wsl$\Ubuntu-22.04\home\<user>\ros2-jazzy-gazebo-turtlebot\dev_ws` |
| inside the container | `/home/dockeruser/dev_ws/simulation_sensors.py` |

Or download it directly to the right place, in a **WSL terminal** (not in the container):

```sh
wget -O ~/ros2-jazzy-gazebo-turtlebot/dev_ws/simulation_sensors.py https://raw.githubusercontent.com/JeremyLebon/turtlebot_setup/master/docs/gitbook/turtlebot3/.gitbook/assets/simulation_sensors.py
```

{% hint style="info" %}
Cloned the repository somewhere else than your home folder? Replace
`~/ros2-jazzy-gazebo-turtlebot` by that folder.
{% endhint %}

### Run

In a terminal **inside the container** (`docker exec -it gazebo_turtlebot_cont bash`):

```sh
cd /home/dockeruser/dev_ws
python3 simulation_sensors.py
```

Check in another terminal: `ros2 topic echo /sim/battery_state`.

<details>

<summary>The code of simulation_sensors.py</summary>

```python
#!/usr/bin/env python3
"""Fake robot sensors for at home (no robot): publishes random values once per
second on /sim/battery_state, /sim/temperature, /sim/humidity and /sim/gas_value.

Run it in the simulation container (gazebo_turtlebot_cont):
    python3 simulation_sensors.py
"""
import random

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState, Temperature, RelativeHumidity
from std_msgs.msg import Float32


class RandomSensorNode(Node):
    def __init__(self):
        super().__init__("random_sensor_node")

        # Topics start with /sim/: the real robot already publishes /battery_state
        self.pub_battery = self.create_publisher(BatteryState, "/sim/battery_state", 10)
        self.pub_temp = self.create_publisher(Temperature, "/sim/temperature", 10)
        self.pub_humidity = self.create_publisher(RelativeHumidity, "/sim/humidity", 10)
        self.pub_gas = self.create_publisher(Float32, "/sim/gas_value", 10)

        self.timer = self.create_timer(1.0, self.publish_random_values)  # 1 Hz
        self.get_logger().info("Random sensors node started: topics /sim/...")

    def publish_random_values(self):
        now = self.get_clock().now().to_msg()

        batt = BatteryState()
        batt.header.stamp = now
        batt.voltage = random.uniform(10.5, 12.6)      # V (3S LiPo)
        batt.percentage = random.uniform(0.0, 1.0)     # 0-1, not 0-100
        self.pub_battery.publish(batt)

        temp = Temperature()
        temp.header.stamp = now
        temp.temperature = random.uniform(18.0, 35.0)  # degrees C
        temp.variance = 0.1
        self.pub_temp.publish(temp)

        hum = RelativeHumidity()
        hum.header.stamp = now
        hum.relative_humidity = random.uniform(0.20, 0.80)  # 0-1
        hum.variance = 0.02
        self.pub_humidity.publish(hum)

        gas = Float32()
        gas.data = random.uniform(0.0, 1024.0)         # raw sensor value
        self.pub_gas.publish(gas)

        self.get_logger().info(
            f"battery {batt.voltage:.2f} V {batt.percentage * 100:.0f} % | "
            f"temp {temp.temperature:.1f} C | humidity {hum.relative_humidity * 100:.0f} % | "
            f"gas {gas.data:.0f}")


def main(args=None):
    rclpy.init(args=args)
    node = RandomSensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
```

</details>

{% hint style="danger" %}
Keep the `/sim/` prefix. The real robot already publishes `/battery_state`: a
second publisher on the same topic would mix fake and real values.
{% endhint %}

## Your node

With `simulation_sensors.py` running, write a node that subscribes to
`/sim/battery_state`, prints the voltage and the percentage, and prints a
**warning** when the voltage is below **11.2 V** or the percentage below **50 %**.

On the real robot you only change the topic to `/battery_state`.

---

### 26. Task 3 - Turn exactly 90°  `[nieuw]`

<sub>homework/task-3-turn-90-degrees.md</sub>


In the lab you drove **straight** (*Drive 10cm with a button*, on time). Now the
robot **turns**, and you use the **odometry** to know when to stop: turn exactly
**90° to the left** on the spot, then stop.

1. Subscribe to `/odom` and calculate the **yaw** (heading) from the quaternion
   in `pose.pose.orientation` (see [IMU - Quaternions](../theory/imu.md)).
2. Remember the yaw of the **first** message: that is your start.
3. Publish on `/cmd_vel` (simulation: `TwistStamped`) with only `angular.z`
   (positive = left, for example 0.3 rad/s).
4. Stop (publish all speeds 0) as soon as the robot turned 90° (π/2 rad).
5. Print the start yaw and how far the robot really turned, in degrees.

Check it in Gazebo: is the robot turned exactly a quarter turn?

<details>

<summary>Hints</summary>

* Yaw from a quaternion `q`:
  `math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))`.
* The yaw jumps from **+180° to -180°**. Starting at 170° and turning 90° left
  ends at -100°, so `yaw - start` gives -270°. Bring the difference back between
  -180° and +180°: `math.atan2(math.sin(d), math.cos(d))`.
* The robot overshoots when it turns fast until the very end: turn **slower**
  when you get close (for example speed proportional to the remaining angle,
  with a minimum).
* Stop your node when it is done, and always publish speed 0 at the end.

</details>

## Extension - drive a square

Combine driving and turning: drive a **square of 0.5 m × 0.5 m** and come back to
the start. Use `/odom` for both the distance (`math.hypot(x - x0, y - y0)`) and
the angle. How far from the start does the robot end? Why?

---

### 27. Task 4 - Theory  `[nieuw]`

<sub>homework/task-4-theory.md</sub>


Answer the **Check yourself** questions of the theory pages:
[Laser scan](../theory/laser-scan.md), [Odometry](../theory/odometry.md),
[IMU](../theory/imu.md), [TF](../theory/tf.md), [cmd_vel](../theory/cmd-vel.md) and
[QoS](../theory/qos.md).

---

## 28. Location files on wsl  `[gewijzigd]`

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

---

## 29. Theory: what the robot measures  `[nieuw]`

<sub>theory/README.md</sub>


Reference chapter: **where the data comes from** and **what it means**, for each important topic, applied to our TurtleBot3 Burger. You saw most of it in the simulation; here are the values of the real robot. The exercises link to the page you need.

* [Laser scan (`/scan`)](laser-scan.md) - what the lidar sees
* [Odometry (`/odom`) and encoders](odometry.md) - where the robot thinks it is
* [IMU (`/imu`)](imu.md) - rotation and acceleration
* [TF - coordinate frames](tf.md) - how everything fits together
* [Driving the robot (`/cmd_vel`)](cmd-vel.md) - speed commands and twist\_mux
* [QoS - Quality of Service](qos.md) - why you sometimes receive nothing

## Where does the data come from?

```
                 TurtleBot3 Burger (robot)                         Laptop (student)
 ┌─────────────────────────────────────────────────────┐
 │  LDS-02 lidar ──USB──┐                              │
 │                      │   Raspberry Pi 5             │
 │                      ▼   (container turtlebot_<nr>) │
 │                 ld08_driver ──────────► /scan       │
 │                                                     │     Zenoh      ┌──────────────┐
 │  OpenCR board ──USB──► turtlebot3_node ─► /odom     │ ◄────wifi────► │ turtlebot-vis│
 │   • 2 motors with       (ROS 2 driver)  ─► /imu     │   TB-AP-<nr>   │  RViz2, rqt, │
 │     encoders                            ─► /tf      │                │  your nodes  │
 │   • IMU chip                            ─► /joint_states            └──────────────┘
 │   • battery, buttons                    ─► /sensor_state, /battery_state
 │                                                     │
 │                 /cmd_vel ──► twist_mux ──► turtlebot3_node ──► motors
 └─────────────────────────────────────────────────────┘
```

* The **OpenCR** board is a microcontroller board. It reads the motor encoders, the IMU, the battery and the buttons and drives the two motors.
* `turtlebot3_node` on the Raspberry Pi talks to the OpenCR over USB and turns everything into ROS 2 topics. It also **calculates the odometry** and publishes the transform `odom -> base_footprint`.
* The **LDS-02** lidar has its own driver (`ld08_driver`) that publishes `/scan`.

## Conventions used by all ROS robots

ROS uses fixed conventions (REP-103), so every robot and every tool agrees:

| Quantity      | Unit                                     |                                      |
| ------------- | ---------------------------------------- | ------------------------------------ |
| distance      | metre (m)                                | not cm or mm!                        |
| angle         | radian (rad)                             | 1 rad ≈ 57.3°, 90° = π/2 ≈ 1.571 rad |
| linear speed  | m/s                                      |                                      |
| angular speed | rad/s                                    |                                      |
| time          | seconds (ROS time stamp in the `header`) |                                      |

Axes of the robot (right-hand rule):

```
            x (forward)
            ▲
            │
   y ◄──────●        z points up, out of the screen
  (left)   robot
```

* **x** = forward, **y** = left, **z** = up.
* A **positive rotation** around z is **counterclockwise** (to the left). So `angular.z = +0.5` in `/cmd_vel` turns the robot to the left.

{% hint style="info" %}
Try it: `ros2 topic list` and `ros2 topic info /odom` (in the `turtlebot-vis` container). Which node publishes `/odom`? Which nodes publish `/scan` and `/imu`?
{% endhint %}

---

### 30. Laser scan (/scan)  `[nieuw]`

<sub>theory/laser-scan.md</sub>


## How a lidar works

On top of the TurtleBot is a **LDS-02** lidar (Laser Distance Sensor). Inside, a laser and a receiver turn around (about 5 rotations per second). For every small angle step the sensor measures the distance to the first object the laser hits. The result of one rotation is a **2D slice** of the world at the height of the lidar (about 18 cm above the floor).

```
                    0 rad (front, x)
                         ▲
                 ·  ·  · │ ·  ·  ·
             ·           │           ·
   +π/2   ·              │              ·    -π/2
  (left) ·───────────────●───────────────·  (right)
          ·            robot            ·
             ·                       ·
                 ·  ·  ·   ·  ·  ·
                       ±π (back)
```

{% hint style="warning" %}
The lidar only sees what is **at its own height**. A low object (a cable, a foot of a chair) or a table top above the robot is invisible to it. Glass and black, shiny surfaces can also give no (or a wrong) reflection.
{% endhint %}

## LDS-02 on our robot

|                      | LDS-02                                            |
| -------------------- | ------------------------------------------------- |
| rotations per second | \~5 Hz → `/scan` arrives about 5 times per second |
| points per rotation  | \~220-230 (not always exactly the same!)          |
| angular resolution   | \~1.6° per point                                  |
| range                | \~0.16 m to 8 m                                   |
| frame                | `base_scan` (see [TF](tf.md))                     |

## The LaserScan message

`/scan` is of type `sensor_msgs/msg/LaserScan`:

| field                    | meaning                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| `header.stamp`           | time of the measurement                                              |
| `header.frame_id`        | `base_scan`: the distances are measured from the centre of the lidar |
| `angle_min`, `angle_max` | angle of the first and the last point (rad)                          |
| `angle_increment`        | angle between two points (rad)                                       |
| `range_min`, `range_max` | limits of the sensor (m)                                             |
| `ranges[]`               | the distances (m), one per angle step                                |
| `intensities[]`          | strength of the reflection (here: the confidence of the point)       |

The **index** `i` in `ranges[]` belongs to the angle:

```
angle(i) = angle_min + i * angle_increment
```

and the other way around, the index for a given angle:

```
i = round((angle - angle_min) / angle_increment)
```

Index `0` is the **front** of the robot, the angle grows **counterclockwise**: a quarter of the array further is the **left** side, half way is the **back**, three quarters is the **right**.

{% hint style="info" %}
Because the number of points is not always the same (220, 221, ...), never use fixed indices like `ranges[55]` for "left". Calculate the index from `angle_increment`, or use `len(msg.ranges) // 4`.
{% endhint %}

## Invalid values

Not every angle gives a good measurement. In `ranges[]` you can find:

* `nan` - no measurement for that angle
* `inf` - nothing within range
* `0.0` or a value smaller than \~0.12 m - no valid echo

Always filter these before you calculate a mean or a minimum, for example:

```python
valid = [r for r in msg.ranges if math.isfinite(r) and r > 0.12]
```

## From distance and angle to a point (x, y)

A lidar point is given in **polar coordinates** (distance `r`, angle `θ`). To get the point in the frame of the lidar (`base_scan`):

```
x = r * cos(θ)        (forward)
y = r * sin(θ)        (left)
```

This is exactly what RViz2 does to draw the red dots. To place the points on the map, RViz2 also needs the position of the lidar on the robot and the position of the robot in the world: that is [TF](tf.md).

## QoS: Best Effort

The lidar publishes with **Best Effort** reliability: if a message is lost on the wifi, it is not sent again (the next scan arrives 0.2 s later anyway). With the standard DDS middleware a subscriber that asks for **Reliable** does not match and receives nothing (our robot uses Zenoh, which is less strict). That is why you set Best Effort in RViz2 and in your own node. More in [QoS](qos.md).

## Try it

```bash
ros2 topic hz /scan                     # how many scans per second?
ros2 topic echo /scan --once --field angle_increment
ros2 topic echo /scan --once --field ranges
```

<details>

<summary>Check yourself</summary>

1. `angle_increment` is 0.0283 rad. How many degrees is that, and how many points do you expect per rotation?
   * 0.0283 × 57.3 ≈ 1.6°; 2π / 0.0283 ≈ 222 points.
2. Which index (approximately) points to the left if `len(ranges)` is 224?
   * 224 / 4 = 56 (angle +π/2).
3. A chair leg is 0.10 m in front of the lidar. What do you see in `ranges`?
   * Nothing useful: it is below the minimum range, you get `0.0`/`nan`.

</details>

Next: [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic/).

---

### 31. Odometry (/odom) and encoders  `[nieuw]`

<sub>theory/odometry.md</sub>


## What is odometry?

**Odometry** is estimating the position of the robot by **counting how far the
wheels have turned**. It is like walking with your eyes closed and counting your
steps: it works well for a short time, but small errors add up.

The robot starts at `(x, y, θ) = (0, 0, 0)` when `turtlebot3_node` starts. From
then on it adds every small movement to that position.

## Encoders on the TurtleBot3

Each wheel is driven by a Dynamixel **XL430** motor with a built-in encoder:

| | Burger |
|---|---|
| encoder ticks per wheel rotation | 4096 |
| wheel radius `r` | 0.033 m |
| distance between the wheels `L` | 0.160 m |
| wheel circumference `2πr` | 0.207 m |
| distance per tick | 0.207 / 4096 ≈ 0.05 mm |

You can see the raw values in two topics:

* `/sensor_state` (`turtlebot3_msgs/msg/SensorState`): `left_encoder`,
  `right_encoder` - the number of ticks (integer).
* `/joint_states` (`sensor_msgs/msg/JointState`): `position[]` of
  `wheel_left_joint` and `wheel_right_joint` in **radians** and `velocity[]` in rad/s.

From ticks to distance travelled by a wheel:

```
angle_wheel  = ticks * 2π / 4096        [rad]
distance     = angle_wheel * r          [m]
speed_wheel  = velocity * r             [m/s]   (velocity from /joint_states)
```

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

{% hint style="info" %}
**On our robot** the IMU helps: `turtlebot3_node` is configured with
`use_imu: true`. The **distance** comes from the wheel encoders, but the
**rotation θ** comes from the [IMU](imu.md). The IMU measures rotation better
than the wheels, which slip when the robot turns.
{% endhint %}

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

* the wheels **slip** (smooth floor, accelerating, turning)
* the wheel radius is not exactly 0.033 m (wear, tyre pressure, dust)
* bumps, thresholds, cables
* small errors in θ become large errors in x, y after a few metres

So `/odom` is **smooth and fast, but not correct over long distances**. To know
where the robot really is, SLAM or AMCL compares the [laser scan](laser-scan.md)
with a map and publishes a correction (`map -> odom`, see [TF](tf.md)).

## Try it

```bash
ros2 topic echo /odom --field pose.pose.position
ros2 topic echo /sensor_state --field left_encoder
ros2 topic echo /joint_states
```

Drive 1 m forward (mark it on the floor) and compare with `x` in `/odom`.
Then turn 4 times on the spot and look at `x`, `y`: are they still 0?

<details>

<summary>Check yourself</summary>

1. The left encoder went from 10 000 to 22 288 ticks. How far did the left wheel drive?
   * 12 288 ticks = 3 rotations → 3 × 0.207 m ≈ 0.62 m.
2. `/cmd_vel` has `linear.x = 0`, `angular.z = 1.0` rad/s. What are the wheel speeds?
   * v_left = -0.08 m/s, v_right = +0.08 m/s: turning left on the spot.
3. After driving through the lab for 5 minutes, the robot in RViz2 (fixed frame `odom`) is 30 cm next to where it really is. Is something broken?
   * No, that is normal odometry drift.

</details>

Next: [Read the encoder value](../ros2-nodes/read-the-encoder-value.md).

---

### 32. IMU (/imu)  `[nieuw]`

<sub>theory/imu.md</sub>


## What is an IMU?

An **IMU** (Inertial Measurement Unit) is a small chip that measures how the
robot **moves and rotates**. On the TurtleBot3 the IMU is on the **OpenCR**
board. It contains:

* a **gyroscope**: rotation speed around x, y and z (rad/s)
* an **accelerometer**: acceleration along x, y and z (m/s²)

(You know these sensors from your phone and from the flight controller of a drone.)

The OpenCR combines both in a filter and calculates the **orientation** of the
robot: how it is turned in space.

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

## The Imu message

`/imu` is of type `sensor_msgs/msg/Imu`, frame `imu_link`:

| field | meaning | robot standing still on the floor |
|---|---|---|
| `orientation` | rotation as a quaternion (`x, y, z, w`) | depends on the heading |
| `angular_velocity` | rad/s around x, y, z | ≈ 0, 0, 0 |
| `linear_acceleration` | m/s² along x, y, z | ≈ 0, 0, **9.81** |

{% hint style="info" %}
Standing still, the accelerometer measures **9.81 m/s² upwards**: it measures
gravity. That is how the IMU knows which way is down (roll and pitch). For yaw
there is no such reference, so yaw slowly **drifts**.
{% endhint %}

## Quaternions

ROS does not store orientation as three angles, but as a **quaternion**: four
numbers `(x, y, z, w)`. Quaternions have no problems with angles that jump from
+180° to -180° and are easy to combine. You don't have to understand the
maths, just remember:

* no rotation: `(0, 0, 0, 1)`
* for a ground robot only `z` and `w` change
* convert to **yaw** (in rad) like this:

```python
import math

q = msg.orientation          # also works for msg.pose.pose.orientation of /odom
yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                 1.0 - 2.0 * (q.y * q.y + q.z * q.z))
print(math.degrees(yaw))
```

## IMU and odometry on our robot

The wheels are good at measuring **distance**, but bad at measuring **rotation**:
during a turn the wheels slip. The gyroscope measures rotation directly. That is
why `turtlebot3_node` uses the yaw of the IMU for the heading in `/odom`
(`use_imu: true`, see [Odometry](odometry.md)).

| | wheel encoders | IMU (gyroscope) |
|---|---|---|
| distance | ✅ good | ❌ (double integration of acceleration → very large drift) |
| rotation | ⚠️ errors from slip | ✅ good, slow drift over time |

Combining sensors to get a better result than each sensor alone is called
**sensor fusion**.

## Try it

```bash
ros2 topic hz /imu
ros2 topic echo /imu --field angular_velocity
ros2 topic echo /imu --field linear_acceleration
```

* Turn the robot by hand around its vertical axis: which value of `angular_velocity` changes? Positive or negative to the left?
* Tilt the robot (carefully!): what happens with `linear_acceleration`?

<details>

<summary>Check yourself</summary>

1. The robot turns left at 0.5 rad/s. What does `angular_velocity.z` show?
   * About +0.5 (counterclockwise is positive).
2. The quaternion is `(0, 0, 0.707, 0.707)`. What is the yaw?
   * atan2(2·0.707·0.707, 1 − 2·0.707²) = atan2(1, 0) = π/2 → 90°, turned to the left.
3. Why can't we calculate the position of the robot from the accelerometer?
   * Acceleration has to be integrated twice; every small error grows very fast (quadratically in time).

</details>

---

### 33. TF - coordinate frames  `[nieuw]`

<sub>theory/tf.md</sub>


## The problem

Every sensor measures in **its own coordinate frame**:

* the lidar says "there is a wall 1.0 m in front of **me**" (frame `base_scan`)
* the IMU measures in **its** frame (`imu_link`)
* odometry says where the **robot** is relative to the **start point** (`odom`)

To draw the wall on the map, or to drive to it, we have to know how these
frames are positioned relative to each other. That is the job of **TF** (the
`tf2` library).

## Frames and transforms

A **frame** is a coordinate system with a name. A **transform** between two
frames is a translation (x, y, z) + a rotation (quaternion). All transforms
together form a **tree**: every frame has exactly one parent.

The TF tree of our TurtleBot3:

```
map                     ← only with SLAM or Nav2 (Cartographer / AMCL)
 └── odom               ← start point of the odometry
      └── base_footprint     ← the robot, on the floor (dynamic: turtlebot3_node)
           └── base_link          ← centre of the robot, 1 cm higher (static)
                ├── base_scan          ← the lidar        (static)
                ├── imu_link           ← the IMU          (static)
                ├── caster_back_link   ← caster           (static)
                ├── wheel_left_link    ← left wheel  (turns: robot_state_publisher)
                └── wheel_right_link   ← right wheel (turns: robot_state_publisher)
```

| transform | published by | kind |
|---|---|---|
| `map -> odom` | Cartographer (SLAM) or AMCL (Nav2) | dynamic, correction of the drift |
| `odom -> base_footprint` | `turtlebot3_node` (odometry) | dynamic, changes when driving |
| `base_footprint -> base_link -> base_scan, imu_link, ...` | `robot_state_publisher` (from the URDF) | **static**, fixed on the robot |
| `base_link -> wheel_*_link` | `robot_state_publisher` (from `/joint_states`) | dynamic, the wheels turn |

* **Dynamic** transforms are published on `/tf` many times per second.
* **Static** transforms are published once on `/tf_static` (they never change).

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
* `map` is **correct** (SLAM/AMCL compares the scan with the map) but **can jump** - good for "where am I in the lab".
* SLAM/AMCL publishes `map -> odom` so that `map -> odom -> base_footprint`
  gives the corrected position, without changing the odometry itself.

## Fixed frame in RViz2

In RViz2 the **Fixed Frame** is the frame in which everything is drawn:

* `base_link` - the robot stands still, the world moves around it
* `odom` - the world stands still, the robot drives (with drift)
* `map` - the robot drives on the map (only with SLAM / Nav2)

If RViz2 says *"No transform from [base_scan] to [map]"*, a link in the tree is
missing: for example SLAM is not running, so there is no `map -> odom`.

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

1. Which node publishes `odom -> base_footprint`, and what happens with it when you restart that node?
   * `turtlebot3_node`; the odometry starts again at (0, 0, 0).
2. You start RViz2 with Fixed Frame `map` but without SLAM. What do you see?
   * An error: there is no transform `map -> odom`, nothing is drawn.
3. You mount a camera 5 cm in front of the lidar. What do you need to add to the TF tree?
   * A static transform, e.g. `base_link -> camera_link` with x = -0.032 + 0.05 = 0.018 m (and the height):
     `ros2 run tf2_ros static_transform_publisher --x 0.018 --z 0.17 --frame-id base_link --child-frame-id camera_link`

</details>

Next: [Visualise the robot](../visualise-the-robot.md).

---

### 34. Driving the robot (/cmd_vel)  `[nieuw]`

<sub>theory/cmd-vel.md</sub>


## A speed, not a position

You don't tell the robot **where** to go, you tell it **how fast** to move
*right now*. That is the job of the topic `/cmd_vel` ("command velocity").
The robot keeps that speed until it gets a new command.

So "drive 10 cm" always becomes: drive at speed `v` during a time `t`, then
send speed 0 (or: drive until [odometry](odometry.md) says you did 10 cm).

## The Twist message

On our robot (ROS 2 Humble) `/cmd_vel` is a `geometry_msgs/msg/Twist`:

```
linear:            angular:
  x: 0.1   ← forward (m/s)    x: 0.0
  y: 0.0                      y: 0.0
  z: 0.0                      z: 0.5   ← turn (rad/s), positive = left
```

A **differential drive** robot can only use two of the six numbers:

| field | meaning | Burger max |
|---|---|---|
| `linear.x` | forward (+) / backward (-) | 0.22 m/s |
| `angular.z` | turn left (+) / right (-) | 2.84 rad/s |
| `linear.y`, `linear.z`, `angular.x`, `angular.y` | ignored: the robot cannot drive sideways, fly or roll | - |

Combining both gives a **curve** with radius `R = v / ω`. For example
`linear.x = 0.1`, `angular.z = 0.5` → a circle with a radius of 0.2 m.

How the robot turns this into two wheel speeds is explained in
[Odometry](odometry.md): `v_left = v - ω·L/2`, `v_right = v + ω·L/2`.

{% hint style="info" %}
In the simulation (ROS 2 Jazzy) `/cmd_vel` is a `TwistStamped`: the same
`Twist` inside `msg.twist`, plus a `header` with a time stamp.
{% endhint %}

## The path of a command on our robot

```
 teleop_keyboard ─┐
 Nav2            ─┼─► /cmd_vel      (prio 10) ─┐
 your node       ─┘                            │
 status page ───────► /cmd_vel_web  (prio 50) ─┼─► twist_mux ─► /cmd_vel_out ─► turtlebot3_node ─► OpenCR ─► motors
 gamepad F710 ──────► /cmd_vel_joy  (prio 100)─┘
```

* **twist_mux** passes only the source with the highest priority that sent
  something in the last 0.5 s (see
  [Manual control by terminal](../controlling-the-robot/manual-control-by-terminal.md)).
* `turtlebot3_node` limits the speed to what the robot can do and sends it to
  the OpenCR, which controls the two motors.

## Good habits

* **Publish regularly** (e.g. 10-20 times per second), not just once: twist_mux
  forgets a source after 0.5 s, and a regular stream is safer.
* **Always stop explicitly**: publish a `Twist()` with everything 0 when you are
  done, and also when your node stops (Ctrl+C). Don't count on the robot
  stopping by itself.
* **Start slow**: test with 0.05 m/s and 0.3 rad/s, with the robot on the floor
  and room around it.
* Keep the gamepad nearby: with **LB** you always take over (highest priority).

## Try it

```bash
# Turn slowly to the left, 10 times per second (Ctrl+C to stop)
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist "{angular: {z: 0.3}}"

# Stop
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{}"

# What arrives at the robot (after twist_mux)?
ros2 topic echo /cmd_vel_out
```

<details>

<summary>Check yourself</summary>

1. You publish `linear.y = 0.1`. What does the robot do?
   * Nothing: a differential drive robot cannot drive sideways.
2. Which command drives a circle with a radius of 0.5 m at 0.1 m/s, to the right?
   * `linear.x = 0.1`, `angular.z = -0.2` (ω = v / R = 0.1 / 0.5).
3. Your node publishes on `/cmd_vel`, but the robot does not react. A classmate is holding LB on the gamepad. Why?
   * `/cmd_vel_joy` has a higher priority in twist_mux; your commands are ignored.

</details>

Next: [Drive 10cm with a button](../ros2-nodes/drive-10cm-with-a-button.md).

---

### 35. QoS - Quality of Service  `[nieuw]`

<sub>theory/qos.md</sub>


## Why QoS?

Not every topic needs the same kind of delivery:

* A **laser scan** arrives 5 times per second. If one is lost on the wifi, it is no use sending it again: the next one is newer anyway.
* A **map** is published once. A node that starts later must still get it.
* A **command** that has to arrive should be sent again when it gets lost.

With **QoS** (Quality of Service) every publisher and subscriber says how it wants to send or receive messages.

## The three settings you need

| setting             | options               | meaning                                                                                    |
| ------------------- | --------------------- | ------------------------------------------------------------------------------------------ |
| **Reliability**     | `RELIABLE`            | a lost message is sent again (like TCP)                                                    |
|                     | `BEST_EFFORT`         | a lost message is lost, no waiting (like UDP) - good for sensors                           |
| **Durability**      | `VOLATILE`            | you only get messages sent **after** you subscribed                                        |
|                     | `TRANSIENT_LOCAL`     | the publisher keeps the last message(s); a **late** subscriber still gets them ("latched") |
| **History + depth** | `KEEP_LAST` + `depth` | how many messages are kept in the queue (e.g. 10)                                          |

There are more settings (deadline, lifespan, liveliness), but you won't need them in this lab.

When you write `self.create_subscription(Imu, '/imu', self.cb, 10)`, the `10` is the depth, and you get the **default** QoS: `RELIABLE`, `VOLATILE`, `KEEP_LAST 10`.

## Publisher and subscriber must match

In standard ROS 2 (DDS middleware, e.g. the simulation) a subscriber only receives messages if it asks for **the same or less** than the publisher offers:

| publisher offers | subscriber asks              | works?        |
| ---------------- | ---------------------------- | ------------- |
| RELIABLE         | RELIABLE                     | ✅             |
| RELIABLE         | BEST\_EFFORT                 | ✅             |
| BEST\_EFFORT     | BEST\_EFFORT                 | ✅             |
| BEST\_EFFORT     | **RELIABLE**                 | ❌ no messages |
| TRANSIENT\_LOCAL | VOLATILE or TRANSIENT\_LOCAL | ✅             |
| VOLATILE         | **TRANSIENT\_LOCAL**         | ❌ no messages |

The nasty part: there is **no error**, you simply get nothing (at most a warning _"incompatible QoS"_). With DDS, that is the classic "RViz2 does not show my laser scan".

{% hint style="info" %}
**Our real robot uses Zenoh** (`rmw_zenoh_cpp`) instead of DDS. Zenoh is less strict: a `RELIABLE` subscriber still receives a `BEST_EFFORT` topic. But your code and RViz2 settings should also work with DDS (other robots, other setups).
{% endhint %}

{% hint style="success" %}
**Rule of thumb:** subscribe to sensor data (`/scan`, `/imu`, ...) with **Best Effort**. A Best Effort subscriber works with a Reliable _and_ a Best Effort publisher: in the simulation (where the Gazebo bridge publishes `/scan` as Reliable), on our robot, and with DDS or Zenoh.
{% endhint %}

## QoS of the TurtleBot3 topics

| topic                                                               | reliability      | durability           | why                                                     |
| ------------------------------------------------------------------- | ---------------- | -------------------- | ------------------------------------------------------- |
| `/scan`                                                             | **BEST\_EFFORT** | VOLATILE             | sensor data (`SensorDataQoS`), newest is most important |
| `/odom`, `/imu`, `/joint_states`, `/battery_state`, `/sensor_state` | RELIABLE         | VOLATILE             | default QoS of `turtlebot3_node`                        |
| `/cmd_vel`                                                          | RELIABLE         | VOLATILE             | default QoS                                             |
| `/tf`                                                               | RELIABLE         | VOLATILE             | changes all the time                                    |
| `/tf_static`                                                        | RELIABLE         | **TRANSIENT\_LOCAL** | sent once; nodes that start later must still get it     |
| `/map` (map server, Nav2)                                           | RELIABLE         | **TRANSIENT\_LOCAL** | sent once; RViz2 started later must still see the map   |

Check it yourself: `ros2 topic info -v /scan` shows the QoS of every publisher and subscriber.

## QoS in Python

For sensor data there is a ready-made profile:

```python
from rclpy.qos import qos_profile_sensor_data

self.create_subscription(LaserScan, '/scan', self.scan_callback, qos_profile_sensor_data)
```

Or set it yourself, as in [Read in the scan topic](../ros2-nodes/read-in-the-scan-topic/):

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy

qos = QoSProfile(depth=10,
                 reliability=ReliabilityPolicy.BEST_EFFORT)

map_qos = QoSProfile(depth=1,
                     reliability=ReliabilityPolicy.RELIABLE,
                     durability=DurabilityPolicy.TRANSIENT_LOCAL)
```

In RViz2 you find the same settings per display under **Topic**: _Reliability Policy_, _Durability Policy_, _Depth_.

## Try it

```bash
ros2 topic info -v /scan
ros2 topic info -v /odom
ros2 topic echo --qos-reliability best_effort /scan --field ranges
```

<details>

<summary>Check yourself</summary>

1. Why is `/scan` Best Effort and not Reliable?
   * Resending an old scan over the wifi is useless (the next one arrives 0.2 s later) and causes extra traffic and delay.
2. With DDS, your subscriber on the real `/scan` uses `10` as QoS. What happens? And on our robot with Zenoh?
   * DDS: default = RELIABLE, publisher offers BEST\_EFFORT → incompatible, no messages. Zenoh: you receive the scans anyway.
3. You start RViz2 after the map server. Which durability do you need to see `/map`?
   * TRANSIENT\_LOCAL.

</details>

