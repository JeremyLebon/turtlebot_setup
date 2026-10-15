# Solution of homework task 1 (obstacle alarm) - for the lecturer, not synced to GitBook.
# Works on the real robot (sound via /sound) and in the simulation (no /sound
# service there: it logs "/sound service not available").
import math

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from sensor_msgs.msg import LaserScan
from turtlebot3_msgs.srv import Sound

ALARM_DISTANCE = 0.30   # m
MIN_VALID = 0.12        # m: smaller values (0.0) = no echo


class ObstacleAlarm(Node):
    def __init__(self):
        super().__init__('obstacle_alarm')
        qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT, depth=10)
        self.create_subscription(LaserScan, '/scan', self.scan_callback, qos)
        self.sound_client = self.create_client(Sound, '/sound')
        self.alarm = False   # was the obstacle already there in the previous scan?
        self.get_logger().info('Obstacle alarm started')

    def scan_callback(self, msg):
        n = 15
        front = list(msg.ranges[:n]) + list(msg.ranges[-n:])
        front = [r for r in front if math.isfinite(r) and r > MIN_VALID]
        if not front:
            return
        closest = min(front)

        if closest < ALARM_DISTANCE and not self.alarm:     # obstacle appears
            self.get_logger().warn(f'obstacle at {closest:.2f} m!')
            self.play_sound(3)         # extra, real robot: 3 = error melody
            self.alarm = True
        elif closest >= ALARM_DISTANCE and self.alarm:     # obstacle gone
            self.get_logger().info('free again')
            self.alarm = False

    def play_sound(self, value):
        if not self.sound_client.service_is_ready():
            self.get_logger().warn('/sound service not available')
            return
        request = Sound.Request()
        request.value = value
        self.sound_client.call_async(request)   # don't wait inside a callback


def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAlarm()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
