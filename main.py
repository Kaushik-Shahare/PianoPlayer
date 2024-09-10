import cv2
import numpy as np
import pygame
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from modules.draw_hand_landmark import draw_landmarks_on_image
from modules.draw_fingertips import draw_fingertips
from modules.key_contours import getWhiteKeyContours, getBlackKeyContours
from modules.key_notes import getKeyWithNote, find_clicked_key

# Initialize MediaPipe HandLandmarker
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
detector = vision.HandLandmarker.create_from_options(options)

# Initialize Pygame and load sounds
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

key_sounds = {
    'A': './audio/pianoKeys/key01.mp3',
    'B': './audio/pianoKeys/key02.mp3',
    'C': './audio/pianoKeys/key03.mp3',
    'D': './audio/pianoKeys/key04.mp3',
    'E': './audio/pianoKeys/key05.mp3',
    'F': './audio/pianoKeys/key06.mp3',
    'G': './audio/pianoKeys/key07.mp3',
    'A#': './audio/pianoKeys/key08.mp3',
    'C#': './audio/pianoKeys/key09.mp3',
    'D#': './audio/pianoKeys/key10.mp3',
    'F#': './audio/pianoKeys/key11.mp3',
    'G#': './audio/pianoKeys/key12.mp3',
}

sounds = {note: pygame.mixer.Sound(file) for note, file in key_sounds.items()}
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
last_channel_used = 2

# Initialize camera
Cam = cv2.VideoCapture(0)
width, height = 720, 1080
Cam.set(3, width)
Cam.set(4, height)

if not Cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Function to play the piano sound based on fingertip position
def play_piano_key(fingertip_positions, keys_with_notes):
    global last_channel_used
    for (x_finger, y_finger, z_finger) in fingertip_positions:
        note = find_clicked_key(x_finger, y_finger, keys_with_notes)
        if note:
            print(f"Playing sound for key: {note}")
            if last_channel_used == 2:
                channel1.play(sounds[note])
                last_channel_used = 1
            else:
                channel2.play(sounds[note])
                last_channel_used = 2

# Main loop
while True:
    ret, frame = Cam.read()
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection and contour detection
    edges = cv2.Canny(blur, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contoursWhite = getWhiteKeyContours(contours)
    contoursBlack = getBlackKeyContours(contours)

    keys_with_notes = getKeyWithNote(contoursBlack, contoursWhite, frame)

    # Convert frame to the format expected by MediaPipe (RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

    # Detect hand landmarks from the video frame
    detection_result = detector.detect(mp_image)
    if detection_result.hand_landmarks:
        # Process hand landmarks to detect fingertips
        annotated_frame = draw_landmarks_on_image(frame, detection_result)
        annotated_frame_with_fingertips = draw_fingertips(annotated_frame, detection_result)

        # Collect fingertip positions
        fingertip_positions = []
        fingertip_indices = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky fingertips
        for hand_landmarks in detection_result.hand_landmarks:
            for index in fingertip_indices:
                x = int(hand_landmarks[index].x * frame.shape[1])
                y = int(hand_landmarks[index].y * frame.shape[0])
                z = int(hand_landmarks[index].z * frame.shape[0])
                if index == 8:
                    print(f"fingertip Indice: {index} X: {x}, Y: {y}, Z: {z}")
                fingertip_positions.append((x, y, z))

        # Check if fingertips are pressing piano keys
        play_piano_key(fingertip_positions, keys_with_notes)

        # Display the result
        cv2.imshow('Hand and Piano Detection', annotated_frame_with_fingertips)
    else:
        cv2.imshow('Hand and Piano Detection', frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

# Cleanup
Cam.release()
cv2.destroyAllWindows()
pygame.quit()