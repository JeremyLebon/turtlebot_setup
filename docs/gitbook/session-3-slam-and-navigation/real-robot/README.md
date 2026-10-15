# Part 2 - On the real robot

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
