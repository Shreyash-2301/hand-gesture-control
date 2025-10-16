"""Advanced gesture control features for system interaction."""

import cv2
import numpy as np
import pyautogui
import os
from typing import Tuple, Dict, Any, Optional

class GestureFeatures:
    """Provides advanced gesture-based control features."""
    
    def __init__(self):
        """Initialize gesture features."""
        # Screen properties for mouse control
        self.screen_width, self.screen_height = pyautogui.size()
        pyautogui.FAILSAFE = False
        
        # Drawing properties
        self.drawing_canvas = None
        self.drawing_color = (0, 255, 0)  # Default green
        self.drawing_thickness = 2
        self.last_point = None
        
        # Volume control
        self.volume_min = 0
        self.volume_max = 100
        self.current_volume = 50
        
        # Mode tracking
        self.current_mode = "normal"  # normal, mouse, volume, drawing
        
    def init_drawing_canvas(self, frame_shape: Tuple[int, int, int]) -> None:
        """
        Initialize the drawing canvas.
        
        Args:
            frame_shape: Shape of the video frame (height, width, channels)
        """
        if self.drawing_canvas is None:
            self.drawing_canvas = np.zeros(frame_shape, dtype=np.uint8)
    
    def handle_mouse_control(self, hand_landmarks, frame_shape: Tuple[int, int]) -> None:
        """
        Control mouse using hand position.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            frame_shape: Shape of the video frame (height, width)
        """
        # Get index finger tip position
        index_tip = hand_landmarks.landmark[8]
        
        # Convert coordinates to screen position
        screen_x = int(index_tip.x * self.screen_width)
        screen_y = int(index_tip.y * self.screen_height)
        
        # Move mouse
        pyautogui.moveTo(screen_x, screen_y, duration=0.1)
        
        # Check for click gesture (thumb and index finger pinch)
        thumb_tip = hand_landmarks.landmark[4]
        if self._calculate_distance(thumb_tip, index_tip) < 0.05:
            pyautogui.click()
    
    def handle_volume_control(self, hand_landmarks) -> None:
        """
        Control system volume using hand position.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
        """
        # Get thumb and pinky positions for volume control
        thumb_tip = hand_landmarks.landmark[4]
        pinky_tip = hand_landmarks.landmark[20]
        
        # Calculate distance for volume level
        distance = self._calculate_distance(thumb_tip, pinky_tip)
        
        # Map distance to volume (0-100)
        volume = int(max(0, min(100, distance * 200)))
        
        # Set system volume
        if abs(volume - self.current_volume) > 5:  # Prevent tiny adjustments
            self.current_volume = volume
            os.system(f"osascript -e 'set volume output volume {volume}'")
    
    def handle_drawing(self, hand_landmarks, frame: np.ndarray) -> np.ndarray:
        """
        Handle virtual drawing using hand gestures.
        
        Args:
            hand_landmarks: MediaPipe hand landmarks
            frame: Input video frame
            
        Returns:
            np.ndarray: Frame with drawing overlay
        """
        self.init_drawing_canvas(frame.shape)
        
        # Get index finger tip position
        index_tip = hand_landmarks.landmark[8]
        point = (
            int(index_tip.x * frame.shape[1]),
            int(index_tip.y * frame.shape[0])
        )
        
        # Draw if index finger is up and middle finger is down
        if (hand_landmarks.landmark[8].y < hand_landmarks.landmark[7].y and 
            hand_landmarks.landmark[12].y > hand_landmarks.landmark[11].y):
            if self.last_point is not None:
                cv2.line(
                    self.drawing_canvas,
                    self.last_point,
                    point,
                    self.drawing_color,
                    self.drawing_thickness
                )
            self.last_point = point
        else:
            self.last_point = None
        
        # Combine frame with drawing
        return cv2.addWeighted(frame, 1, self.drawing_canvas, 0.5, 0)
    
    def handle_shortcuts(self, gesture: str) -> None:
        """
        Execute shortcuts based on gestures.
        
        Args:
            gesture: Detected gesture name
        """
        shortcuts = {
            "Open Palm": lambda: pyautogui.hotkey('command', 'space'),  # Spotlight
            "Closed Fist": lambda: pyautogui.hotkey('command', 'w'),    # Close window
            "2 Fingers": lambda: pyautogui.hotkey('command', 'tab'),    # App switcher
            "3 Fingers": lambda: pyautogui.hotkey('command', 'm'),      # Minimize
            "4 Fingers": lambda: pyautogui.hotkey('command', 'q'),      # Quit app
        }
        
        if gesture in shortcuts:
            shortcuts[gesture]()
    
    def clear_drawing(self) -> None:
        """Clear the drawing canvas."""
        if self.drawing_canvas is not None:
            self.drawing_canvas.fill(0)
    
    def change_drawing_color(self) -> None:
        """Cycle through drawing colors."""
        colors = [
            (0, 255, 0),   # Green
            (255, 0, 0),   # Blue
            (0, 0, 255),   # Red
            (255, 255, 0), # Cyan
            (255, 0, 255), # Magenta
        ]
        current_index = colors.index(self.drawing_color)
        self.drawing_color = colors[(current_index + 1) % len(colors)]
    
    def _calculate_distance(self, point1, point2) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            point1: First point
            point2: Second point
            
        Returns:
            float: Distance between points
        """
        return ((point1.x - point2.x) ** 2 + 
                (point1.y - point2.y) ** 2 + 
                (point1.z - point2.z) ** 2) ** 0.5
    
    def handle_mode_switch(self, gesture: str) -> None:
        """
        Switch between different control modes.
        
        Args:
            gesture: Detected gesture name
        """
        mode_gestures = {
            "5 Fingers Up": "normal",
            "Pinch": "mouse",
            "Victory": "volume",
            "ILY": "drawing"
        }
        
        if gesture in mode_gestures:
            self.current_mode = mode_gestures[gesture]
            self.clear_drawing()  # Clear drawing when switching modes