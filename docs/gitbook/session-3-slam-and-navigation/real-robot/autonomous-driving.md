# Autonomous driving

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
