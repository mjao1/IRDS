import cv2
import numpy as np
import face_recognition
import os
import serial
import pygame

# Initialize video capture from external webcam
cap = cv2.VideoCapture(1)

# Initialize the serial communication with Arduino
arduinoCoordinates = serial.Serial('/dev/cu.usbmodem4827E2E11E382', 57600)

# Send face coordinates to Arduino IDE
def send_coordinates_arduino(y, w, h, x):
    coordinates = f"{(x + w)/2},{(y + h)/2}\r"
    arduinoCoordinates.write(coordinates.encode())
    print(f"X{(x + w)/2}Y{(y + h)/2}\n")

# Loads known faces from a directory
def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []

    # Iterate over each directory in the known faces directory
    for user_name in os.listdir(known_faces_dir):
        user_dir = os.path.join(known_faces_dir, user_name)
        if os.path.isdir(user_dir):
            # Iterate over each image in the user directory
            for image_name in os.listdir(user_dir):
                image_path = os.path.join(user_dir, image_name)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    # Append the encodings and user name to the respective lists
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(user_name)

    return known_face_encodings, known_face_names

known_faces_dir = "known_faces"

known_face_encodings, known_face_names = load_known_faces(known_faces_dir)

face_locations = []
face_encodings = []
face_names = []

counter = 0
seen_names = []

while True:
    # Get frame from webcam
    ret, frame = cap.read()

    # Flip frame horizontally, resize to 1/4 size for faster reading, and convert frame to RGB
    flipped_frame = cv2.flip(frame, 1)
    small_frame = cv2.resize(flipped_frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
  
    # Detect face locations and encodings in the frame 
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
      
        # Get distances between face and known faces
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]  

        face_names.append(name)

        # Play sound if new face is detected
        if name in seen_names and counter == 1:
            break
        else:
            counter = 0
            pygame.mixer.init()
            pygame.mixer.music.load("detected.wav")
            pygame.mixer.music.play()
            counter += 1
            seen_names.append(name)

    # Draw rectangle and labels around detected faces
    for (y, w, h, x), name in zip(face_locations, face_names):
        # Rescale frame to full size
        y *= 4
        w *= 4
        h *= 4
        x *= 4
        
        # Draw rectangle around face
        cv2.rectangle(flipped_frame, (x, y), (w, h), (0, 0, 255), 2)  

        # Draw label box
        cv2.rectangle(flipped_frame, (x, h - 35), (w, h), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(flipped_frame, name, (x + 6, h - 6), font, 1.0, (255, 255, 255), 1)

      # Send face coordinates to Arduino IDE if face is unknown (can be changed to known faces by changing "Unknown" to a known face name)
        if name == "Unknown":
            send_coordinates_arduino(y, w, h, x)

    # Display the frame
    cv2.imshow('Video', flipped_frame)

    # Break loop if 'x' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

# Close camera windows
cap.release()
cv2.destroyAllWindows()
