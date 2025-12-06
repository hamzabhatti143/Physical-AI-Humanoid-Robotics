---
title: Building ROS 2 Packages with Python and rclpy
sidebar_position: 3
description: A comprehensive guide to building ROS 2 packages using Python and the rclpy client library.
---

# Building ROS 2 Packages with Python and rclpy

ROS 2 (Robot Operating System 2) provides a flexible framework for robot application development. When working with Python, `rclpy` is the official client library that allows you to interface with the ROS 2 system. This module will guide you through the essentials of creating and managing ROS 2 packages using Python and `rclpy`.

## rclpy Basics

`rclpy` is built on top of the underlying ROS 2 C++ client library (`rcl`) and provides Python bindings. It allows Python developers to write ROS 2 nodes, publish and subscribe to topics, manage parameters, and interact with other ROS 2 constructs.

At its core, a ROS 2 application written in Python will typically involve:
- Initializing `rclpy`.
- Creating a node.
- Spinning the node to process callbacks.
- Shutting down `rclpy`.

Here's a minimal example of a ROS 2 Python node:

```python
import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args) # Initialize rclpy

    node = Node('my_minimal_node') # Create a node with a name
    node.get_logger().info('Minimal ROS 2 Python Node has started!')

    rclpy.spin(node) # Keep node alive until Ctrl+C or shutdown

    node.destroy_node() # Clean up when done
    rclpy.shutdown() # Shut down rclpy

if __name__ == '__main__':
    main()
```

## Creating Publishers and Subscribers

Communication in ROS 2 primarily happens through topics. Nodes can publish messages to topics or subscribe to messages from topics.

### Publishers

A publisher node sends messages to a specific topic. You need to import the appropriate message type from the ROS 2 interfaces.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Import the String message type
import time

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10) # Create a publisher
        self.i = 0
        self.timer = self.create_timer(0.5, self.timer_callback) # Publish every 0.5 seconds

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2! Count: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscribers

A subscriber node receives messages from a topic. It defines a callback function that is executed whenever a new message arrives.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Parameter Handling

ROS 2 parameters allow you to configure nodes at runtime. `rclpy` provides methods to declare, get, set, and interact with parameters.

### Declaring and Getting Parameters

Parameters can be declared with default values, and then retrieved by other parts of your node or external tools.

```python
import rclpy
from rclpy.node import Node

class ParameterNode(Node):

    def __init__(self):
        super().__init__('parameter_node')
        self.declare_parameter('my_parameter', 'default_value') # Declare a parameter
        timer_period = 1.0
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info(f'Hello with parameter: {my_param}')

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

You can set parameters from the command line:
`ros2 run your_package parameter_node --ros-args -p my_parameter:=new_value`

## Launch Files

Launch files are XML or Python files used to start multiple ROS 2 nodes and configure their parameters in a structured way. Python launch files are more powerful as they allow for conditional logic and more complex setups.

Here's a simple Python launch file (`my_launch_file.launch.py`) that starts the publisher and subscriber nodes:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='your_package_name', # Replace with your package name
            executable='minimal_publisher', # Replace with your publisher executable name
            name='talker',
            output='screen'
        ),
        Node(
            package='your_package_name', # Replace with your package name
            executable='minimal_subscriber', # Replace with your subscriber executable name
            name='listener',
            output='screen'
        )
    ])
```

To run this launch file:
`ros2 launch your_package_name my_launch_file.launch.py`

## Conclusion

This module provided an introduction to developing ROS 2 applications with Python and `rclpy`. You've learned how to create basic nodes, implement publishers and subscribers for topic-based communication, handle node parameters for runtime configuration, and orchestrate multiple nodes using Python launch files. These fundamental concepts are crucial for building complex robotic systems with ROS 2.
