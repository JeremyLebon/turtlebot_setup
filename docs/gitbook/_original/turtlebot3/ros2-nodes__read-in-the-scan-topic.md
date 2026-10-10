> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/turtlebot3/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/turtlebot3/ros2-nodes/read-in-the-scan-topic.md).

# Read in the scan topic

Make a Python script (`sub_scan.py`) that is subscribed to the `/scan` topic. Make the script inside the `turtlebot-vis` container in the directory `/root/ros_ws`.

Use the Remote explorer extension in VScode to make connection with the WSL and the running docker container. See the previous [session](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node)

Sometimes the extension python has be installed in the docker container via VScode

## Add the needed libraries

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy
import numpy as np
import math
```

{% hint style="info" %}

* `rclpy`: ROS 2 Python library
* `Node`: Base class for ROS 2 nodes
* `LaserScan`: Message type published on `/scan`
* `QoSProfile` & `ReliabilityPolicy`: Needed to match subscriber QoS with publisher
* `numpy`: Calculate the mean of the laserscan
* `math`: check if something is finite
  {% endhint %}

## Main function and lifecycle

```python
def main(args=None):
    rclpy.init(args=args)
    node = ScanSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

* `rclpy.init(args=args)`: initializes the ROS 2 client library (must be called before creating nodes).
* `node = ScanSubscriber()`: instantiates the node (runs `__init__`).
* `rclpy.spin(node)`: enters the ROS event loop, processing incoming messages and calling callbacks until shutdown.
* `except KeyboardInterrupt`: lets the user stop the node with `Ctrl+C`.
* `node.destroy_node()`: cleans up node resources.
* `rclpy.shutdown()`: finalizes the rclpy library and releases network resources.

<pre class="language-python"><code class="lang-python"><strong>if __name__ == '__main__':
</strong>    main()
</code></pre>

* Standard Python guard so `main()` runs only if the file is executed as a script (not if imported as a module).

## Make a Node class

Add the class above the `main` function.

```python
class ScanSubscriber(Node):
    def __init__(self):
        super().__init__('sub_scan')
```

\
Change the QoS (Quality of Service)&#x20;

Add this to the `__init__` function

```python
qos_profile = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    depth=10
)
```

* ROS 2 topics use Quality of Service (QoS).
* TurtleBot3 /scan LIDAR uses Best Effort, so we must match it.
* depth=10 sets the queue size.

Add the `create_subscription`  also to the `__init__` function.

```python
self.subscription = self.create_subscription(
    LaserScan,
    '/scan',
    self.scan_callback,
    qos_profile
)
```

* `create_subscription(...)` registers a subscriber on the node.
  * `LaserScan`: the message class expected.
  * `'/scan'`: topic to listen to.
  * `self.scan_callback`: function to call each time a message arrives.
  * `qos_profile`: ensures compatibility with the LIDAR publisher
* The returned subscription object is stored in `self.subscription` to keep a reference (prevents garbage collection).

{% hint style="info" %}
Make sure the indentation in Python is correct!
{% endhint %}

## Log vs. print

To print data to the terminal don't use the print statement. The print causes a significant delay. Use the logger instead. At this line below in the `__init__` function

```python
self.get_logger().info('LaserScan subscriber node started!')
```

## Callback function

Add the callback function to the class.

```python
def scan_callback(self, msg):
```

{% hint style="info" %}
This method is called each time a `LaserScan` message is received. `msg` is an instance of `sensor_msgs.msg.LaserScan`.
{% endhint %}

## Laserscan msg info

Explain fields of `LaserScan` (important to understand `msg.ranges`):

* `msg.header` — timestamp and frame id
* `msg.angle_min`, `msg.angle_max`, `msg.angle_increment` — describe the angular span and resolution of the scan
* `msg.range_min`, `msg.range_max` — valid range limits for the sensor
* `msg.ranges` — list (array) of distance measurements, usually one per angle step
* `msg.intensities` — (optional) reflectance / intensity values

Add the code below to the callback function

```python
# Filter out invalid (non-finite) values
msg.ranges = [r for r in msg.ranges if math.isfinite(r)]
```

This line removes any invalid values from msg.ranges.

* `msg.ranges` is typically a list of distance readings (for example, from a LIDAR sensor).
* `math.isfinite(r)` checks if a value is a real number — not `inf`, `-inf`, or `NaN`.
* The result is a cleaned list containing only valid distance measurements.

```python
# Log how many valid points we have
self.get_logger().info(f"Valid ranges: {len(msg.ranges)}")
```

This logs the number of valid range readings that remain after filtering.\
It helps you verify that the data is being received and processed correctly.

Below you see the build up of the laserscan. You get roughly 240 points per rotation

<img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2Fjl07REjZyMmR6JgmDR3O%2Ffile.excalidraw.svg?alt=media&amp;token=22bfd257-79c7-429b-afb2-85ec2fa16979" alt="" class="gitbook-drawing">

```python
# Get front sector — for example, 15 readings on each side of the forward direction
n = 15
front_full = msg.ranges[:n] + msg.ranges[-n:]
```

This selects the **front part** of the sensor’s field of view.

* The first `n` values (`msg.ranges[:n]`) represent readings from one side of the front.
* The last `n` values (`msg.ranges[-n:]`) represent readings from the other side of the front.\
  By combining them, `front_full` contains readings that roughly correspond to what’s **in front of the robot**.

```python
# Compute mean safely (in case list is empty)
mean_front = np.mean(front_full) if front_full else float('nan')
```

This computes the **average distance** in the front sector.

* It uses `numpy.mean()` to calculate the mean.
* If `front_full` is empty (e.g., no valid readings), it safely returns `NaN` instead of causing an error.

```python
self.get_logger().info(f"Front ranges ({len(front_full)}): mean={mean_front:.3f}")
```

Finally, this logs how many front readings were used and what their average distance was — formatted to three decimal places.
