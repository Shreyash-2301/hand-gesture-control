"""Basic gesture control demo using OpenCV."""

import cv2
import numpy as np

def main():
    """Run basic gesture control demo using color-based hand detection."""
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    
    print("Basic Gesture Control Demo")
    print("\nInstructions:")
    print("1. Keep your hand in good lighting")
    print("2. Move your hand to test tracking")
    print("3. Press 'q' to quit")
    
    # Define the lower and upper bounds for skin color in HSV
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    try:
        while True:
            # Read frame from webcam
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Create a mask for skin color
            mask = cv2.inRange(hsv, lower_skin, upper_skin)
            
            # Apply morphological operations to clean up the mask
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.erode(mask, kernel, iterations=2)
            mask = cv2.dilate(mask, kernel, iterations=2)
            
            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get the largest contour (presumably the hand)
                max_contour = max(contours, key=cv2.contourArea)
                
                # Get the convex hull and defects
                hull = cv2.convexHull(max_contour, returnPoints=False)
                defects = cv2.convexityDefects(max_contour, hull)
                
                # Draw the contour and hull
                cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)
                
                # Count fingers using convexity defects
                finger_count = 0
                if defects is not None:
                    for i in range(defects.shape[0]):
                        s, e, f, d = defects[i,0]
                        start = tuple(max_contour[s][0])
                        end = tuple(max_contour[e][0])
                        far = tuple(max_contour[f][0])
                        
                        # Calculate the triangle sides
                        a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                        b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                        c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                        
                        # Calculate the angle
                        angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c)) * 180/np.pi
                        
                        # If angle is less than 90 degrees, it's likely a finger
                        if angle <= 90:
                            finger_count += 1
                            cv2.circle(frame, far, 5, [0, 0, 255], -1)
                
                # Display finger count
                cv2.putText(frame, f'Fingers: {finger_count}', (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show the frames
            cv2.imshow('Hand Detection', frame)
            cv2.imshow('Mask', mask)
            
            # Break on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()