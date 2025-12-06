# Data Model: Physical AI & Humanoid Robotics Book Content Structure

This document outlines the conceptual data model for the book's content, detailing its modular and hierarchical organization as defined in the feature specification and planning input.

## Key Entities

### Book
-   **Title**: "Physical AI & Humanoid Robotics"
-   **Overview**: Introduction to Physical AI, transition from digital to embodied intelligence, why humanoids excel.
-   **Duration**: 13 weeks (quarter-long course).
-   **Format**: MDX (Markdown + JSX) with frontmatter.

### Module
-   **ID**: `module-1-ros2`, `module-2-digital-twin`, `module-3-nvidia-isaac`, `module-4-vla`
-   **Name**: E.g., "The Robotic Nervous System (ROS 2)", "The Digital Twin (Gazebo & Unity)", etc.
-   **Contents**: Module introduction (`index.md`), weekly concepts, weekly hands-on exercises, code examples, diagrams, summary (implicit in weekly content).
-   **Relationships**: Contains multiple `Week` entities.

### Week
-   **ID**: `week-X-concepts.md`, `week-X-hands-on.md`, etc.
-   **Concepts**: Theoretical content for the week.
-   **Hands-on**: Practical exercises and tutorials for the week.
-   **Relationships**: Belongs to a `Module` (or Introduction/Capstone).

### Chapter/Section (within Week/Module)
-   **Type**: Concepts (`week-X-concepts.md`), Hands-on (`week-X-hands-on.md`), Module Index (`index.md`).
-   **Content**: MDX text, code snippets (Python/rclpy), Mermaid diagrams.
-   **Relationships**: Part of a `Week` or `Module`.

### Code Example
-   **Language**: Python (`rclpy` for ROS 2).
-   **Purpose**: Illustrate concepts, provide practical implementations.
-   **Location**: `static/code-examples/` or specific module directories.

### Diagram
-   **Format**: Mermaid.
-   **Purpose**: Visualize architecture, flows, relationships.
-   **Location**: Embedded directly in MDX or linked from `static/img/`.

### Capstone Project
-   **Title**: "The Autonomous Humanoid"
-   **Description**: Final project integrating voice command, path planning, navigation, object identification, and manipulation.
-   **Location**: `docs/module-4-vla/capstone-project.md`

### Learning Outcome
-   **ID**: `1` through `6`
-   **Description**: Measurable knowledge/skill student gains.
-   **Relationships**: Associated with overall `Book` and implicitly covered across `Modules`.
-   **Location**: `docs/learning-outcomes.md`

### Reference
-   **Content**: Links to resources, further reading.
-   **Location**: Integrated within relevant MDX files or a dedicated `references.md` if needed.

## Content Hierarchy (File Structure Mapping)

```text
physical-ai-humanoid-robotics/
├── docs/
│   ├── intro.md                # Quarter Overview + Why Physical AI Matters (Weeks 1-2)
│   ├── module-1-ros2/          # The Robotic Nervous System (ROS 2)
│   │   ├── _category_.json
│   │   ├── index.md            # Module 1 introduction and objectives
│   │   ├── week-3-fundamentals.md  # ROS 2 Fundamentals: Architecture and core concepts
│   │   ├── week-4-nodes-topics.md  # ROS 2: Nodes, topics, services, actions
│   │   ├── week-5-python-rclpy.md  # ROS 2: Building packages with Python, launch files and parameters
│   │   └── urdf-humanoids.md   # Understanding URDF (Unified Robot Description Format) for humanoids
│   ├── module-2-digital-twin/  # Gazebo & Unity
│   │   ├── _category_.json
│   │   ├── index.md            # Module 2 introduction and objectives
│   │   ├── week-6-gazebo-intro.md # Robot Simulation with Gazebo: Environment setup, URDF/SDF formats, Physics and sensor simulation
│   │   ├── week-7-unity-renderig.md # Unity integration and high-fidelity rendering
│   │   └── sensor-simulation.md # Simulating sensors (LiDAR, Depth Cameras, and IMUs)
│   ├── module-3-nvidia-isaac/  # The AI-Robot Brain (NVIDIA Isaac™)
│   │   ├── _category_.json
│   │   ├── index.md            # Module 3 introduction and objectives
│   │   ├── week-8-isaac-intro.md # Isaac SDK and Isaac Sim: Photorealistic simulation and synthetic data generation
│   │   ├── week-9-isaac-sim.md # AI-powered perception
│   │   ├── week-10-isaac-ros.md # Isaac ROS: Hardware-accelerated VSLAM and navigation
│   │   └── nav2-planning.md    # Nav2: Path planning for bipedal humanoid movement
│   ├── module-4-vla/           # Vision-Language-Action (VLA)
│   │   ├── _category_.json
│   │   ├── index.md            # Module 4 introduction and objectives
│   │   ├── week-11-vla-intro.md # Humanoid Robot Development: Kinematics and dynamics, Bipedal locomotion and manipulation
│   │   ├── week-12-humanoid-dev.md # Natural HRI design and GPT integration, Speech recognition and NLU
│   │   ├── week-13-conversational.md # Multi-modal interaction and cognitive planning (LLMs to ROS 2 actions)
│   │   ├── voice-to-action.md  # Voice-to-Action: Using OpenAI Whisper for voice commands
│   │   ├── llm-cognitive-planning.md # Cognitive Planning: Using LLMs to translate natural language commands into ROS 2 actions
│   │   └── capstone-project.md # Capstone Project: The Autonomous Humanoid
│   └── learning-outcomes.md    # Learning Outcomes (Assessment and outcomes)
├── src/
│   ├── css/
│   │   └── custom.css
│   └── pages/
│       └── index.js
├── static/
│   ├── img/
│   └── code-examples/          # Root level for general code examples if any
├── docusaurus.config.js
├── sidebars.js
├── package.json
└── README.md
```
