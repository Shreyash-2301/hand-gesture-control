# Hand Gesture Control Project

A Python-based hand gesture detection and control system using MediaPipe and OpenCV.

## Features

- Real-time hand detection and tracking
- Multiple Control Modes:
  - Normal Mode:
    - System shortcuts and commands
    - Application control
    - Window management
  - Mouse Control Mode:
    - Cursor movement with index finger
    - Click with thumb-index pinch
  - Volume Control Mode:
    - Adjust system volume with hand gestures
    - Intuitive thumb-pinky distance control
  - Drawing Mode:
    - Virtual air drawing
    - Multiple colors
    - Persistent canvas
- Gesture Recognition:
  - Static gestures:
    - Open palm
    - Closed fist
    - Individual finger counting (1-5 fingers)
  - Dynamic gestures:
    - Swipe Left/Right
    - Swipe Up/Down
  - Custom gesture recording and recognition
- Advanced visualization:
  - Hand landmark tracking
  - Movement trajectories with fade effect
  - Gesture history display
  - Mode status indicator
- Multi-hand support
- System Integration:
  - Customizable shortcuts
  - Application control
  - Volume management
  - Mouse control
- Easy integration with other applications

## Requirements

- Python 3.9+
>>>>>>> 75ac977546de8a460cbb2a12bb696979e26f00f2
- OpenCV
- MediaPipe
- NumPy

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Shreyash-2301/hand-gesture-control.git
   cd hand-gesture-control
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the feature demo script to test all capabilities:

```bash
python examples/feature_demo.py
```

### Control Modes

1. Normal Mode (5 fingers to activate):
   - Open Palm: Spotlight search
   - Closed Fist: Close window
   - 2 Fingers: App switcher
   - 3 Fingers: Minimize window
   - 4 Fingers: Quit application

2. Mouse Control Mode (Pinch gesture to activate):
   - Move index finger to control cursor
   - Pinch (thumb + index) to click

3. Volume Control Mode (Victory gesture to activate):
   - Adjust volume by changing thumb-pinky distance
   - Further apart = louder
   - Closer together = quieter

4. Drawing Mode (ILY gesture to activate):
   - Draw in the air with index finger
   - Press 'c' to change colors
   - Press 'x' to clear canvas

### General Controls
- Press 'q' to quit
- Press 'm' to manually cycle through modes

## Project Structure

```
gesture-control-project/
├── src/
│   └── gesture_control.py     # Main gesture detection module
├── examples/
│   └── gesture_demo.py        # Demo application
├── tests/                     # Unit tests
└── requirements.txt           # Project dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- MediaPipe team for their hand tracking solution
- OpenCV community
python gesture_control.py
```

- Show your hand to the camera
- Try different gestures (open palm, closed fist, or show different numbers of fingers)
- Press 'q' to quit

## Future Enhancements
- Advanced gesture recognition
- Custom gesture mapping
- Application control integration
- Multiple hand tracking improvements
>>>>>>> 75ac977546de8a460cbb2a12bb696979e26f00f2
