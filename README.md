# Syntecxhub Hand Gesture Recognition

A real-time hand gesture recognition demo built with Python, OpenCV and MediaPipe.
It detects hand landmarks from the webcam, recognizes simple gestures, and maps
them to media actions. Built as part of the Syntecxhub AI Internship (Task 3, Project 2).

## Features
- Real-time hand landmark detection (21 points) using MediaPipe Hand Landmarker
- Gesture classification: Thumbs Up, Fist, Open Palm
- Gestures mapped to actions (demo):
  - Thumbs Up: volume up
  - Open Palm: volume down
  - Fist: play / pause
- Actions are OFF by default for safety (press `A` to turn them on or off)
- Runs on a normal laptop CPU, no GPU or model training needed

## How it works
1. OpenCV reads frames from the webcam.
2. MediaPipe finds 21 landmarks on the hand.
3. Simple rules check which fingers are up (finger tip above its middle joint).
   The thumb is checked against the knuckles, scaled by hand size.
4. A gesture must stay the same for 5 frames before an action runs, to avoid flicker.
5. `pyautogui` presses the media key for the gesture.

## Setup
1. Install Python 3.9 or newer.
2. Create and activate a virtual environment (optional but recommended).
3. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
4. Keep the MediaPipe hand model `hand_landmarker.task` in the project folder
   (it is included in this repo). If it is missing, download it from:
   ```
   https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
   ```

## Run
```
python main.py
```

## Controls
| Key | What it does |
|---|---|
| `A` | Turn actions ON / OFF |
| `Q` | Quit |

## Tips
- Use good light and keep your hand upright, about 30 to 50 cm from the camera.
- If thumbs up is not detected, lower `THUMB_MARGIN` in `main.py`. If a fist is
  detected as thumbs up, raise it.

## Privacy
The program does not save any image or video and does not use the internet
while running. Frames are processed only in memory.

## Author
Alishba