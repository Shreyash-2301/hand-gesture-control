"""Advanced gesture control demo with system interaction features."""

import cv2
import numpy as np
from src.gesture_control import GestureController
from src.gesture_features import GestureFeatures

def main():
    """Run advanced gesture control demo with features."""
    # Initialize controllers
    controller = GestureController(max_hands=2, trajectory_points=32)
    features = GestureFeatures()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    print("Advanced Gesture Control Demo with Features")
    print("\nControl Modes:")
    print("1. Normal Mode (5 fingers)")
    print("   - Open Palm: Spotlight search")
    print("   - Closed Fist: Close window")
    print("   - 2 Fingers: App switcher")
    print("   - 3 Fingers: Minimize window")
    print("   - 4 Fingers: Quit application")
    
    print("\n2. Mouse Control Mode (Pinch gesture)")
    print("   - Move index finger: Move cursor")
    print("   - Pinch (thumb + index): Click")
    
    print("\n3. Volume Control Mode (Victory gesture)")
    print("   - Thumb-pinky distance controls volume")
    
    print("\n4. Drawing Mode (ILY gesture)")
    print("   - Index finger up: Draw")
    print("   - Change color: Press 'c'")
    print("   - Clear canvas: Press 'x'")
    
    print("\nGeneral Controls:")
    print("- Press 'q' to quit")
    print("- Press 'm' to cycle through modes")
    
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
            elif key == ord('m'):
                # Cycle through modes
                modes = ["normal", "mouse", "volume", "drawing"]
                current_index = modes.index(features.current_mode)
                features.current_mode = modes[(current_index + 1) % len(modes)]
            elif key == ord('c') and features.current_mode == "drawing":
                features.change_drawing_color()
            elif key == ord('x') and features.current_mode == "drawing":
                features.clear_drawing()
            
            # Process detected gestures
            if gestures:
                # Check for mode switch gestures
                features.handle_mode_switch(gestures[0])
                
                # Process gestures based on current mode
                results = controller.hands.process(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                )
                
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    
                    if features.current_mode == "normal":
                        features.handle_shortcuts(gestures[0])
                    elif features.current_mode == "mouse":
                        features.handle_mouse_control(
                            hand_landmarks,
                            (frame.shape[1], frame.shape[0])
                        )
                    elif features.current_mode == "volume":
                        features.handle_volume_control(hand_landmarks)
                    elif features.current_mode == "drawing":
                        annotated_frame = features.handle_drawing(
                            hand_landmarks,
                            annotated_frame
                        )
            
            # Add mode indicator
            cv2.putText(
                annotated_frame,
                f"Mode: {features.current_mode.capitalize()}",
                (10, annotated_frame.shape[0] - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            # Show the frame
            cv2.imshow('Advanced Gesture Control', annotated_frame)
                
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        controller.close()

if __name__ == "__main__":
    main()