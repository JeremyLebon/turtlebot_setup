# Play a sound

## Play a sound by terminal

The turtlebot can play a sound when sending a specific ros2 service.

```
ros2 service call /sound turtlebot3_msgs/srv/Sound value:\ 2
```

{% hint style="info" %}
Only value 0,1, 2 and 3 are implemented.
{% endhint %}

## Play a sound with rqt

<figure><img src="https://1503299445-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FjFguour9DiTaRsxIJsRZ%2Fuploads%2FcP4tbpiXSomyXAWwtjVJ%2Fimage.png?alt=media&amp;token=30733453-b8af-45da-8b5a-917d9f71af3c" alt=""><figcaption></figcaption></figure>

Play a sound with ros2 node

```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlebot3_msgs.srv import Sound  # Service type for TB3 sound
import sys
class SoundClientNode(Node):
    def __init__(self):
        super().__init__('turtlebot3_sound_client')
        # create the client
        self.cli = self.create_client(Sound, '/sound')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('/sound service not available, waiting...')
        self.req = Sound.Request()

    def play_sound(self, sound: int):
        self.req.value = sound
        self.get_logger().info(f'Calling /sound with value={sound}')
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future, timeout_sec=5.0)

        if self.future.done() and not self.future.cancelled():
            resp = self.future.result()
            if resp is not None:
                self.get_logger().info(f'Sound service call succeeded: {resp}')
            else:
                self.get_logger().error('Service call returned None')
        else:
            self.get_logger().error('Service call failed or timed out')

def main(args=None):
    rclpy.init(args=args)
    node = SoundClientNode()
    # Example: play sound #1 (turtlebot3 built-in sound). You can change number.
    node.play_sound(sound=int(sys.argv[1]))
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

```

Try to start the command.
