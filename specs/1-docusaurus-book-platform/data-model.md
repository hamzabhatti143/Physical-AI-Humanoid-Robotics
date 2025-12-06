# Data Model: Physical AI & Humanoid Robotics Book Content Structure

**Feature Branch**: `1-docusaurus-book-platform` | **Date**: 2025-12-04 | **Spec**: specs/1-docusaurus-book-platform/spec.md
**Input**: `specs/1-docusaurus-book-platform/spec.md`, `specs/1-docusaurus-book-platform/plan.md`

## Summary

This document outlines the data model for the "Physical AI & Humanoid Robotics" book content, specifically tailored for a Docusaurus 3.x implementation. It defines the hierarchical structure, content attributes, and relationships between different parts of the book, mapping directly to MDX files and Docusaurus navigation concepts.

## Entities

### Book
-   **ID**: Unique identifier (implicit from Docusaurus path).
-   **Title**: "Physical AI & Humanoid Robotics"
-   **Tagline**: "Bridging the gap between digital brain and physical body"
-   **Format**: MDX (Markdown + JSX) with frontmatter.
-   **Structure**: Composed of `Modules`, `Introduction`, and `Learning Outcomes`.

### Module
-   **ID**: Unique identifier (e.g., `module-1-ros2`).
-   **Title**: Display title for the module (e.g., "Module 1: The Robotic Nervous System (ROS 2) - Weeks 3-5").
-   **Description**: Brief summary of the module's content.
-   **Path**: File system path (e.g., `docs/module-1-ros2/`).
-   **Content**: A collection of `WeekContent` files.
-   **Category File**: `_category_.json` for Docusaurus sidebar configuration.

### WeekContent
-   **ID**: Unique identifier (e.g., `week-3-fundamentals.md`).
-   **Title**: Page title, displayed in navigation and page header.
-   **Sidebar Position**: Numerical order for display within a module's sidebar.
-   **Description**: Short description for SEO and navigation previews.
-   **Path**: File system path (e.g., `docs/module-1-ros2/week-3-fundamentals.md`).
-   **Content Body**: MDX content, including text, Python code blocks, and Mermaid diagrams.

### LearningOutcome
-   **Description**: Text describing what the student will learn (e.g., "Master ROS 2 for robotic control").
-   **Reference**: Associated with `docs/learning-outcomes.md`.

### CodeExample
-   **Language**: `Python` (specifically `rclpy`).
-   **Content**: Python code snippets.
-   **Highlighting**: Docusaurus-supported syntax highlighting.
-   **Integration**: Embedded directly within `WeekContent` MDX files.

### Diagram
-   **Type**: `Mermaid`.
-   **Content**: Mermaid markdown syntax.
-   **Integration**: Embedded directly within `WeekContent` MDX files.

## Content Hierarchy (File Structure Mapping)

The Docusaurus `docs/` directory will represent the main content hierarchy:

```text
physical-ai-humanoid-robotics/
├── docs/
│   ├── intro.md                # Quarter Overview + Why Physical AI Matters (Weeks 1-2)
│   │   # Frontmatter: title, sidebar_position: 1, description
│   │
│   ├── module-1-ros2/          # Module 1 (Weeks 3-5)
│   │   ├── _category_.json     # { label: "Module 1: The Robotic Nervous System (ROS 2) - Weeks 3-5", position: 2 }
│   │   ├── index.md            # Module 1 Overview
│   │   │   # Frontmatter: title, sidebar_position: 1, description
│   │   ├── week-3-fundamentals.md # Frontmatter: title, sidebar_position: 2, description
│   │   ├── week-4-nodes-topics.md # Frontmatter: title, sidebar_position: 3, description
│   │   ├── week-5-python-rclpy.md # Frontmatter: title, sidebar_position: 4, description
│   │   └── urdf-humanoids.md      # Frontmatter: title, sidebar_position: 5, description
│   │
│   ├── module-2-digital-twin/  # Module 2 (Weeks 6-7)
│   │   ├── _category_.json     # { label: "Module 2: The Digital Twin (Gazebo & Unity) - Weeks 6-7", position: 3 }
│   │   ├── index.md            # Module 2 Overview
│   │   ├── week-6-gazebo-intro.md
│   │   ├── week-7-unity-renderig.md
│   │   └── sensor-simulation.md
│   │
│   ├── module-3-nvidia-isaac/  # Module 3 (Weeks 8-10)
│   │   ├── _category_.json     # { label: "Module 3: The AI-Robot Brain (NVIDIA Isaac) - Weeks 8-10", position: 4 }
│   │   ├── index.md            # Module 3 Overview
│   │   ├── week-8-isaac-intro.md
│   │   ├── week-9-isaac-sim.md
│   │   ├── week-10-isaac-ros.md
│   │   └── nav2-planning.md
│   │
│   ├── module-4-vla/           # Module 4 (Weeks 11-13)
│   │   ├── _category_.json     # { label: "Module 4: Vision-Language-Action (VLA) - Weeks 11-13", position: 5 }
│   │   ├── index.md            # Module 4 Overview
│   │   ├── week-11-vla-intro.md
│   │   ├── week-12-humanoid-dev.md
│   │   ├── week-13-conversational.md
│   │   ├── voice-to-action.md
│   │   ├── llm-cognitive-planning.md
│   │   └── capstone-project.md
│   │
│   └── learning-outcomes.md    # Consolidated Learning Outcomes
│       # Frontmatter: title, sidebar_position: 6, description
```

## Relationships

-   **Book** has-many **Modules**.
-   **Module** has-many **WeekContent**.
-   **Book** has-one **Introduction** (`intro.md`).
-   **Book** has-one **Learning Outcomes** (`learning-outcomes.md`).
-   **WeekContent** may contain **CodeExamples** and **Diagrams**.
-   **Module** contains a `_category_.json` file for Docusaurus sidebar organization.
