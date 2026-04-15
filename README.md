# Virtual Air Keyboard (Gesture-Based Typing)

This project is a virtual keyboard that lets you type in the air using hand gestures. It uses your webcam to detect your hand and allows you to select keys by hovering your finger over them.

The goal of this project was to explore real-time computer vision and build something interactive and practical using Python.

## What it does

- Tracks your hand using MediaPipe
- Uses your index finger as a pointer
- Lets you type by hovering over keys (no physical keyboard needed)
- Displays typed text on the screen in real time

## Features

- Smooth and responsive hand tracking
- Hover-based typing (no unreliable clicking needed)
- Clean keyboard UI with custom color theme
- Includes:
  - Alphabets (A–Z)
  - Space key
  - Backspace (`BACK`)
  - Delete (`DEL`)
- Multi-line text display with automatic wrapping
- Blinking cursor that shows typing position
- Layout fits properly within the screen

## How it works

The webcam captures your hand movement and MediaPipe detects hand landmarks.

- The tip of your index finger acts like a cursor
- When you hover over a key for a short duration (~0.6 seconds), that key is selected
- The selected character is added to the text display

This “hover + hold” approach makes the typing much more stable compared to gesture clicking.

## Technologies used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI

## How to run the project

1. Make sure Python is installed (preferably Python 3.10)

2. Install required libraries: pip install -r requirements.txt

3. Run the program: python virtual_keyboard.py


## Controls

- Move your index finger to navigate over keys
- Hold your finger over a key for a moment to type
- `BACK` → deletes last character  
- `DEL` → clears entire text  
- `SPACE` → adds space  
- Press `ESC` to exit the program  

## Project structure

Virtual_keyboard/
│
├── virtual_keyboard.py
├── requirements.txt
├── README.md
