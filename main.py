import cv2
import numpy as np
import matplotlib.pyplot as plt
import pygame

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()
pygame.mixer.music.set_volume(1)  # Sets the volume to maximum

# Load the image
url = "./images/keyboard.png"
# url = "./images/whitekeys.jpg"
image = cv2.imread(url)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# ------------------------------------------------------------ # 
# Edge detection
# edges = cv2.Canny(blur, 50, 150)

# Canny for edges detection

## Initialize thick edges with same shape as blur image but with zeros
thick_edges = np.zeros_like(blur)

edges = cv2.Canny(blur, 100, 200)

# Thicken the edges
for i in range(-4, 4):
    # Add the edges shifted by i pixels in both directions in x and y
    thick_edges += (np.roll(edges, i, 0) + np.roll(edges, i, 1))

# ------------------------------------------------------------ # 


# Find contours
contours1, _ = cv2.findContours(thick_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours for keys
contours = []
for contour in contours1:
    area = cv2.contourArea(contour)
    x, y, w, h = cv2.boundingRect(contour)
    aspect_ratio = w / float(h)
    
    min_area = 500 
    max_area = 50000
    min_aspect_ratio = 0.1 
    max_aspect_ratio = 2 
    
    if min_area < area < max_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
        contours.append(contour)

cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Create a mapping of keys to sounds
key_sounds = {
    'A': './audio/pianoKeys/key01.mp3',
    'B': './audio/pianoKeys/key02.mp3',
    'C': './audio/pianoKeys/key03.mp3',
    'D': './audio/pianoKeys/key04.mp3',
    'E': './audio/pianoKeys/key05.mp3',
    'F': './audio/pianoKeys/key06.mp3',
    'G': './audio/pianoKeys/key07.mp3',
}

# Initialize sound for each key
sounds = {note: pygame.mixer.Sound(file) for note, file in key_sounds.items()}

# Detect and map keys
notes_sequence = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
notes_sequence = notes_sequence[::-1]  


# Create a window to display the keyboard
cv2.namedWindow('Keyboard')

keys_with_notes = []
i=0
for i, contour in enumerate(contours):
    x, y, w, h = cv2.boundingRect(contour)
    note = notes_sequence[i % len(notes_sequence)]
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, note, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
    keys_with_notes.append({'note': note, 'rect': (x, y, w, h)})

# Function to find which key was clicked
def find_clicked_key(x_click, y_click):
    for key in keys_with_notes:
        x, y, w, h = key['rect']
        if x <= x_click <= x + w and y <= y_click <= y + h:
            return key['note']
    return None

# Handle mouse click events
def play_key(event, x_click, y_click, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: 
        note = find_clicked_key(x_click, y_click)
        print(f"Playing sound for key: {note}")
        if note:
            sound = sounds[note]
            sound.play()

cv2.setMouseCallback('Keyboard',  play_key)

while True:
    cv2.imshow('Keyboard',image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
pygame.quit()
