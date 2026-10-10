> For the complete documentation index, see [llms.txt](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/llms.txt). Markdown versions of documentation pages are available by appending `.md` to page URLs; this page is available as [Markdown](https://vives-4.gitbook.io/ros2-simulation-turtlebo-gazebo/the-first-ros2-node.md).

# The first ros2 node

## Connect to the container via VScode

Make sure the `turtlebot3_gazebo` node and t`eleop_twist_keyboard` is running.

Open VScode and use the Remote Explorer in VScode.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F4gVfVBGdrmG81hQkuGaE%2Fimage.png?alt=media&amp;token=489d161f-750e-4197-a858-84cdc20b5720" alt=""><figcaption></figcaption></figure>

Select *WSL Targets* and select *Ubuntu-22.04*

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fuql0D1fIp2NdALC78tim%2Fimage.png?alt=media&amp;token=61074534-e4a7-4997-91a2-115772b1304e" alt=""><figcaption></figcaption></figure>

After connecting, you should see below that you are connected to the WSL target.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FmZIjktpamZ37ACKqxlor%2Fimage.png?alt=media&amp;token=1a59cc5c-6be0-486a-a229-efa23eb14bb2" alt=""><figcaption></figcaption></figure>

After the connection, select Dev Containers again in the remote explorer dropdown menu.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FJ0t6nXGbRSHsmkPxDwln%2Fimage.png?alt=media&amp;token=25c48d15-72f7-4eae-bf56-457ff220b78d" alt=""><figcaption></figcaption></figure>

Select the ros2-jazzy-gazebo-turtlebot. Click on the arrow to connect.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F5IyrVViWo3rFjiKEcBAO%2Fimage.png?alt=media&amp;token=2d99fee1-609f-4cb6-afb1-8a3b14c35ae7" alt=""><figcaption></figcaption></figure>

You should now be inside the Docker container. You may be asked to select a directory in the Docker container.

## Make your first ROS 2 node

### Subscribe to /odom

The objective is to read out the location of the turtlebot with our own written Python script.

Make a new directory, `turtlebot` and make a `turtlebot_subscribe.py` script.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F9VzjsmJr7wkCoOzcnJVM%2Fimage.png?alt=media&amp;token=5159afc2-8983-4a66-8615-616ca03a4ea0" alt=""><figcaption></figcaption></figure>

Paste the code below in the `turtlebot_subscribe.py`

<details>

<summary>Python script</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from math import atan2, asin

class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_listener')
        # Subscribe to the /odom topic
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.get_logger().info("Subscribed to /odom topic.")

    def odom_callback(self, msg):
        # Extract position
        pos = msg.pose.pose.position
        # Extract orientation (quaternion)
        ori = msg.pose.pose.orientation

        # Convert quaternion to yaw (2D orientation)
        siny_cosp = 2 * (ori.w * ori.z + ori.x * ori.y)
        cosy_cosp = 1 - 2 * (ori.y * ori.y + ori.z * ori.z)
        yaw = atan2(siny_cosp, cosy_cosp)

        # Log position and yaw
        self.get_logger().info(
            f"Position -> x: {pos.x:.3f}, y: {pos.y:.3f}, "
            f"Yaw: {yaw:.3f} rad"
        )

def main(args=None):
    rclpy.init(args=args)
    node = OdomSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

```

</details>

Analyse the Python code. And try to understand what is happening.

Run the code with the following command in VScode terminal.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FizQRvsCKr4Yakbz52Psb%2Fimage.png?alt=media&amp;token=7258d38e-4be6-4ee6-b058-f1a22de88a15" alt=""><figcaption></figcaption></figure>

Make sure you are in the directory of the python script.

```
python turtlebot_subscribe.py
```

Then drive the turtlebot around. You see, the position and orientation should change.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2Fxd1mgaz95dHeLv8FhaWX%2Fimage.png?alt=media&amp;token=022a1449-c9cf-417c-94a4-ec7a6412eefd" alt=""><figcaption></figcaption></figure>

### Publish the cmd\_vel

The objective is to control the turtlebot with our own written Python script. To make it easy, the turtlebot will just be turning around.

Make a `turtlebot_publish.py` script.

Paste the code below in the `turtlebot_publish.py`

Analyse the Python code. And try to understand what is happening.

<details>

<summary>Python script</summary>

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped

class CmdVelStampedPublisher(Node):
    def __init__(self):
        super().__init__('cmd_vel_stamped_publisher')
        
        # Publisher for TwistStamped messages
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        
        # Timer to publish at 10 Hz
        self.timer = self.create_timer(0.1, self.publish_velocity)
        
        # Example motion parameters
        self.linear_speed = 0.0   # m/s forward
        self.angular_speed = 0.2  # rad/s rotation
        
        self.get_logger().info("Publishing TwistStamped messages on /cmd_vel_stamped")

    def publish_velocity(self):
        msg = TwistStamped()
        
        # Stamp message with current ROS time
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        # Set linear and angular velocity
        msg.twist.linear.x = self.linear_speed
        msg.twist.angular.z = self.angular_speed
        
        self.publisher.publish(msg)
        self.get_logger().info(
            f"Published TwistStamped: linear.x={msg.twist.linear.x:.2f}, angular.z={msg.twist.angular.z:.2f}"
        )

def main(args=None):
    rclpy.init(args=args)
    node = CmdVelStampedPublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

```

</details>

Run the code with the following command in VScode terminal.&#x20;

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FHJhni9phH0g7pYedLbm8%2Fimage.png?alt=media&amp;token=93f92315-13f8-4ff3-b701-7b817c5690c7" alt=""><figcaption></figcaption></figure>

The Turtlebot3 should be turning slowly.

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2FNrd3Jm5t1AYtYX3qXPd2%2Fimage.png?alt=media&amp;token=cbf1e1de-e207-43b7-a0bd-2c46b7c2d07a" alt=""><figcaption></figcaption></figure>

<figure><img src="https://2210214786-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2Fu6u3SP6puU3zF003QGfq%2Fuploads%2F3TfIOrCA9Q9lyppz4Py5%2F20251019-1330-11.4924500.gif?alt=media&amp;token=fdf77290-1e74-48a9-85e5-44478f62de47" alt=""><figcaption></figcaption></figure>

Change the Python code so that the Turtlebot:&#x20;

* can turn faster&#x20;
* or even drive straight.
