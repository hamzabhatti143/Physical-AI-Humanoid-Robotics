// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  tutorialSidebar: [
    'intro', // Quarter Overview + Why Physical AI Matters
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2) - Weeks 3-5',
      link: {
        type: 'doc',
        id: 'module-1-ros2/index', // Points to the index.md of the module
      },
      items: [
        'module-1-ros2/week-3-fundamentals',
        'module-1-ros2/week-4-nodes-topics',
        'module-1-ros2/week-5-python-rclpy', //hamza
        'module-1-ros2/urdf-humanoids',     //hamza
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity) - Weeks 6-7',
      link: {
        type: 'doc',
        id: 'module-2-digital-twin/index',
      },
      items: [
        'module-2-digital-twin/week-6-gazebo-intro',
        'module-2-digital-twin/week-7-unity-rendering',  ///hamza
        'module-2-digital-twin/sensor-simulation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac) - Weeks 8-10',
      link: {
        type: 'doc',
        id: 'module-3-nvidia-isaac/index',
      },
      items: [
        'module-3-nvidia-isaac/week-8-isaac-intro',
        'module-3-nvidia-isaac/week-9-isaac-sim',
        'module-3-nvidia-isaac/week-10-isaac-ros',
        'module-3-nvidia-isaac/nav2-planning',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA) - Weeks 11-13',
      link: {
        type: 'doc',
        id: 'module-4-vla/index',
      },
      items: [
        'module-4-vla/week-11-vla-intro',
        'module-4-vla/week-12-humanoid-dev',
        'module-4-vla/week-13-conversational',
        'module-4-vla/voice-to-action',              ///hamza 
        'module-4-vla/llm-cognitive-planning',
        'module-4-vla/capstone-project',
      ],
    },
    'learning-outcomes',
  ],
};

export default sidebars;
