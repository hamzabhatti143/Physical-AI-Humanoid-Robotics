---
title: "Week 4: ROS 2 Core Communication Concepts"
---

## 2. ROS 2 Core Communication Concepts

ROS 2 is built upon a modular architecture where different functionalities are encapsulated into independent units that communicate with each other. The primary communication mechanisms in ROS 2 are Nodes, Topics, Services, and Actions.

### 2.1 Nodes

#### Definition and role of nodes in a robotic system

A **Node** is the fundamental unit of computation in ROS 2. It is an executable process that performs a specific task, such as reading sensor data, controlling a motor, or performing complex path planning. Each node is designed to be self-contained and focused on a single responsibility, promoting modularity and reusability within the robotic system.

Nodes communicate with each other using the other ROS 2 communication primitives (Topics, Services, Actions), forming a distributed graph of processes that collectively achieve the robot's overall functionality.

#### Node lifecycle (init, spin, destroy)

ROS 2 introduces a managed lifecycle for nodes, allowing for more predictable and robust system behavior. While simple nodes can run with a basic `spin` loop, more advanced nodes can implement a lifecycle that includes states like:

*   **Unconfigured**: Initial state, ready to be configured.
*   **Inactive**: Configured but not yet active.
*   **Active**: The node is running its primary operations (e.g., publishing data, receiving commands).
*   **Finalized**: The node is shutting down.

Common operations within a node's execution include:

*   **Initialization (`init`)**: Setting up publishers, subscribers, services, and parameters.
*   **Spinning (`spin`)**: The main loop where the node processes incoming messages and executes callbacks. This is typically an infinite loop that keeps the node alive.
*   **Destruction (`destroy`)**: Releasing resources and performing cleanup tasks when the node is shut down.

#### Example: Motor controller node; sensor-processing node

*   **Motor Controller Node**: This node might subscribe to a topic like `/cmd_vel` (command velocity) and publish to a topic like `/joint_states`. Its responsibility is to translate high-level velocity commands into low-level motor signals to drive the robot's wheels or joints, and to report the current state of those joints.
*   **Sensor-Processing Node**: This node could subscribe to raw data from a `/camera/image_raw` topic, process the image (e.g., detect objects, estimate depth), and then publish the processed information to a new topic like `/object_detection_results` or `/depth_map`.

### 2.2 Topics

#### Publish/subscribe communication

**Topics** are the most common way for nodes to asynchronously exchange data in ROS 2. They implement a **publish/subscribe** communication model:

*   **Publisher**: A node that sends messages on a specific topic.
*   **Subscriber**: A node that receives messages from a specific topic.

When a publisher publishes a message to a topic, all nodes subscribed to that topic receive a copy of the message. This one-to-many or many-to-many communication pattern is ideal for streaming data, such as sensor readings, control commands, or status updates.

#### Message types (std_msgs, sensor_msgs, custom messages)

Messages exchanged over topics must adhere to a predefined structure called a **message type**. ROS 2 provides a rich set of standard message types organized into packages:

*   `std_msgs`: Contains basic data types like `String`, `Int32`, `Float64`, `Bool`, etc.
*   `sensor_msgs`: Contains common sensor data types such as `Image`, `PointCloud2`, `Imu`, `JointState`, `CameraInfo`, etc.
*   `geometry_msgs`: Contains messages for geometric primitives like `Point`, `Pose`, `Quaternion`, `Twist`, etc.

Developers can also define **custom message types** using `.msg` files to handle application-specific data structures. These custom messages allow for rich, structured data exchange tailored to the robot's needs.

#### QOS settings and reliability for real robots

ROS 2 leverages DDS's **Quality of Service (QoS) settings** to configure the reliability, urgency, and lifespan of message communication. These settings are crucial for real-world robotic applications, where network conditions can vary, and data integrity or timeliness is critical.

Key QoS policies include:

*   **Reliability**: `BEST_EFFORT` (messages may be lost) or `RELIABLE` (messages are guaranteed to arrive).
*   **Durability**: `VOLATILE` (only new subscribers receive messages) or `TRANSIENT_LOCAL` (new subscribers receive the last published message).
*   **History**: `KEEP_LAST` (keep a specified number of messages) or `KEEP_ALL` (keep all messages).
*   **Liveliness**: `AUTOMATIC` (DDS infrastructure monitors liveliness) or `MANUAL_BY_TOPIC` (publishers assert liveliness).

Choosing appropriate QoS settings ensures that critical data (e.g., motor commands) is delivered reliably, while high-frequency, less critical data (e.g., raw camera frames) can be sent with best-effort, prioritizing throughput.

#### Use cases: Joint angles, IMU streams, camera feeds

*   **Joint Angles**: A `JointState` message containing the current position, velocity, and effort of a robot's joints can be published periodically by a motor controller node.
*   **IMU Streams**: An `Imu` message with orientation, angular velocity, and linear acceleration data can be published by an Inertial Measurement Unit node at a high frequency.
*   **Camera Feeds**: `Image` messages (or `CompressedImage` for bandwidth efficiency) are published by camera driver nodes, providing visual data for perception tasks.

### 2.3 Services

#### Request/response pattern

**Services** in ROS 2 implement a **request/response** communication pattern. Unlike topics, which are asynchronous and one-to-many, services are synchronous and one-to-one. A client node sends a request to a service server node, and the server processes the request and sends back a single response.

Services are ideal for operations that require immediate feedback or a specific action to be performed by another node, where the client needs to wait for the result.

#### When to use services vs topics

*   **Use Topics when**: You need continuous, asynchronous streaming of data (e.g., sensor data, odometry, joint states) to multiple consumers. Order and reliability can be tuned with QoS.
*   **Use Services when**: You need to trigger a specific, discrete action and receive an immediate result. This is for one-shot operations, queries, or configuration changes.

#### Typical examples:

*   **Triggering motion**: A client might request a service `move_robot_to_pose` with a target pose as a request. The service server (e.g., a navigation node) executes the motion and responds with a success/failure status.
*   **Querying robot state**: A client could request a service `get_current_pose` to get the robot's current position and orientation, receiving the `Pose` as a response.
*   **Configuration commands**: A service `set_camera_exposure` could be used to change the exposure settings of a camera, receiving an acknowledgement upon successful configuration.

### 2.4 Actions (optional but relevant)

#### Long-running tasks (navigation, manipulation)

**Actions** are a higher-level communication primitive in ROS 2 designed for **long-running, goal-oriented tasks** that might take a significant amount of time to complete. They extend the request/response pattern of services by providing continuous feedback and the ability to preempt (cancel) a goal.

Actions are particularly relevant for tasks like robot navigation, arm manipulation, or complex motion sequences where an immediate response isn't sufficient, and the client needs to monitor progress or potentially abort the operation.

#### Feedback and result reporting

An Action consists of three primary components:

*   **Goal**: The target state or task to be achieved (e.g., navigate to a specific `Pose`).
*   **Feedback**: Continuous updates on the progress towards the goal (e.g., current pose during navigation, percentage complete).
*   **Result**: The final outcome of the action once it has completed (e.g., `SUCCESS`, `FAILURE`, final path taken).

This structure allows client nodes to send a goal, receive periodic updates on its execution, and ultimately get a final result, making them suitable for complex, asynchronous operations in robotics.
