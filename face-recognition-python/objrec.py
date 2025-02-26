import cv2
import numpy as np
import serial
import pygame
from pathlib import Path

# Initialize video capture from external webcam
cap = cv2.VideoCapture(1)

# Initialize the serial communication with Arduino
arduinoCoordinates = serial.Serial('/dev/cu.usbmodem4827E2E11E382', 57600)

# Load YOLO model
yolo_dir = Path(__file__).parent / "yolo-coco"
net = cv2.dnn.readNet(
    str(yolo_dir / "yolov3.weights"),
    str(yolo_dir / "yolov3.cfg")
)

# Load COCO class labels
with open(str(yolo_dir / "coco.names"), "r") as f:
    classes = [line.strip() for line in f.readlines()]

# YOLO settings
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

pygame.mixer.init()

# Send coordinates to Arduino IDE
def send_coordinates_arduino(x, y, w, h):
    center_x = x + (w/2)
    center_y = y + (h/2)
    coordinates = f"{center_x},{center_y}\r"
    arduinoCoordinates.write(coordinates.encode())
    print(f"X{center_x}Y{center_y}\n")

# List of objects to track (can be modified)
target_objects = ["cell phone", "laptop", "bottle"]
seen_objects = []
counter = 0

while True:
    # Get frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Prepare image for YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Box coordinates
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Draw boxes and labels
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            
            if label in target_objects:
                # Draw rectangle and label
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Play sound if new object is detected
                if label not in seen_objects and counter == 0:
                    pygame.mixer.music.load("detected.wav")
                    pygame.mixer.music.play()
                    seen_objects.append(label)
                    counter += 1
                
                # Send object coordinates to Arduino IDE
                send_coordinates_arduino(x, y, w, h)

    if counter > 0:
        counter = 0

    # Display the frame
    cv2.imshow('Object Detection', frame)

    # Break loop if 'x' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Close camera windows
cap.release()
cv2.destroyAllWindows() 
