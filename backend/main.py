"""FastAPI backend for gesture control system."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import json
import asyncio
from typing import Dict, Any
import base64
from src.gesture_control import GestureController
from src.gesture_features import GestureFeatures

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
controller = GestureController(max_hands=2, trajectory_points=32)
features = GestureFeatures()
active_connections: Dict[int, WebSocket] = {}
connection_counter = 0

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global connection_counter
    await websocket.accept()
    
    # Assign unique ID to connection
    connection_id = connection_counter
    connection_counter += 1
    active_connections[connection_id] = websocket
    
    try:
        while True:
            # Receive frame data from client
            data = await websocket.receive_text()
            frame_data = json.loads(data)
            
            # Convert base64 image to numpy array
            frame_bytes = base64.b64decode(frame_data["image"].split(",")[1])
            frame_arr = np.frombuffer(frame_bytes, dtype=np.uint8)
            frame = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)
            
            # Process frame
            gestures, annotated_frame = controller.process_frame(frame)
            
            # Handle mode-specific features
            if frame_data["mode"] == "mouse":
                features.handle_mouse_control(frame)
            elif frame_data["mode"] == "volume":
                features.handle_volume_control(frame)
            elif frame_data["mode"] == "drawing":
                annotated_frame = features.handle_drawing(frame)
            
            # Convert processed frame back to base64
            _, buffer = cv2.imencode('.jpg', annotated_frame)
            img_str = base64.b64encode(buffer).decode('utf-8')
            
            # Send results back to client
            await websocket.send_json({
                "gestures": gestures,
                "processed_image": f"data:image/jpeg;base64,{img_str}"
            })
    
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        del active_connections[connection_id]

@app.on_event("startup")
async def startup():
    print("Gesture Control Backend Started")

@app.on_event("shutdown")
async def shutdown():
    # Cleanup resources
    controller.close()
    cv2.destroyAllWindows()