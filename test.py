import cv2
import pickle
import numpy as np
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
from sklearn.neighbors import KNeighborsClassifier

# Function to speak text
def speak(str1):
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str1)

# Initialize video capture and face detector
video = cv2.VideoCapture(0)
facedetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load existing faces data and labels
with open('data/names.pkl', 'rb') as w:
    LABELS = pickle.load(w)
with open('data/faces_data.pkl', 'rb') as f:
    FACES = pickle.load(f)

# Ensure both FACES and LABELS have the same length
min_length = min(len(LABELS), FACES.shape[0])  # Find the minimum length
FACES = FACES[:min_length]
LABELS = LABELS[:min_length]

print(f"Shape of FACES: {FACES.shape}")
print(f"Shape of LABELS: {len(LABELS)}")

# Initialize the KNN classifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(FACES, LABELS)

# Load background image and check if it loads correctly
imgBackground = cv2.imread("background.jpg")

if imgBackground is None:
    print("Error: Unable to load background image")
    video.release()
    cv2.destroyAllWindows()
    exit()  # Exit the program if the background image can't be loaded

# Column names for attendance CSV file
COL_NAMES = ['NAME', 'TIME']

# Main loop for face recognition and attendance
while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Crop and resize the detected face
        crop_img = frame[y:y+h, x:x+w, :]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        # Predict using the KNN classifier
        output = knn.predict(resized_img)

        # Capture timestamp for attendance
        ts = time.time()
        date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
        timestamp = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
        exist = os.path.isfile(f"Attendance/Attendance_{date}.csv")

        # Draw a rectangle around the face and display name
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 1)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (50, 50, 255), 2)
        cv2.rectangle(frame, (x, y-40), (x+w, y), (50, 50, 255), -1)
        cv2.putText(frame, str(output[0]), (x, y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)

        # Store attendance entry
        attendance = [str(output[0]), str(timestamp)]

    # Resize the frame to match the target size (438x640)
    frame_resized = cv2.resize(frame, (640, 438))

    # Overlay the resized frame on the background
    imgBackground[162:162 + 438, 55:55 + 640] = frame_resized

    cv2.imshow("Frame", imgBackground)

    k = cv2.waitKey(1)

    # If 'o' key is pressed, log attendance
    if k == ord('o'):
        speak("Attendance Taken..")
        time.sleep(5)

        # Write to the attendance CSV file
        if exist:
            with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(attendance)
        else:
            with open(f"Attendance/Attendance_{date}.csv", "a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(COL_NAMES)
                writer.writerow(attendance)

    # If 'q' key is pressed, exit
    if k == ord('q'):
        break

# Release video capture and close windows
video.release()
cv2.destroyAllWindows()
