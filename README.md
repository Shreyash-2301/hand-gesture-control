# Hand Gesture Control Project

A Python-based hand gesture detection and control system using MediaPipe and OpenCV.

## Features

- Real-time hand detection and tracking
- Multiple gesture recognition:
  - Open palm
  - Closed fist
  - Individual finger counting (1-5 fingers)
- Customizable gesture-to-command mapping
- Easy integration with other applications

## Requirements

- Python 3.8+
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

Run the demo script to test gesture detection:

```bash
python examples/gesture_demo.py
```

### Available Gestures

- Open Palm: Detected when all fingers are extended
- Closed Fist: Detected when no fingers are extended
- 1-5 Fingers: Detected based on number of extended fingers

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