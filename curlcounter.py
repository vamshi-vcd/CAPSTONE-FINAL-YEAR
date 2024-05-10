#!/usr/bin/env python
# coding: utf-8

import numpy as np
import mediapipe as mp
from PIL import Image
from skimage import io
from skimage.color import rgb2gray
from skimage.draw import circle
from skimage.draw import line
from skimage.filters import threshold_otsu
from skimage.transform import resize

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Function to calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle

# Setup mediapipe instances
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Curl counter variables
counter = 0 
stage = None

# Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:  # Changed from 'cap.isOpened()' to an infinite loop since video capturing is not directly supported by scikit-image.
        # Capture frame using scikit-image
        frame = io.imread('frame.jpg')  # Assuming you have saved a frame as 'frame.jpg' or you have another way of capturing frames
        
        # Recolor image to RGB (not needed if you're directly capturing RGB images)
        image_rgb = frame

        # Make detection
        results = pose.process(image_rgb)

        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * image_rgb.shape[1],
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * image_rgb.shape[0]]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image_rgb.shape[1],
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image_rgb.shape[0]]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * image_rgb.shape[1],
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * image_rgb.shape[0]]
            
            # Calculate angle
            angle = calculate_angle(shoulder, elbow, wrist)
            
            # Visualize angle
            # You can choose not to display the angle if not needed
            
            # Curl counter logic
            if angle > 160:
                stage = "down"
            if angle < 30 and stage =='down':
                stage="up"
                counter +=1
                print(counter)
                       
        except:
            pass
        
        # Render curl counter
        # You may choose not to render the counter if not needed
        
        # Render detections
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        # You may choose to display the frame if needed
        # io.imshow(frame)
        # io.show()
        
        # You may have some other way of terminating the loop
        # Here, we use a keyboard interrupt to break the loop
        try:
            # Placeholder for any termination condition
            pass
        except KeyboardInterrupt:
            break
