import rclpy
from rclpy.node import Node
from aisd_msgs.msg import Hand
from geometry_msgs.msg import Twist


class Move(Node):

    def __init__(self):
        super().__init__('move')
        self.subscription = self.create_subscription(
            Hand,
            'cmd_hand',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

    def listener_callback(self, msg):
        # desired twist angle and linear velocity
        angle = 0.0
        linear = 0.0
        if msg.xindex > 0.55:
            # index finger is to the right, spin right
            self.get_logger().info('right')
            angle = -0.1
        elif msg.xindex < 0.45:
            # index finger is to the left, spin left
            self.get_logger().info('left')
            angle = 0.1
        else:
            # index finger is around the middle, stop spinning
            angle = 0.0
        if msg.xindex > msg.xpinky:
            # hand is facing away from us, come gesture, so move forward
            self.get_logger().info('come')
            linear = 0.5
        else:
            # hand is facing towards us, stay gesture, dont move
            self.get_logger().info('stay')
            linear = 0.0
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angle
        if self.vel_publisher.get_subscription_count() > 0:
            self.vel_publisher.publish(twist)
        else:
            self.get_logger().info('waiting for subcriber')
            
def main(args=None):
    rclpy.init(args=args)

    move = Move()

    rclpy.spin(move)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    move.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()