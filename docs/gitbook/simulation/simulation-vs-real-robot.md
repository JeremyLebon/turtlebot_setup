# Simulation vs. real robot

**New page** (suggested at the end of this book, before going to the real
TurtleBot3). What you learned here works on the real robot, but a few things
differ:

| | Simulation (this book) | Real TurtleBot3 (lab) |
|---|---|---|
| ROS 2 version | **Jazzy** (Ubuntu 24.04) | **Humble** (Ubuntu 22.04) |
| Container | `gazebo_turtlebot_cont` (on your laptop) | `turtlebot_<nr>` on the robot + `turtlebot-vis` on your laptop |
| Communication | everything in one container | **Zenoh**: laptop <-> robot over the robot's own wifi `TB-AP-<nr>` |
| `/cmd_vel` message | `geometry_msgs/TwistStamped` | `geometry_msgs/Twist` |
| Teleop | `teleop_twist_keyboard ... -p stamped:=true` | `turtlebot3_teleop teleop_keyboard`, gamepad, or the status page |
| SLAM | `slam_toolbox` (`navigation2.launch.py slam:=True`) | **Cartographer** |
| Clock | `use_sim_time:=True` (Gazebo clock) | real clock: **no** `use_sim_time` |
| Who drives? | only you | twist_mux: gamepad > web page > `/cmd_vel` (your code, Nav2) |
| Your files | in the simulation container | `/root/ros2_ws` (laptop: `turtlebot_vis/ros2_ws`) |

## Example: publish cmd_vel

Simulation (Jazzy):

```python
from geometry_msgs.msg import TwistStamped
msg = TwistStamped()
msg.header.stamp = self.get_clock().now().to_msg()
msg.header.frame_id = 'base_link'
msg.twist.angular.z = 0.2
self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
```

Real robot (Humble):

```python
from geometry_msgs.msg import Twist
msg = Twist()
msg.angular.z = 0.2
self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
```

{% hint style="info" %}
A node that publishes the wrong type often gives no clear error: the robot simply
doesn't move. Check with `ros2 topic info /cmd_vel` which type is expected.
{% endhint %}
