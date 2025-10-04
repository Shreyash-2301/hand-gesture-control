"""Gesture detection and control module using MediaPipe."""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Dict, Any, Optional

class GestureController:
    """Handles hand gesture detection and interpretation."""
    
    def __init__(self):
        """Initialize MediaPipe hand detection."""
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def count_fingers(self, hand_landmarks) -> int:
        """
        Count number of fingers held up.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            int: Number of fingers detected as being held up
        """
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
    
    def detect_gesture(self, hand_landmarks) -> str:
        """
        Detect basic hand gestures.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            str: Detected gesture name
        """
        fingers_up = self.count_fingers(hand_landmarks)
        
        if fingers_up == 0:
            return "Closed Fist"
        elif fingers_up == 5:
            return "Open Palm"
        else:
            return f"{fingers_up} Fingers"
    
    def process_frame(self, frame: np.ndarray) -> Tuple[str, np.ndarray]:
        """
        Process a video frame and detect gestures.
        
        Args:
            frame (np.ndarray): Input video frame
            
        Returns:
            Tuple[str, np.ndarray]: Detected gesture and annotated frame
        """
        # Flip the image horizontally for selfie-view display
        image = cv2.flip(frame, 1)
        
        # Convert BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect hands
        results = self.hands.process(rgb_image)
        
        gesture = "No Gesture"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Detect gesture
                gesture = self.detect_gesture(hand_landmarks)
                
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
        
        return gesture, image
    
    def handle_gesture_command(self, gesture: str, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert detected gesture to command and update state.
        
        Args:
            gesture (str): Detected gesture
            state (Dict[str, Any]): Current state dictionary
            
        Returns:
            Dict[str, Any]: Updated state dictionary
        """
        if gesture == "Open Palm":
            # Next page
            state["page"] = min(state["page"] + 1, state["total_pages"] - 1)
        elif gesture == "Closed Fist":
            # Previous page
            state["page"] = max(state["page"] - 1, 0)
        elif gesture == "2 Fingers":
            # Zoom in
            state["zoom"] = min(state["zoom"] * 1.1, 3.0)
        elif gesture == "3 Fingers":
            # Zoom out
            state["zoom"] = max(state["zoom"] * 0.9, 0.5)
        elif gesture == "4 Fingers":
            # Rotate right
            state["rotation"] = (state["rotation"] + 90) % 360
        elif gesture == "1 Fingers":
            # Pan mode
            # Pan implementation would depend on tracking finger movement
            pass
        
        return state
    
    def close(self):
        """Release MediaPipe resources."""
        self.hands.close()