# 🕷️ Spidey Keyboard

A gesture-controlled air keyboard using a webcam, MediaPipe hand tracking, OpenCV, and PyAutoGUI.

## Features

- Webcam-based hand tracking
- Index finger controls the virtual cursor
- Thumb + index finger pinch presses a key
- Visible QWERTY keyboard overlay
- Hover and press feedback
- SPACE, BACKSPACE, and ENTER support
- Typed text preview
- Sends key presses to the currently focused application

## Run

```powershell
python -m pip install -r requirements.txt
python app.py
```

On first run, the MediaPipe hand model is downloaded automatically.

## How to use

1. Run `python app.py`.
2. Show your hand to the webcam.
3. Move your index finger over a key.
4. Pinch your thumb and index finger together.
5. The selected key is typed into the focused application.

To type into Notepad, VS Code, Chrome, etc., focus that application while the air keyboard is running.

## Controls

- **INDEX** → move
- **PINCH** → press
- **Q** → quit

## Tech Stack

Python · OpenCV · MediaPipe · PyAutoGUI
