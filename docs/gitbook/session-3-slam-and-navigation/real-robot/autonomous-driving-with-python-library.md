# Autonomous driving with python library

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
