# Session 4 - Project

_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/session-4-project/`._

---

## 1. Session 4 - Project  `[nieuw]`

<sub>README.md</sub>


In this session you make your **own project** with the real robot: the robot
navigates on a map with **SLAM** and the **Nav2 Simple Commander**, measures
something on the way, and you generate a **report** of the results.

1. [Measure while driving](measure-while-driving.md) - example: measure the battery at every waypoint
2. [Install python libraries in container](install-python-libraries-in-container.md) - matplotlib, reportlab, ... for your report

{% hint style="info" %}
You need the map and the navigation of *Session 3 - SLAM and navigation*.
{% endhint %}

---

## 2. Measure while driving  `[ongewijzigd]`

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

## 3. Install python libraries in container  `[gewijzigd]`

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

## 4. Solution: Measure while driving  `[gewijzigd]`

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

