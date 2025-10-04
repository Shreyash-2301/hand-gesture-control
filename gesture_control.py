import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_draw = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    """Count number of fingers held up"""
    finger_tips = [8, 12, 16, 20]  # Index for finger tips (except thumb)
    thumb_tip = 4
    count = 0
    
    # Check thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        count += 1
    
    # Check other fingers
    for tip in finger_tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            count += 1
            
    return count

def detect_gesture(hand_landmarks):
    """Detect basic hand gestures"""
    fingers_up = count_fingers(hand_landmarks)
    
    if fingers_up == 0:
        return "Closed Fist"
    elif fingers_up == 5:
        return "Open Palm"
    else:
        return f"{fingers_up} Fingers"

# Start video capture
cap = cv2.VideoCapture(0)

print("Gesture Control Started! Press 'q' to quit.")
print("Try showing different numbers of fingers or open/closed palm.")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Failed to read from webcam.")
        break
        
    # Flip the image horizontally for a later selfie-view display
    image = cv2.flip(image, 1)
    
    # Convert BGR image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and detect hands
    results = hands.process(rgb_image)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks
            mp_draw.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
            
            # Detect gesture
            gesture = detect_gesture(hand_landmarks)
            
            # Display gesture text
            cv2.putText(
                image,
                gesture,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
    
    # Display the image
    cv2.imshow('Gesture Control', image)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
hands.close()