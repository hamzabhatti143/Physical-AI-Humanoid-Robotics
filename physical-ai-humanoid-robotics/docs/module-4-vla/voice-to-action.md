---
title: Voice-to-Action using OpenAI Whisper
sidebar_position: 4
description: Implement voice-controlled actions for humanoid robots using OpenAI Whisper for speech-to-text and ROS 2 action mapping.
---

# Voice-to-Action using OpenAI Whisper

Voice control offers an intuitive and natural interface for human-robot interaction. This module explores how to implement a "Voice-to-Action" system for humanoid robots, leveraging OpenAI's Whisper for robust speech-to-text conversion and mapping detected commands to ROS 2 actions.

## OpenAI Whisper Integration

OpenAI Whisper is a general-purpose speech recognition model that can transcribe audio into text. Its high accuracy and multi-language support make it an excellent choice for converting human voice commands into machine-readable text.

### Setting up Whisper

First, you need to install the `openai` Python library and the `whisper` library (which can be installed via pip). You'll also need an OpenAI API key for cloud-based transcription or can use the local `whisper` package for local models.

```bash
pip install openai-whisper openai
```

### Speech-to-Text with Whisper API

To use Whisper via the OpenAI API, you'll typically record audio, save it to a file, and then send it to the API for transcription.

```python
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_filepath):
    with open(audio_filepath, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

if __name__ == "__main__":
    # This assumes you have an audio file named 'command.wav'
    # You would typically record this from a microphone
    audio_file = "command.wav"
    print(f"Transcribing {audio_file}...")
    try:
        text = transcribe_audio(audio_file)
        print(f"Transcription: {text}")
    except Exception as e:
        print(f"Error during transcription: {e}")
```

For local models, the process is similar but uses the `whisper` library directly:

```python
import whisper

def transcribe_local_audio(audio_filepath, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_filepath)
    return result["text"]

if __name__ == "__main__":
    audio_file = "command.wav"
    print(f"Transcribing {audio_file} with local Whisper model...")
    try:
        text = transcribe_local_audio(audio_file)
        print(f"Transcription (local): {text}")
    except Exception as e:
        print(f"Error during local transcription: {e}")
```

## Command Processing

Once you have the transcribed text, the next step is to process it to extract meaningful commands and arguments. This often involves natural language processing (NLP) techniques, from simple keyword matching to more sophisticated intent recognition.

### Simple Keyword Matching

For basic commands, a dictionary of keywords and corresponding actions can be effective.

```python
def process_command(text):
    text = text.lower()
    if "move forward" in text or "go forward" in text:
        return {"action": "move", "direction": "forward", "distance": 1.0}
    elif "turn left" in text:
        return {"action": "turn", "direction": "left", "angle": 90.0}
    elif "stop" in text:
        return {"action": "stop"}
    else:
        return {"action": "unknown"}

if __name__ == "__main__":
    commands = [
        "Robot, move forward one meter",
        "Please turn left",
        "Stop what you are doing",
        "What is the weather like?"
    ]
    for cmd in commands:
        print(f"Processing \"{cmd}\": {process_command(cmd)}")
```

For more complex scenarios, you might use libraries like SpaCy or NLTK for entity extraction or build a custom intent classifier using machine learning.

## ROS 2 Action Mapping

After processing the command, the final step is to map it to a ROS 2 action. ROS 2 actions are a client-server communication type for long-running tasks with feedback. They are ideal for robot movements or complex manipulations that take time to complete.

### Defining a Custom ROS 2 Action

First, you would define a custom action in your ROS 2 package (e.g., `MoveRobot.action` in `your_robot_actions/action`):

```
# Goal
float32 distance
float32 angle
---
# Result
bool success
string message
---
# Feedback
float32 current_distance
float32 current_angle
```

### Interacting with ROS 2 Action Servers

In your voice command processing node, you would act as an action client, sending goals to the robot's action server.

```python
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

# Import your custom action type
from your_robot_actions.action import MoveRobot # Replace with your package and action

class VoiceToActionClient(Node):

    def __init__(self):
        super().__init__('voice_to_action_client')
        self._action_client = ActionClient(self, MoveRobot, 'move_robot')

    def send_goal(self, distance, angle):
        goal_msg = MoveRobot.Goal()
        goal_msg.distance = distance
        goal_msg.angle = angle

        self._action_client.wait_for_server()
        self._send_goal_future = self._action_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result: {result.success}, {result.message}')
        # rclpy.shutdown() # Shutdown if this is the only operation

# Example integration with command processing
# ... (transcription and command processing logic here)

def execute_voice_command(parsed_command, client_node):
    if parsed_command["action"] == "move":
        client_node.send_goal(parsed_command["distance"], 0.0) # Assume 0 angle for forward movement
    elif parsed_command["action"] == "turn":
        client_node.send_goal(0.0, parsed_command["angle"])
    elif parsed_command["action"] == "stop":
        # Implement a cancel goal or a specific stop action
        pass

if __name__ == '__main__':
    rclpy.init()
    action_client_node = VoiceToActionClient()

    # Simulate a transcribed and parsed command
    sample_command = {"action": "move", "direction": "forward", "distance": 1.0}
    execute_voice_command(sample_command, action_client_node)

    rclpy.spin(action_client_node)

    action_client_node.destroy_node()
    rclpy.shutdown()
```

## Conclusion

Implementing Voice-to-Action for humanoid robots combines state-of-the-art speech recognition with robust robotic control frameworks. OpenAI Whisper provides a powerful foundation for accurate speech-to-text, which can then be processed and mapped to ROS 2 actions for executing complex robot behaviors. This approach significantly enhances the naturalness and efficiency of human-robot interaction, paving the way for more intuitive control systems in physical AI applications.
