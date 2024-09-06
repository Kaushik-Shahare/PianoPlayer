import cv2


# Detect and map keys
notes_sequence_white = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
notes_sequence_white = notes_sequence_white[::-1]  

notes_sequence_black = ['C#', 'D#', 'F#', 'G#', 'A#']
notes_sequence_black = notes_sequence_black[::-1]

def getKeyWithNote(contoursBlack, contoursWhite, image):
    keys_with_notes = []
    # Draw the keys of black keys
    i=0
    for i, contour in enumerate(contoursBlack):
        x, y, w, h = cv2.boundingRect(contour)
        note = notes_sequence_black[i % len(notes_sequence_black)]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, note, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        keys_with_notes.append({'note': note, 'rect': (x, y, w, h), 'type': 'black'})

    # Draw the keys of white keys
    i=0
    for i, contour in enumerate(contoursWhite):
        x, y, w, h = cv2.boundingRect(contour)
        note = notes_sequence_white[i % len(notes_sequence_white)]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, note, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        keys_with_notes.append({'note': note, 'rect': (x, y, w, h), 'type': 'white'})
    
    return keys_with_notes


# Function to find which key was clicked
def find_clicked_key(x_click, y_click, keys_with_notes):
    keys = []
    for key in keys_with_notes:
        x, y, w, h = key['rect']
        if x <= x_click <= x + w and y <= y_click <= y + h:
            # return key['note']
            keys.append(key)

    if len(keys) >= 1:
        for key in keys:
            if key['note'] == 'black':
                return key['note']
        return keys[0]['note']
    else:
        return None
    

