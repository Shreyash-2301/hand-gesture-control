"""Enhanced gesture detection and control module using MediaPipe."""

import cv2
import mediapipe as mp
import numpy as np
from typing import Tuple, Dict, Any, Optional, List
from collections import deque
import time

class GestureController:
    """Advanced gesture detection and control system."""
    
    def __init__(self, max_hands: int = 2, trajectory_points: int = 32):
        """
        Initialize the gesture controller.
        
        Args:
            max_hands (int): Maximum number of hands to detect
            trajectory_points (int): Number of points to store for gesture trajectories
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture trajectory tracking
        self.trajectory_length = trajectory_points
        self.trajectories = {}  # Store trajectories for each hand
        self.gesture_history = deque(maxlen=10)  # Store last 10 gestures
        
        # Dynamic gesture recognition
        self.gesture_start_time = None
        self.gesture_positions = []
        self.dynamic_gesture_threshold = 1.0  # seconds
        
        # Custom gesture mapping
        self.custom_gestures = {}
        
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
    
    def process_frame(self, frame: np.ndarray) -> Tuple[List[str], np.ndarray]:
        """
        Process a video frame and detect gestures.
        
        Args:
            frame (np.ndarray): Input video frame
            
        Returns:
            Tuple[List[str], np.ndarray]: List of detected gestures and annotated frame
        """
        # Flip the image horizontally for selfie-view display
        image = cv2.flip(frame, 1)
        
        # Convert BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect hands
        results = self.hands.process(rgb_image)
        
        detected_gestures = []
        
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw hand landmarks
                self.mp_draw.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
                
                # Update hand trajectory
                self.update_trajectory(idx, hand_landmarks)
                
                # Detect static gesture
                static_gesture = self.detect_gesture(hand_landmarks)
                if static_gesture:
                    detected_gestures.append(static_gesture)
                
                # Detect dynamic gesture
                dynamic_gesture = self.detect_dynamic_gesture(hand_landmarks)
                if dynamic_gesture:
                    detected_gestures.append(dynamic_gesture)
                
                # Check for custom gestures
                custom_gesture = self.match_custom_gesture(hand_landmarks)
                if custom_gesture:
                    detected_gestures.append(f"Custom: {custom_gesture}")
        
        # Draw trajectories
        image = self.draw_trajectories(image)
        
        # Update gesture history
        if detected_gestures:
            self.gesture_history.extend(detected_gestures)
        
        # Display gesture history
        self.draw_gesture_history(image)
        
        return detected_gestures, image
    
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
    
    def detect_dynamic_gesture(self, hand_landmarks) -> Optional[str]:
        """
        Detect gestures based on hand movement.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            
        Returns:
            Optional[str]: Detected dynamic gesture name if any
        """
        palm_pos = (hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y)
        
        if not self.gesture_start_time:
            self.gesture_start_time = time.time()
            self.gesture_positions = [palm_pos]
            return None
        
        self.gesture_positions.append(palm_pos)
        
        if time.time() - self.gesture_start_time > self.dynamic_gesture_threshold:
            # Analyze movement pattern
            if len(self.gesture_positions) > 10:
                dx = self.gesture_positions[-1][0] - self.gesture_positions[0][0]
                dy = self.gesture_positions[-1][1] - self.gesture_positions[0][1]
                
                # Detect swipe gestures
                if abs(dx) > 0.2:
                    gesture = "Swipe Right" if dx > 0 else "Swipe Left"
                elif abs(dy) > 0.2:
                    gesture = "Swipe Down" if dy > 0 else "Swipe Up"
                else:
                    gesture = None
                
                # Reset tracking
                self.gesture_start_time = None
                self.gesture_positions = []
                
                return gesture
        
        return None
    
    def update_trajectory(self, hand_id: int, landmarks) -> None:
        """
        Update the trajectory for a specific hand.
        
        Args:
            hand_id (int): Unique identifier for the hand
            landmarks: MediaPipe hand landmarks
        """
        if hand_id not in self.trajectories:
            self.trajectories[hand_id] = deque(maxlen=self.trajectory_length)
        
        # Track palm center
        palm_center = np.mean([(landmarks.landmark[i].x, landmarks.landmark[i].y) 
                             for i in [0, 5, 17]], axis=0)
        self.trajectories[hand_id].append(palm_center)
    
    def draw_trajectories(self, image: np.ndarray) -> np.ndarray:
        """
        Draw hand movement trajectories on the image.
        
        Args:
            image (np.ndarray): Input image
            
        Returns:
            np.ndarray: Image with trajectories drawn
        """
        h, w, _ = image.shape
        
        for hand_id, trajectory in self.trajectories.items():
            points = np.array([(int(x * w), int(y * h)) for x, y in trajectory])
            if len(points) > 1:
                # Draw trajectory line with fading effect
                for i in range(len(points) - 1):
                    alpha = (i + 1) / len(points)
                    color = (0, int(255 * alpha), int(255 * (1 - alpha)))
                    cv2.line(image, tuple(points[i]), tuple(points[i + 1]), color, 2)
        
        return image
    
    def draw_gesture_history(self, image: np.ndarray) -> None:
        """
        Draw gesture history on the image.
        
        Args:
            image (np.ndarray): Input image
        """
        h, w, _ = image.shape
        y_offset = 30
        
        for i, gesture in enumerate(reversed(self.gesture_history)):
            if i >= 5:  # Show only last 5 gestures
                break
            cv2.putText(
                image,
                f"Recent: {gesture}",
                (10, y_offset + i * 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
    
    def record_custom_gesture(self, name: str, landmarks) -> None:
        """
        Record a custom gesture pattern.
        
        Args:
            name (str): Name of the custom gesture
            landmarks: MediaPipe hand landmarks
        """
        # Store normalized landmark positions
        gesture_pattern = [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
        self.custom_gestures[name] = gesture_pattern
    
    def match_custom_gesture(self, landmarks, threshold: float = 0.2) -> Optional[str]:
        """
        Try to match current hand pose with recorded custom gestures.
        
        Args:
            landmarks: MediaPipe hand landmarks
            threshold (float): Matching threshold
            
        Returns:
            Optional[str]: Matched gesture name if found
        """
        if not self.custom_gestures:
            return None
            
        current_pattern = [(lm.x, lm.y, lm.z) for lm in landmarks.landmark]
        
        best_match = None
        min_distance = float('inf')
        
        for name, pattern in self.custom_gestures.items():
            # Calculate pattern similarity
            distance = np.mean([np.sqrt(
                (c[0] - p[0])**2 + (c[1] - p[1])**2 + (c[2] - p[2])**2
            ) for c, p in zip(current_pattern, pattern)])
            
            if distance < threshold and distance < min_distance:
                min_distance = distance
                best_match = name
        
        return best_match
    
    def close(self):
        """Release MediaPipe resources."""
        self.hands.close()