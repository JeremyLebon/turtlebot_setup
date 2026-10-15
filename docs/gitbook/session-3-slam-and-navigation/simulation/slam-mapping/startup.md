# Startup

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
