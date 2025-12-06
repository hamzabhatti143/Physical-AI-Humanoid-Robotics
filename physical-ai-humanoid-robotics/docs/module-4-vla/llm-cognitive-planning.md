---
title: "Cognitive Planning with LLMs"
---

## 4.3 Cognitive Planning with LLMs

One of the most profound impacts of Large Language Models (LLMs) in robotics is their ability to enable **cognitive planning**. This means robots can go beyond merely executing pre-programmed actions to understanding abstract human goals, decomposing them into manageable sub-tasks, and generating adaptable action plans. This section explores how LLMs facilitate this higher-level reasoning for robotic systems.

### 4.3.1 From Natural Language to High-Level Tasks

#### LLM interpretation of human intent

At the core of cognitive planning is the LLM's ability to interpret ambiguous or high-level human instructions. Given a natural language prompt like "clean the kitchen" or "prepare for guests," an LLM can:

*   **Extract Core Intent**: Identify the primary goal the human wishes to achieve.
*   **Infer Context**: Draw upon its vast pre-training knowledge to understand what "cleaning" or "preparing for guests" typically entails in a household setting.
*   **Clarify Ambiguity**: If the command is unclear (e.g., "move that thing"), the LLM can generate clarifying questions to resolve ambiguity, potentially leveraging visual cues.

This deep semantic understanding allows robots to receive instructions in a human-centric way, rather than requiring precise, machine-readable commands.

#### Breaking down goals (“Clean the room”) into sub-tasks

Once human intent is understood, LLMs excel at **task decomposition**. A high-level goal like "clean the room" is too abstract for a robot to execute directly. An LLM can break this down into a sequence of concrete, actionable sub-tasks:

1.  Identify misplaced items.
2.  Pick up item A and place it in location X.
3.  Pick up item B and place it in location Y.
4.  Vacuum the floor.
5.  Wipe down surfaces.

This hierarchical breakdown allows a robot to systematically approach complex tasks, even those it hasn't been explicitly programmed for.

### 4.3.2 Generating Action Plans for ROS 2

After task decomposition, the LLM needs to translate these cognitive steps into executable commands for the robot's control system, typically within a ROS 2 framework.

#### Mapping LLM output to ROS 2 action servers

LLM-generated sub-tasks are mapped to existing **ROS 2 action servers**. For example:

*   `Pick up item A` → Call the `pick_and_place` action server with target `item_A` and destination `location_X`.
*   `Vacuum the floor` → Call the `navigate_to` action server for the vacuuming path and then a `start_vacuum` service.

The LLM acts as a high-level sequencer, orchestrating calls to these modular robotic capabilities.

#### Task → Behavior Tree conversion

For more complex and reactive robot behaviors, the LLM's plan can be converted into or guide the generation of a **Behavior Tree (BT)**. Behavior trees are a powerful way to represent robot control logic, allowing for sequential actions, conditional execution, and robust error handling. The LLM can specify the desired sequence of actions and conditions, which are then translated into BT nodes and edges.

#### Safety constraints and guardrails

While LLMs are powerful, they can sometimes generate unsafe or impractical plans. Therefore, it is crucial to implement **safety constraints and guardrails**:

*   **Constraint Checking**: Before executing any LLM-generated action, a separate safety module checks for physical limits, collision risks, and adherence to predefined safety protocols.
*   **Human Oversight**: In critical applications, a human operator can review and approve LLM-generated plans.
*   **Fallback Mechanisms**: If an LLM plan fails or leads to an unsafe state, the robot should revert to a safe, pre-programmed behavior or pause and request human intervention.
*   **Environment Model**: The LLM's planning should be grounded in an accurate model of the robot's current environment, ensuring plans are physically feasible.

#### Maintaining robot context and memory

For effective cognitive planning, the LLM needs to maintain a persistent understanding of the robot's state and history:

*   **Environmental State**: Knowledge of object locations, previously visited areas, and changes in the environment.
*   **Task Progress**: Which sub-tasks have been completed, which are pending, and any failures encountered.
*   **Dialog History**: The ongoing conversation with the human user.

This context can be fed back to the LLM (e.g., through a "long-term memory" module) to inform future planning decisions, allowing for more coherent and adaptable behavior.

### 4.3.3 Multi-Modal Planning

#### Incorporating vision context into LLM prompts

To enhance planning, LLMs must integrate visual information directly. This is achieved through **multi-modal prompts**, where visual observations (e.g., descriptions of objects, scene graphs, or even raw image embeddings) are provided alongside natural language instructions. For example, an LLM might receive:

"The user said: 'Put the blue cup on the table'. Current scene contains: a red mug (ID 123, location X), a blue cup (ID 456, location Y), a table (ID 789, location Z)."

The LLM can then use this combined input to generate a more precise plan.

#### Handling ambiguity (“the cup on the left”)

Visual context is crucial for resolving linguistic ambiguities. If a human says, "pick up the cup," and there are multiple cups, the robot can use visual information to ask a clarifying question ("which cup?") or, if the command is refined with a visual cue ("the cup on the left"), the VLM (Vision-Language Model) component helps ground this reference to a specific object in the scene.

This integration allows LLMs to create plans that are not just cognitively sound but also perceptually grounded and robust to real-world complexities.
