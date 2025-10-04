"""Example script demonstrating gesture control."""

import cv2
from gesture_control import GestureController

def main():
    """Run gesture control demo."""
    # Initialize gesture controller
    controller = GestureController()
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    print("Gesture Control Started! Press 'q' to quit.")
    print("Available Gestures:")
    print("- Open Palm")
    print("- Closed Fist")
    print("- 1-5 Fingers")
    
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Failed to read from webcam.")
                break
            
            # Process frame and detect gestures
            gesture, annotated_frame = controller.process_frame(frame)
            
            # Display the annotated frame
            cv2.imshow('Gesture Control Demo', annotated_frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    finally:
        # Release resources
        cap.release()
        cv2.destroyAllWindows()
        controller.close()

if __name__ == "__main__":
    main()