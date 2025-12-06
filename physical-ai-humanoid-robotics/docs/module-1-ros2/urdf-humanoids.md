---
title: Understanding URDF for Humanoid Robots
sidebar_position: 4
description: A deep dive into using URDF (Unified Robot Description Format) to model humanoid robots in ROS 2 environments.
---

# Understanding URDF for Humanoid Robots

URDF (Unified Robot Description Format) is an XML format used in ROS 2 to describe all aspects of a robot. It allows you to model the robot's kinematics (links and joints), visual properties (geometry, color, texture), and collision properties. For humanoid robots, a well-structured URDF is crucial for simulation, motion planning, and visualization.

## URDF Structure Basics

A URDF file is essentially a tree of `link` and `joint` elements. A `link` represents a rigid body (e.g., a torso, an arm, a leg), and a `joint` connects two links, defining their relative motion.

### The `<robot>` Tag

Every URDF file starts with a `<robot>` tag, which gives the robot a name.

```xml
<robot name="my_humanoid">
  <!-- Robot description goes here -->
</robot>
```

### `<link>` Element

A `link` element describes the physical and visual properties of a robot segment. It includes:
- `<visual>`: Defines how the link appears (geometry, material).
- `<collision>`: Defines the link's collision properties (geometry).
- `<inertial>`: Defines the link's mass, center of mass, and inertia tensor, critical for physics simulation.

Example of a simple humanoid link (e.g., a torso):

```xml
<link name="torso">
  <visual>
    <geometry>
      <box size="0.2 0.4 0.6" />
    </geometry>
    <material name="blue">
      <color rgba="0 0 0.8 1" />
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.2 0.4 0.6" />
    </geometry>
  </collision>
  <inertial>
    <mass value="10.0" />
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0" />
  </inertial>
</link>
```

### `<joint>` Element

A `joint` element connects a parent link to a child link and defines the type of motion allowed between them. Key attributes include:
- `name`: Unique name for the joint.
- `type`: Type of joint (e.g., `revolute`, `continuous`, `prismatic`, `fixed`). Humanoids typically use `revolute` for rotational joints (like shoulders, elbows) and `fixed` for rigid connections.
- `<parent>` and `<child>`: Specify the connected links.
- `<origin>`: Defines the joint's position and orientation relative to the parent link.
- `<axis>`: For revolute/prismatic joints, defines the axis of motion.
- `<limit>`: Defines the joint's range of motion and velocity/effort limits.

Example of a humanoid shoulder joint:

```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.1 0.2 0.5" rpy="0 0 0"/>
  <axis xyz="1 0 0"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1.0"/>
</joint>
```

## Joints, Links, and Sensors for Humanoids

Building a URDF for a humanoid involves carefully defining all its segments and their interconnections.

### Common Humanoid Links

Humanoid robots typically include a complex hierarchy of links:
- **Base/Torso**: The central part of the robot.
- **Head**: Connected to the torso via a neck joint.
- **Arms**: Composed of upper arm, forearm, and hand links, connected by shoulder, elbow, and wrist joints.
- **Legs**: Composed of thigh, shin, and foot links, connected by hip, knee, and ankle joints.
- **End Effectors**: Grippers or specialized tools if applicable.

### Common Humanoid Joints

- **Revolute Joints**: Most common for humanoids, allowing rotation around a single axis (e.g., elbow, knee, hip, shoulder).
- **Fixed Joints**: Used for rigid connections where no relative motion is intended (e.g., connecting a camera to a head link).
- **Continuous Joints**: Revolute joints without limits (e.g., a wheel that can spin infinitely, though less common for primary humanoid joints).

### Integrating Sensors

Sensors are critical for humanoids to perceive their environment and their own state. In URDF, sensors are typically represented as `link` elements (often small, fixed links) and then referenced in simulation environments or through ROS 2 components.

Common sensors for humanoids include:
- **Cameras**: For vision and object detection.
  ```xml
  <link name="camera_link">
    <visual>
      <geometry><box size="0.02 0.05 0.02" /></geometry>
    </visual>
  </link>
  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0.05" rpy="0 1.5707 0"/>
  </joint>
  ```
- **IMUs (Inertial Measurement Units)**: For orientation, angular velocity, and acceleration.
- **Force/Torque Sensors**: At joints or end effectors for interaction control.
- **Lidars/Depth Sensors**: For environmental mapping and obstacle avoidance.

These sensors are often added as new links connected by `fixed` joints to a relevant parent link (e.g., a camera to the head, an IMU to the torso). Their actual data publication is handled by ROS 2 drivers and simulation plugins, not directly within the URDF.

## Best Practices for Humanoid URDFs

- **Modularity**: Break down the robot into logical components (e.g., `_macro.xacro` files for arms, legs, etc.) using XACRO (XML Macros for URDF) for easier management and reuse.
- **Consistent Naming**: Use clear and consistent naming conventions for links and joints.
- **Origin Placement**: Carefully define `<origin>` tags to ensure correct assembly and joint axes.
- **Collision Geometry**: Simplify collision geometries where possible to reduce simulation computational load, but ensure they accurately represent the robot's physical extent.
- **Visualization**: Use accurate meshes (`.dae`, `.stl`) for visual representation rather than simple geometric primitives where detail is important.

## Conclusion

URDF is a powerful tool for describing the physical and kinematic properties of humanoid robots within the ROS 2 ecosystem. By understanding how to define links, joints, and integrate sensors, you can create accurate and functional robot models essential for simulation, control, and visualization. Mastering URDF is a foundational step in developing advanced humanoid robotics applications. The next steps would typically involve integrating this URDF with a simulation environment like Gazebo or a real robot.