import cv2
import numpy as np
import matplotlib.pyplot as plt
import pygame
Cam = cv2.VideoCapture(0)

from modules.key_contours import getWhiteKeyContours, getBlackKeyContours
from modules.key_notes import getKeyWithNote, find_clicked_key

width, height = 720, 1080


Cam.set(3, width)
Cam.set(4, height)

if not Cam.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()
pygame.mixer.music.set_volume(1)  # Sets the volume to maximum

# Create a mapping of keys to sounds
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

note = {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F', 'G': 'G', 'A#': 'A#', 'C#': 'C#', 'D#': 'D#', 'F#': 'F#', 'G#': 'G#'}

sounds = {note: pygame.mixer.Sound(file) for note, file in key_sounds.items()}
channel1 = pygame.mixer.Channel(0)
channel2 = pygame.mixer.Channel(1)
last_channel_used = 2


while True:
    # Load the image
    url = "./images/keyboard.png"
    # url = "./images/whitekeys.jpeg"
    # image = cv2.imread(url)
    ret, frame = Cam.read()
    image = frame

    
    if not ret:
        print("Error: Can't receive frame (stream end?). Exiting ...")
        break
    
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
    contours, _ = cv2.findContours(thick_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contoursWhite = getWhiteKeyContours(contours)
    contoursBlack = getBlackKeyContours(contours)


    # cv2.drawContours(image, contoursWhite, -1, (0, 255, 0), 2)
    # cv2.drawContours(image, contoursBlack, -1, (0, 0, 255), 2)

    # Initialize sound for each key

    # Create a window to display the keyboard
    cv2.namedWindow('Keyboard')

    keys_with_notes = getKeyWithNote(contoursBlack, contoursWhite, image)

    # Handle mouse click events
    def play_key(event, x_click, y_click, flags, param):
        global last_channel_used
        if event == cv2.EVENT_LBUTTONDOWN: 
            note = find_clicked_key(x_click, y_click, keys_with_notes)
            print(f"Playing sound for key: {note}")
            if note:
            #    sounds[note].play() 
                if last_channel_used == 2:
                    channel1.play(sounds[note])
                    last_channel_used = 1
                else:
                    channel2.play(sounds[note])
                    last_channel_used = 2


    cv2.setMouseCallback('Keyboard',  play_key)
    cv2.imshow('Keyboard',image)
    if cv2.waitKey(1) & 0xFF == 27:
        break


# while True:
#     cv2.imshow('Keyboard',image)
#     cv2.imshow('Camera', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

Cam.release()
cv2.destroyAllWindows()
pygame.quit()
