import cv2
import numpy as np
import matplotlib.pyplot as plt
import pygame

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()
pygame.mixer.music.set_volume(1.0)  # Sets the volume to maximum

# Load the image
# url = "./images/keyboard.jpeg"
url = "./images/keyboard.png"
image = cv2.imread(url)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Edge detection
edges = cv2.Canny(gray, 50, 150)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
# for contour in contours:
#     approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#     if len(approx) == 4:  # Assuming keys are rectangular
#         cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# cv2.imshow('Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Create a mapping of keys to sounds
key_sounds = {
    'A': './audio/bruh.mp3',
    'B': './audio/bruh.mp3',
    'C': './audio/bruh.mp3',
    'D': './audio/bruh.mp3',
    'E': './audio/bruh.mp3',
    'F': './audio/bruh.mp3',
    'G': './audio/bruh.mp3',
}

# Initialize sound for each key
sounds = {note: pygame.mixer.Sound(file) for note, file in key_sounds.items()}

# Detect and map keys
notes_sequence = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
# keys = []
# i=0
# for contour in contours:
#     note = notes_sequence[i % len(notes_sequence)]
#     i+=1
#     approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#     if len(approx) == 4:  # Assuming keys are rectangular
#         x, y, w, h = cv2.boundingRect(approx)
#         key_center = (x + w//2, y + h//2)
#         # keys.append((key_center, 'C'))  # Assign a note based on position
#         keys.append((approx, note))

# Create a window to display the keyboard
cv2.namedWindow('Keyboard')

# Function to detect and play key press
# def play_key(event, x, y, flags, param):
#     # print(f"Event detected: {event}, at position: {x}, {y}")
#     if event == cv2.EVENT_LBUTTONDOWN:
#         print("Left button clicked")
#         for key in keys:
#             contour, event = key
#             # if cv2.pointPolygonTest(np.array([key[0]]), (x, y), False) >= 0:
#             if cv2.pointPolygonTest(np.array(contour), (x, y), False) >= 0:
#                 print(f"Playing sound for key: {key[1]}")
#                 sounds[event].play()
keys_with_notes = []
i=0
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    note = notes_sequence[i % len(notes_sequence)]
    i+=1
    keys_with_notes.append({'note': note, 'rect': (x, y, w, h)})

# Function to find which key was clicked
def find_clicked_key(x_click, y_click):
    for key in keys_with_notes:
        x, y, w, h = key['rect']
        if x <= x_click <= x + w and y <= y_click <= y + h:
            return key['note']
    return None

# Example click handling
def play_key(event, x_click, y_click, flags, param):
    note = find_clicked_key(x_click, y_click)
    print(f"Playing sound for key: {note}")
    if note:
        sound = sounds[note]
        sound.play()

cv2.setMouseCallback('Keyboard', play_key)

while True:
    cv2.imshow('Keyboard',image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
pygame.quit()
