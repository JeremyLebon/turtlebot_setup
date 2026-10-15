# Solution of homework task 3 (turn exactly 90 degrees) - for the lecturer, not synced to GitBook.
# Simulation (Jazzy): /cmd_vel is a TwistStamped. Real robot (Humble): use Twist.
import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry

TARGET = math.radians(90)   # rad, positive = left
MAX_SPEED = 0.5             # rad/s
MIN_SPEED = 0.05            # rad/s
TOLERANCE = math.radians(1)


def yaw_from_quaternion(q):
    return math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                      1.0 - 2.0 * (q.y * q.y + q.z * q.z))


class Turn90(Node):
    def __init__(self):
        super().__init__('turn_90')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        self.start_yaw = None
        self.done = False

    def odom_callback(self, msg):
        if self.done:
            return
        yaw = yaw_from_quaternion(msg.pose.pose.orientation)
        if self.start_yaw is None:
            self.start_yaw = yaw
            self.get_logger().info(f'start yaw {math.degrees(yaw):.1f} deg')

        turned = yaw - self.start_yaw
        turned = math.atan2(math.sin(turned), math.cos(turned))   # wrap to -pi..pi
        error = TARGET - turned

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        if abs(error) < TOLERANCE:
            self.done = True                    # stop: all speeds 0
            self.get_logger().info(f'done: turned {math.degrees(turned):.1f} deg')
        else:
            speed = max(MIN_SPEED, min(MAX_SPEED, 1.5 * abs(error)))   # slower near the end
            cmd.twist.angular.z = math.copysign(speed, error)
        self.pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = Turn90()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.pub.publish(TwistStamped())   # make sure the robot stops
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
