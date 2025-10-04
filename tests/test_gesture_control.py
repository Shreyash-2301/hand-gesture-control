"""Unit tests for gesture control module."""

import pytest
import numpy as np
import cv2
from src.gesture_control import GestureController

def test_gesture_controller_initialization():
    """Test GestureController initialization."""
    controller = GestureController()
    assert controller is not None
    controller.close()

def test_process_frame():
    """Test frame processing with a blank image."""
    controller = GestureController()
    
    # Create a blank test image
    test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Process frame
    gesture, annotated_frame = controller.process_frame(test_frame)
    
    # Verify outputs
    assert gesture == "No Gesture"
    assert annotated_frame.shape == test_frame.shape
    
    controller.close()

def test_handle_gesture_command():
    """Test gesture command handling."""
    controller = GestureController()
    
    # Initial state
    state = {
        "page": 0,
        "total_pages": 5,
        "zoom": 1.0,
        "rotation": 0
    }
    
    # Test page navigation
    state = controller.handle_gesture_command("Open Palm", state)
    assert state["page"] == 1
    
    state = controller.handle_gesture_command("Closed Fist", state)
    assert state["page"] == 0
    
    # Test zoom
    state = controller.handle_gesture_command("2 Fingers", state)
    assert state["zoom"] > 1.0
    
    state = controller.handle_gesture_command("3 Fingers", state)
    assert state["zoom"] < 1.1
    
    # Test rotation
    state = controller.handle_gesture_command("4 Fingers", state)
    assert state["rotation"] == 90
    
    controller.close()