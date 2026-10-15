# Startup at home

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
