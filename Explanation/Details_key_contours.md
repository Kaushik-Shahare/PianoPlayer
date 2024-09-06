These two functions, `getWhiteKeyContours` and `getBlackKeyContours`, are designed to differentiate and categorize the contours of piano keys from an image based on their size and aspect ratio. Here's a breakdown of how each function works:

### 1. `getWhiteKeyContours(contours)`

This function identifies the white keys of a piano based on the contours extracted from an image.

```python
def getWhiteKeyContours(contours):
    contoursWhite = []
    for contour in contours:
        area = cv2.contourArea(contour)  # Calculate the area of the contour
        x, y, w, h = cv2.boundingRect(contour)  # Get the bounding rectangle (x, y, width, height)
        aspect_ratio = w / float(h)  # Calculate aspect ratio (width / height)
    
        # Set limits for the area and aspect ratio for white keys
        min_area = 10000 
        max_area = 50000
        min_aspect_ratio = 0.1 
        max_aspect_ratio = 1 
    
        # Check if the contour falls within the range of a white key
        if min_area < area < max_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            contoursWhite.append(contour)  # If conditions are met, add it to the white key contours list
    return contoursWhite  # Return the list of white key contours
```

- **Purpose**: It filters the contours based on their area and aspect ratio to identify white keys.
- **White Key Conditions**:
  - The **area** should be between 10,000 and 50,000 pixels.
  - The **aspect ratio** (width/height) should be between `0.1` and `1`. White keys are typically long and narrow, so their aspect ratio will be small but less than 1.

### 2. `getBlackKeyContours(contours)`

This function works similarly to `getWhiteKeyContours` but is tuned to identify the black keys, which are smaller and narrower.

```python
def getBlackKeyContours(contours):
    contoursBlack = []
    for contour in contours:
        area = cv2.contourArea(contour)  # Calculate the area of the contour
        x, y, w, h = cv2.boundingRect(contour)  # Get the bounding rectangle (x, y, width, height)
        aspect_ratio = w / float(h)  # Calculate aspect ratio (width / height)
    
        # Set limits for the area and aspect ratio for black keys
        min_area = 5000 
        max_area = 50000
        min_aspect_ratio = 0.25
        max_aspect_ratio = 1 
    
        # Check if the contour falls within the range of a black key
        if min_area < area < max_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            contoursBlack.append(contour)  # If conditions are met, add it to the black key contours list
    return contoursBlack  # Return the list of black key contours
```

- **Purpose**: It filters the contours based on their area and aspect ratio to identify black keys.
- **Black Key Conditions**:
  - The **area** should be between 5,000 and 50,000 pixels (black keys are smaller).
  - The **aspect ratio** should be between `0.25` and `1`. Black keys are narrower and taller than white keys, so their aspect ratio is closer to that of a square but still less than 1.

### Summary

- **`getWhiteKeyContours`** identifies white keys by selecting contours that are larger and longer, with a lower aspect ratio.
- **`getBlackKeyContours`** identifies black keys by focusing on smaller, narrower contours that fall within a different aspect ratio range.
- Both functions return a list of contours that match the respective key characteristics, which are then used for further processing like sound mapping in your main program.

These functions are essential for distinguishing between the different types of piano keys based on their shape in the camera feed.
