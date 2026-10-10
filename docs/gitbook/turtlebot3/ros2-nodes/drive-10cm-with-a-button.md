# Drive 10cm with a button

Make a Python script (`pub_controlling_the_robot.py`). Make the script inside the `turtlebot-vis` container in the directory `/root/ros2_ws`.

## Imports and top-level setup

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
import time
```

* `rclpy` — the ROS 2 Python client library. It provides node lifecycle, spinning, and other ROS 2 functions.
* `Node` — base class for creating ROS 2 nodes in Python.
* `Twist` — ROS message type used to send velocity commands (`linear` and `angular`) (commonly published on `/cmd_vel`).
* `Joy` — ROS message type published by joystick drivers; it contains `axes` and `buttons` arrays.
* `time` — Python standard library module, used here for simple time and sleeps.

### Class definition and constructor

```python
class MoveOnJoyButton(Node):
    def __init__(self):
        super().__init__('move_on_joy_button')

        # Publisher voor snelheid
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # Abonneren op de joystick
        self.sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)

        self.last_button_state = 0
        self.get_logger().info("Druk op A (knop 0) op de controller om 10 cm vooruit te rijden")
```

* `MoveOnJoyButton` is a ROS 2 node class (inherits from `Node`).
* `super().__init__('move_on_joy_button')` sets the node name to `move_on_joy_button`.
* `self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)` creates a publisher that will publish `Twist` messages to the `/cmd_vel` topic. The `10` is the queue size (history depth) for the publisher.
* `self.sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)` subscribes to the joystick input on the `/joy` topic. When a `Joy` message arrives, `self.joy_callback` is called.
* `self.last_button_state = 0` stores the previous state of the A button so the code can detect the **rising edge** (press event).
* `self.get_logger().info(...)` logs an informational message. The logged text in your code is Dutch; it tells the user which button to press. (This is executed once when the node starts.)

### The joystick callback

```python
def joy_callback(self, msg: Joy):
    # Controleer of A is ingedrukt (index 0)
    if len(msg.buttons) > 0:
        pressed = msg.buttons[0]
        if pressed == 1 and self.last_button_state == 0:
            self.get_logger().info("A-knop ingedrukt → rijden 10 cm vooruit")
            self.drive_forward(0.10)
        self.last_button_state = pressed
```

* `joy_callback` is executed every time a `Joy` message arrives. `msg.buttons` is an array of integers (0 or 1), where `msg.buttons[0]` corresponds to the A button by convention in many controllers.
* `if len(msg.buttons) > 0:` ensures `msg.buttons[0]` exists before accessing it.
* `pressed = msg.buttons[0]` reads current state of button A.
* `if pressed == 1 and self.last_button_state == 0:` detects a **rising edge**: the button was previously unpressed (`0`) and is now pressed (`1`). That prevents repeated triggers while the button is held down.
* On that rising edge the node logs a message (Dutch: “A button pressed → drive 10 cm forward”) and calls `self.drive_forward(0.10)` to move 0.10 meters forward.
* `self.last_button_state = pressed` updates the stored state for the next callback.

### The drive routine

```python
def drive_forward(self, distance):
    speed = 0.05  # m/s
    duration = distance / speed

    twist = Twist()
    twist.linear.x = speed

    end_time = time.time() + duration
    while time.time() < end_time:
        self.cmd_pub.publish(twist)
        time.sleep(0.05)

    twist.linear.x = 0.0
    self.cmd_pub.publish(twist)
    self.get_logger().info("Beweging voltooid")
```

* `drive_forward(self, distance)` takes a distance in meters (here called with `0.10` for 10 cm).
* `speed = 0.05` sets a constant forward linear speed of 0.05 m/s.
* `duration = distance / speed` calculates how many seconds to publish that speed to cover the requested distance. Example: `0.10 / 0.05 = 2 seconds`.
* A `Twist()` message is created and `twist.linear.x = speed` sets forward velocity. (Other fields remain zero.)
* `end_time = time.time() + duration` sets a wall-clock time when motion should stop.
* The `while` loop repeatedly publishes the `Twist` message until the end time is reached. Inside the loop it sleeps `0.05` seconds between publishes — this effectively publishes at \~20 Hz.
* After the loop, the code sets `twist.linear.x = 0.0` and publishes once to stop the robot.
* It logs a message in Dutch: “Movement complete”.

**Important note about this implementation:** the `drive_forward` method is *blocking*. It uses `time.sleep()` and a while loop inside the callback chain. That blocks the node’s thread while driving and prevents other incoming callbacks from running on the same thread.

{% hint style="warning" %}
This node publishes on `/cmd_vel`: the lowest priority in **twist_mux**. While
someone drives with the gamepad or the arrows on the status page, your commands
are ignored (see [Manual control by terminal](../controlling-the-robot/manual-control-by-terminal.md)).
Try it: start your node, press A, and keep LB on the gamepad pressed at the same time.
{% endhint %}

{% hint style="info" %}
On the real robot (ROS 2 Humble) `/cmd_vel` is a `Twist`. In the simulation
(ROS 2 Jazzy) it is a `TwistStamped` - code from the simulation needs a small change.
{% endhint %}

### Node lifecycle / program entry point

```python
def main(args=None):
    rclpy.init(args=args)
    node = MoveOnJoyButton()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

* `rclpy.init()` initializes the ROS 2 client library.
* `node = MoveOnJoyButton()` creates your node instance.
* `rclpy.spin(node)` starts the ROS 2 event loop: it listens for messages and calls callbacks (like `joy_callback`). `spin` blocks until the node is shut down.
* On `KeyboardInterrupt` (Ctrl+C) the code continues to shutdown gracefully: `node.destroy_node()` and `rclpy.shutdown()`.
