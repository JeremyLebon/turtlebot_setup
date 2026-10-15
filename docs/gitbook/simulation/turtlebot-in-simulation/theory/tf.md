# TF - coordinate frames

## The problem

Every sensor measures in **its own coordinate frame**:

* the lidar says "there is a wall 1.0 m in front of **me**" (frame `base_scan`)
* the IMU measures in **its** frame (`imu_link`)
* odometry says where the **robot** is relative to the **start point** (`odom`)

To draw the wall in the world, or to drive to it, we have to know how these
frames are positioned relative to each other. That is the job of **TF** (the
`tf2` library).

## Frames and transforms

A **frame** is a coordinate system with a name. A **transform** between two
frames is a translation (x, y, z) + a rotation (quaternion). All transforms
together form a **tree**: every frame has exactly one parent.

The TF tree of the TurtleBot3 Burger in the simulation:

```
map                     ← only with SLAM or Nav2 (later in this book)
 └── odom               ← start point of the odometry
      └── base_footprint     ← the robot, on the floor (dynamic: Gazebo DiffDrive)
           └── base_link          ← centre of the robot, 1 cm higher (static)
                ├── base_scan          ← the lidar        (static)
                ├── imu_link           ← the IMU          (static)
                ├── caster_back_link   ← caster           (static)
                ├── wheel_left_link    ← left wheel  (turns: robot_state_publisher)
                └── wheel_right_link   ← right wheel (turns: robot_state_publisher)
```

| transform | published by | kind |
|---|---|---|
| `map -> odom` | slam_toolbox (SLAM) or AMCL (Nav2) | dynamic, correction of the drift |
| `odom -> base_footprint` | Gazebo DiffDrive plugin (via the bridge) | dynamic, changes when driving |
| `base_footprint -> base_link -> base_scan, imu_link, ...` | `robot_state_publisher` (from the URDF) | **static**, fixed on the robot |
| `base_link -> wheel_*_link` | `robot_state_publisher` (from `/joint_states`) | dynamic, the wheels turn |

* **Dynamic** transforms are published on `/tf` many times per second.
* **Static** transforms are published once on `/tf_static` (they never change).

On the real robot the tree is exactly the same; only `odom -> base_footprint`
comes from the robot driver instead of Gazebo.

## Positions on the Burger (from the URDF)

| from `base_link` to | x | y | z |
|---|---|---|---|
| `base_scan` (lidar) | -0.032 m | 0 | 0.172 m |
| `imu_link` | -0.032 m | 0 | 0.068 m |
| `wheel_left_link` | 0 | +0.080 m | 0.023 m |
| `wheel_right_link` | 0 | -0.080 m | 0.023 m |

`base_link` is 0.010 m above `base_footprint` (the floor).

So the lidar is **3.2 cm behind** the centre between the wheels. A wall at
1.000 m in the scan is at 1.000 - 0.032 = 0.968 m in front of `base_link`. TF
does this calculation for you.

## Why both `map` and `odom`?

* `odom` is **smooth** (no jumps) but **drifts** - good for the controller that drives.
* `map` is **correct** (SLAM/AMCL compares the scan with the map) but **can jump** - good for "where am I".
* SLAM/AMCL publishes `map -> odom` so that `map -> odom -> base_footprint`
  gives the corrected position, without changing the odometry itself.

## Fixed frame in RViz2

In RViz2 the **Fixed Frame** is the frame in which everything is drawn:

* `base_link` - the robot stands still, the world moves around it
* `odom` - the world stands still, the robot drives
* `map` - the robot drives on the map (only with SLAM / Nav2)

If RViz2 says *"No transform from [base_scan] to [map]"*, a link in the tree is
missing: for example SLAM is not running, so there is no `map -> odom`. That is
the Global Status error you see in [Show me the robot](../show-me-the-robot.md).

## Try it

```bash
# Show the TF tree as a PDF (frames_<date>.pdf in the current folder)
ros2 run tf2_tools view_frames

# Position of the robot relative to odom, live
ros2 run tf2_ros tf2_echo odom base_footprint

# Fixed offset of the lidar
ros2 run tf2_ros tf2_echo base_link base_scan
```

In RViz2: add the **TF** display and enable *Show Names*.

In Python you can ask TF for a transform with a `tf2_ros.Buffer` and a
`tf2_ros.TransformListener`:

```python
from tf2_ros import Buffer, TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)
...
t = self.tf_buffer.lookup_transform('odom', 'base_footprint', rclpy.time.Time())
self.get_logger().info(f"x={t.transform.translation.x:.2f} y={t.transform.translation.y:.2f}")
```

<details>

<summary>Check yourself</summary>

1. Who publishes `odom -> base_footprint` in the simulation? And on the real robot?
   * Simulation: the Gazebo DiffDrive plugin (via `ros_gz_bridge`). Real robot: the robot driver `turtlebot3_node`.
2. You start RViz2 with Fixed Frame `map` but without SLAM. What do you see?
   * An error: there is no transform `map -> odom`, nothing is drawn.
3. You mount a camera 5 cm in front of the lidar. What do you need to add to the TF tree?
   * A static transform, e.g. `base_link -> camera_link` with x = -0.032 + 0.05 = 0.018 m (and the height):
     `ros2 run tf2_ros static_transform_publisher --x 0.018 --z 0.17 --frame-id base_link --child-frame-id camera_link`

</details>

Next: [Show me the robot](../show-me-the-robot.md).
