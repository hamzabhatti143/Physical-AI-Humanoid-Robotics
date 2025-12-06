# Quickstart Guide: Physical AI & Humanoid Robotics Book

**Feature Branch**: `1-docusaurus-book-platform` | **Date**: 2025-12-04 | **Spec**: specs/1-docusaurus-book-platform/spec.md
**Input**: Docusaurus implementation plan.

## Summary

This quickstart guide provides essential information to get started with the "Physical AI & Humanoid Robotics" book, which is built using Docusaurus 3.x. It covers the target audience, technical recommendations, and how to set up the development environment.

## Target Audience

This book is designed for:

*   **AI/ML Engineers**: Looking to transition their digital AI skills to physical robotics.
*   **Robotics Enthusiasts**: Interested in understanding how modern AI (especially LLMs) integrates with robotic systems.
*   **Students/Researchers**: In the fields of AI, Robotics, Computer Science, and Engineering, seeking a comprehensive guide to embodied intelligence.

**Prerequisites**: A basic understanding of Python programming and fundamental AI/ML concepts is recommended.

## Technical Recommendations

To get the most out of this book and its code examples, the following are recommended:

*   **Operating System**: Linux (Ubuntu 20.04+ recommended) is ideal for ROS 2 and NVIDIA Isaac development. Windows Subsystem for Linux (WSL2) can be used on Windows.
*   **Python**: Version 3.8+ (for ROS 2 and `rclpy` compatibility).
*   **Node.js**: Version 18+ and `npm` (for Docusaurus development).
*   **Docker**: For containerized development environments, especially for ROS 2 and NVIDIA Isaac components.
*   **NVIDIA GPU**: Highly recommended for working with NVIDIA Isaac Sim/ROS, and for accelerating AI workloads. Ensure up-to-date drivers.

## Getting Started with Development

To set up your local development environment for the Docusaurus book, follow these steps:

1.  **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd physical-ai-humanoid-robotics
    ```

2.  **Install Node.js Dependencies**:
    Navigate to the `physical-ai-humanoid-robotics/` directory and install the Docusaurus dependencies:
    ```bash
    npm install
    ```

3.  **Start the Docusaurus Development Server**:
    To view the book locally, run the Docusaurus development server:
    ```bash
    npm run start
    ```
    This will open a browser window at `http://localhost:3000` (or another available port).

4.  **Explore the Content**: Browse through the modules and weeks in the sidebar navigation. You can edit MDX files in the `docs/` directory, and changes will hot-reload in your browser.

5.  **Build the Static Site**:
    To generate a production-ready static build of the book:
    ```bash
    npm run build
    ```
    The static files will be generated in the `build/` directory.

## Next Steps

*   Begin by exploring the `docs/intro.md` for an overview of Physical AI.
*   Dive into `docs/module-1-ros2/index.md` to start with ROS 2 fundamentals.
*   Refer to the `tasks.md` file for detailed implementation steps and contribution guidelines.
