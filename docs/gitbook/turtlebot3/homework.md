# Homework

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

## Startup at home

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
   [Simulation of sensors](#simulation-of-sensors) below.

5. Drive the robot (for task 1) in another terminal:

   ```sh
   ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
   ```

{% hint style="info" %}
Check: `ros2 topic list` in the container shows `/scan`, `/odom`, `/cmd_vel`,
... (and `/sim/battery_state` when step 4 runs).
{% endhint %}

## Task 1 - Scan sectors

Do the [Exercise](ros2-nodes/read-in-the-scan-topic/exercise.md) of *Read in the
scan topic* in the simulation (`turtlebot3_world.launch.py`): print the mean
distance **in front**, **left**, **behind** and **right** of the robot, and the
**closest obstacle** with its angle.

{% hint style="info" %}
Calculate the indices from `angle_increment` (see [Laser scan](theory/laser-scan.md)),
not with fixed numbers: then the same script works in the simulation (360 points)
and on the real robot (about 220-230 points).
{% endhint %}

## Task 2 - Battery warning

Start the [Simulation of sensors](#simulation-of-sensors) script below: it
publishes random values on `/sim/battery_state`. Write a node that subscribes to
`/sim/battery_state`, prints the voltage and the percentage, and prints a
**warning** when the voltage is below **11.2 V** or the percentage below **50 %**.

On the real robot you only change the topic to `/battery_state`.

## Task 3 - Drive exactly 1 m with odometry

In *Drive 10cm with a button* the robot drives on **time**. Now use **`/odom`**:
drive forward at 0.1 m/s until the robot has driven **1.0 m** from its start
position, then stop (publish all speeds 0).

* Subscribe to `/odom` and remember the start position.
* Distance from the start: `math.hypot(x - x0, y - y0)`.
* Publish `TwistStamped` on `/cmd_vel` (simulation).

Extra: turn exactly **90°** to the left, using the yaw from the quaternion
(see [IMU](theory/imu.md)).

## Task 4 - Theory

Answer the **Check yourself** questions of the theory pages:
[Laser scan](theory/laser-scan.md), [Odometry](theory/odometry.md),
[IMU](theory/imu.md), [TF](theory/tf.md), [cmd_vel](theory/cmd-vel.md) and
[QoS](theory/qos.md).

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

{% file src=".gitbook/assets/simulation_sensors.py" %}
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

## Hand in

Upload on Toledo, before the next session:

* your Python scripts of task 1, 2 and 3;
* a screenshot of the terminal output of each script;
* your answers of task 4.

{% hint style="success" %}
Next session: SLAM (make a map) and autonomous navigation with the real robot.
{% endhint %}
