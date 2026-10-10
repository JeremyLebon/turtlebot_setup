> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/autonomous-driving-with-python-library.md).

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

**Change max speed.**

\
Go to turtlebot.yaml file

```
nano /opt/ros/jazzy/share/turtlebot3_navigation2/param/burger.yaml
```

Go to the line FollowPath

```yaml
    FollowPath:
      plugin: "dwb_core::DWBLocalPlanner"
      debug_trajectory_details: true
      min_vel_x: 0.0
      min_vel_y: 0.0
      max_vel_x: 0.3
      max_vel_y: 0.0
      max_vel_theta: 1.0
      min_speed_xy: 0.0
      max_speed_xy: 0.3
      min_speed_theta: 0.0
```

Change the `max_vel_x`, `max_vel_theta` and `max_speed_xy` if needed
