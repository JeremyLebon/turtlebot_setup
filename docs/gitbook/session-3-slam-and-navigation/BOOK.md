# Session 3 - SLAM and navigation

_Alle pagina's in leesvolgorde. Statuslabel per pagina tussen haakjes; bron: `docs/gitbook/session-3-slam-and-navigation/`._

---

## 1. Session 3 - SLAM and navigation  `[nieuw]`

<sub>README.md</sub>


In this session the robot learns its environment and drives on its own:

* **SLAM** (Simultaneous Localization And Mapping): the robot makes a **map**
  of the room with its lidar, while it keeps track of where it is on that map.
* **Navigation** with **Nav2**: on that map you give a goal, the robot plans a
  path and drives there by itself, around obstacles.

You do it twice: first in the **simulation** (safe, the same world every time),
then on the **real robot**.

1. [Part 1 - In simulation](simulation/README.md) - slam\_toolbox and Nav2 in Gazebo
2. [Part 2 - On the real robot](real-robot/README.md) - Cartographer and Nav2 on the TurtleBot3

{% hint style="info" %}
Theory you need: **TF - map and odom** (why there is a `map` frame next to
`odom`) and **Odometry - why it drifts**, in the theory chapter of the
simulation and Turtlebot3 books.
{% endhint %}

---

## 2. Part 1 - In simulation  `[nieuw]`

<sub>simulation/README.md</sub>


Work in the simulation container `gazebo_turtlebot_cont`, as in the simulation
book (ROS 2 Jazzy, Gazebo).

1. [SLAM / Mapping](slam-mapping/README.md) - make a map of the TurtleBot3 world with slam\_toolbox and save it
2. [Autonomous Navigation](autonomous-navigation/README.md) - navigate on your map with Nav2, also from Python

Then do the same with the real robot: [Part 2 - On the real robot](../real-robot/README.md).

---

### 3. SLAM / Mapping  `[gewijzigd]`

<sub>simulation/slam-mapping/README.md</sub>


1. [Startup](startup.md) - Gazebo and slam\_toolbox
2. [Start mapping](start-mapping.md) - drive around and build the map
3. [Save map](save-map.md) - save the map for navigation

---

#### 4. Startup  `[ongewijzigd]`

<sub>simulation/slam-mapping/startup.md</sub>


Go the terminal where docker compose up is used. And stop it with CRTL + C

Restart the container with docker compose up.&#x20;

Open a new terminal and connect with&#x20;

```sh
docker exec -it gazebo_turtlebot_cont bash
```

Select the `burger` turtlebot3 as loaded model in Gazebo with the following command

```sh
export TURTLEBOT3_MODEL=burger
```

Use extra terminals to start the following ros2 nodes

<pre class="language-sh"><code class="lang-sh"><strong>ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
</strong></code></pre>

{% code overflow="wrap" %}

```sh
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -p stamped:=true -p frame_id:="base_link"
```

{% endcode %}

Make sure the `turtlebot3_gazebo` node and t`eleop_twist_keyboard` are running.

---

#### 5. Start mapping  `[ongewijzigd]`

<sub>simulation/slam-mapping/start-mapping.md</sub>


Open a new terminal and connect to the docker container.

Add the following command

```sh
export TURTLEBOT3_MODEL=burger
```

Start the mapping script

```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py slam:=True
```

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FZ1g74ImNk5Yt3xcrBrxs%2Fimage.png?alt=media&amp;token=4dfb77c9-0802-4d96-b259-77edadf94dad" alt=""><figcaption></figcaption></figure>

Rviz2 should be started.

You can see that a partially obstacle map is generated.&#x20;

Try to ride, move around and map the entire world.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FGdexf1LRrE5fHolpf73i%2Fimage.png?alt=media&amp;token=699a5a01-1eec-4580-bfdc-eacc7e79a9ec" alt=""><figcaption></figcaption></figure>

---

#### 6. Save map  `[gewijzigd]`

<sub>simulation/slam-mapping/save-map.md</sub>


With the following command in a new terminal the map can be saved.

{% hint style="warning" %}
It is important not to stop the mapping node of the previous step.
{% endhint %}

