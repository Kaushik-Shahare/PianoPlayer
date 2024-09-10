import cv2

def draw_fingertips(image, detection_result):
    # Fingertip indices based on the hand landmark model
    fingertip_indices = [4, 8, 12, 16, 20]

    # Check for detected landmarks in each hand
    for hand_landmarks in detection_result.hand_landmarks:
        for index in fingertip_indices:
            landmark = hand_landmarks[index]
            x, y = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])  # Scale landmarks

            # Draw a red box around the fingertip
            box_size = 20  # Define the size of the box
            cv2.rectangle(image, (x - box_size//2, y - box_size//2), 
                          (x + box_size//2, y + box_size//2), (0, 255, 0), 2)

    return image