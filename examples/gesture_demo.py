"""Advanced gesture control demo with custom gestures and dynamic tracking."""

import cv2
import numpy as np
from src.gesture_control import GestureController

def main():
    """Run advanced gesture control demo."""
    # Initialize gesture controller
    controller = GestureController(max_hands=2, trajectory_points=32)
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    # Application state
    state = {
        "recording_gesture": False,
        "custom_gesture_name": "",
        "mode": "normal"  # normal or recording
    }
    
    print("Advanced Gesture Control Demo")
    print("\nStatic Gestures:")
    print("- Open Palm: Next page/item")
    print("- Closed Fist: Previous page/item")
    print("- 1-5 Fingers: Various actions")
    
    print("\nDynamic Gestures:")
    print("- Swipe Left/Right: Pan horizontally")
    print("- Swipe Up/Down: Pan vertically")
    
    print("\nControls:")
    print("- Press 'r' to start/stop recording a custom gesture")
    print("- Press 'n' to name a recorded gesture")
    print("- Press 'q' to quit")
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Failed to read from webcam.")
                break
            
            # Process frame and detect gestures
            gestures, annotated_frame = controller.process_frame(frame)
            
            # Handle keyboard input
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('r'):
                # Toggle gesture recording
                state["recording_gesture"] = not state["recording_gesture"]
                if state["recording_gesture"]:
                    print("Recording gesture... Make a gesture and press 'n' to name it.")
                else:
                    print("Stopped recording.")
            elif key == ord('n') and state["recording_gesture"]:
                # Name and save custom gesture
                name = input("Enter a name for this gesture: ")
                if name:
                    # Get the last detected hand landmarks
                    results = controller.hands.process(
                        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    )
                    if results.multi_hand_landmarks:
                        controller.record_custom_gesture(
                            name,
                            results.multi_hand_landmarks[0]
                        )
                        print(f"Recorded gesture '{name}'")
                    state["recording_gesture"] = False
            
            # Add recording indicator
            if state["recording_gesture"]:
                cv2.putText(
                    annotated_frame,
                    "Recording Gesture...",
                    (10, annotated_frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )
            
            # Show the annotated frame
            cv2.imshow('Advanced Gesture Control Demo', annotated_frame)
                
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        controller.close()

if __name__ == "__main__":
    main()