import cv2
from cvzone.FaceDetectionModule import FaceDetector
from cvzone.SerialModule import SerialObject
import time

arduino = SerialObject('COM3')

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = FaceDetector(minDetectionCon=0.8)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

center_threshold = frame_width // 6
left_threshold = frame_width // 3
right_threshold = frame_width - left_threshold

last_command = None
last_face_center_x = None
face_lost_time = 0
face_lost_threshold = 1.0

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)
    cv2.line(img, (left_threshold, 0), (left_threshold, frame_height), (0, 255, 0), 2)  # Lewa granica
    cv2.line(img, (right_threshold, 0), (right_threshold, frame_height), (0, 255, 0), 2)  # Prawa granica
    cv2.rectangle(img, (left_threshold, 0), (right_threshold, frame_height), (255, 0, 0), 2)  # Środkowa strefa

    if bboxs:
        x, y, w, h = bboxs[0]['bbox']
        face_center_x = x + w // 2
        face_lost_time = 0
        if face_center_x < left_threshold:
            command = 2  # Obrót w prawo
        elif face_center_x > right_threshold:
            command = 3  # Obrót w lewo
        else:
            command = 1  # Stop
        if command != last_command:
            print(f"Wysyłam do Arduino: {command}")  # Logowanie w konsoli
            arduino.sendData([command])
            last_command = command
    else:
        face_lost_time += 0.1
        if face_lost_time >= face_lost_threshold:
            command = 0
            if command != last_command:
                print(f"Wysyłam do Arduino: {command}")
                arduino.sendData([command])
                last_command = command

    cv2.imshow("Image", img)
    cv2.waitKey(1)
