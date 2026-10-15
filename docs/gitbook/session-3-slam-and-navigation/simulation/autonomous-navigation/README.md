# Autonomous Navigation

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