{% code overflow="wrap" %}
```sh
ros2 run nav2_map_server map_saver_cli -f /home/dockeruserjazzy/my_map --free 0.196 --occ 0.65
```
{% endcode %}

You get two files: `my_map.pgm` (the image) and `my_map.yaml` (resolution,
origin, thresholds). The `.yaml` is what Nav2 needs in the next step.

{% hint style="info" %}
`--free 0.196`: otherwise grey (unknown) cells are loaded as free space later on,
and Nav2 plans paths through unexplored areas. Want a PNG to put in a report?
Add `--fmt png` (the `.yaml` then points to the `.png`).
{% endhint %}

If you look in the directory with VS Code inside the container, you can find the
image of the map. This map will be used as base map for the autonomous navigation.

---

### 7. Autonomous Navigation  `[gewijzigd]`

<sub>simulation/autonomous-navigation/README.md</sub>


{% hint style="danger" %}
Cancel the SLAM command of the previous step with `CTRL + C` !!!!
{% endhint %}

Start Nav2 with **your** map from the previous step:

{% code overflow="wrap" %}
```sh
ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=/home/dockeruserjazzy/my_map.yaml
```
{% endcode %}

{% hint style="warning" %}
* Without `map:=...` Nav2 loads the default map of the TurtleBot3 package, not yours.
* `use_sim_time:=True` is needed here because Gazebo publishes a simulated
  clock. On the **real** robot you leave it out (see the TurtleBot3 book).
{% endhint %}

## Set the initial position of the turtlebot3

Set the initial pose of the TurtleBot3 with the **2D Pose Estimate** button.

After the pose is set, autonomous navigation should be possible.

Use the **Nav2 Goal** button to set a desired goal. After setting it, the
TurtleBot3 should start navigating.

Try to navigate to a point and drop an obstacle in Gazebo. You see the
calculated path will change when the obstacle is detected.

---

#### 8. Autonomous driving with python library  `[ongewijzigd]`

<sub>simulation/autonomous-navigation/autonomous-driving-with-python-library.md</sub>


Make a nav2\_simple.py script via VScode  > WSL > docker container (See The first ros2 node)

The script makes use of the [nav2\_simple\_commander](https://docs.nav2.org/commander_api/index.html) library

```python
#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from copy import deepcopy

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

"""
Basic stock inspection demo. In this demonstration, the expectation
is that there are cameras or RFID sensors mounted on the robots
collecting information about stock quantity and location.
"""


def main():
    rclpy.init()

    navigator = BasicNavigator()

    # Inspection route, probably read in from a file for a real application
    # from either a map or drive and repeat. (x, y, yaw)
    inspection_route = [
        [2.0, -0.55, 1.57],
        [0.0, -0.55, 1.57],
        [1.5, -0.55, -1.57],
        
    ]

    # Set our demo's initial pose
    # initial_pose = PoseStamped()
    # initial_pose.header.frame_id = 'map'
    # initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    # initial_pose.pose.position.x = 0.0
    # initial_pose.pose.position.y = 0.0
    # initial_pose.pose.orientation.z = 0.0
    # initial_pose.pose.orientation.w = 1.0
    # navigator.setInitialPose(initial_pose)

    # Wait for navigation to fully activate
    navigator.waitUntilNav2Active()

    # Send our route
    inspection_points = []
    inspection_pose = PoseStamped()
    inspection_pose.header.frame_id = 'map'
    inspection_pose.header.stamp = navigator.get_clock().now().to_msg()
    for pt in inspection_route:
        inspection_pose.pose.position.x = pt[0]
        inspection_pose.pose.position.y = pt[1]
        # Simplification of angle handling for demonstration purposes
        if pt[2] > 0:
            inspection_pose.pose.orientation.z = 0.707
            inspection_pose.pose.orientation.w = 0.707
        else:
            inspection_pose.pose.orientation.z = -0.707
            inspection_pose.pose.orientation.w = 0.707
        inspection_points.append(deepcopy(inspection_pose))

    navigator.followWaypoints(inspection_points)

    # Do something during our route (e.x. AI to analyze stock information or upload to the cloud)
    # Simply the current waypoint ID for the demonstation
    i = 0
    while not navigator.isTaskComplete():
        i += 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(
                'Executing current waypoint: '
                + str(feedback.current_waypoint + 1)
                + '/'
                + str(len(inspection_points))
            )

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Inspection of shelves complete! Returning to start...')
    elif result == TaskResult.CANCELED:
        print('Inspection of shelving was canceled. Returning to start...')
    elif result == TaskResult.FAILED:
        print('Inspection of shelving failed! Returning to start...')

    # go back to start
    #initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    #navigator.goToPose(initial_pose)
    while not navigator.isTaskComplete():
        pass

    exit(0)


if __name__ == '__main__':
    main()
```

---

## 9. Part 2 - On the real robot  `[nieuw]`

<sub>real-robot/README.md</sub>


Before you start: the bringup runs on the robot and your laptop is connected
(Turtlebot3 book, *Turtlebot3 - startup*).

1. [SLAM](slam.md) - make a map of the room with Cartographer and save it
2. [Autonomous driving](autonomous-driving.md) - navigate on the map with Nav2
3. [Autonomous driving with python library](autonomous-driving-with-python-library.md) - send goals from Python (Nav2 Simple Commander)
4. [Compare planners and controllers](compare-planners-and-controllers.md) - how does the robot choose its path?
5. [Zones](zones.md) - keep-out zones and speed zones on the map

{% hint style="warning" %}
Real robot vs. simulation: Cartographer instead of slam\_toolbox, **no**
`use_sim_time`, `/cmd_vel` is a `Twist`, and the gamepad (LB) can always take over.
{% endhint %}

---

### 10. SLAM  `[gewijzigd]`

<sub>real-robot/slam.md</sub>


Make a map of the classroom.

There are two ways. Do **way 1 first** - that's where you learn what happens.

## Way 1 - yourself, with ROS 2 commands

Make sure the bringup runs on the robot and the `turtlebot-vis` container on your laptop is started (see the Turtlebot3 book, *Turtlebot3 - startup*).

In the **robot** container (web terminal or SSH):

```sh
ros2 launch turtlebot3_bringup robot.launch.py
```

In a new WSL terminal, in the **turtlebot-vis** container on your laptop:

```sh
ros2 launch turtlebot3_cartographer cartographer.launch.py
```

RViz2 opens with the map being built. Drive around (gamepad, status page or `teleop_keyboard`) and try to map the whole room. Drive slowly and turn slowly: Cartographer needs time to match the lidar scans.

When ready, save the map. Make the directory first:

```sh
mkdir -p /root/ros2_ws/maps
ros2 run nav2_map_server map_saver_cli -f /root/ros2_ws/maps/classroom --free 0.196 --occ 0.65
```

{% hint style="warning" %}
* Don't stop the mapping (Cartographer) before the map is saved.
* `--free 0.196`: otherwise grey (unknown) cells are loaded as free later on, and Nav2 plans paths through unexplored space.
{% endhint %}

You get two files: `classroom.pgm` (the image) and `classroom.yaml` (resolution, origin, thresholds). Open the `.pgm` in VS Code or Windows to look at it.

{% hint style="info" %}
Here Cartographer runs on your laptop and receives all lidar data over the wifi. That works, but it is heavy for the wifi and your laptop.
{% endhint %}

## Way 2 - with the status page

Status page > **Rijden** > **Kaart maken**: the bringup and Cartographer start **on the robot**. You see the map grow live with the robot and the lidar points. Give the map a name and click the save button (disk icon).

The map is stored **on the robot** and can be chosen directly on the **Navigatie** tab.

Show the map to the lecturer.

---

### 11. Autonomous driving  `[gewijzigd]`

<sub>real-robot/autonomous-driving.md</sub>


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

### 12. Autonomous driving with python library  `[gewijzigd]`

<sub>real-robot/autonomous-driving-with-python-library.md</sub>


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

### 13. Compare planners and controllers  `[nieuw]`

<sub>real-robot/compare-planners-and-controllers.md</sub>


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

### 14. Zones  `[nieuw]`

<sub>real-robot/zones.md</sub>


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

