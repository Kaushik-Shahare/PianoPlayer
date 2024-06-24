import cv2

def getWhiteKeyContours(contours):
    contoursWhite = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
    
        min_area = 7000 
        max_area = 50000
        min_aspect_ratio = 0.1 
        max_aspect_ratio = 2 
    
        if min_area < area < max_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            contoursWhite.append(contour)
    return contoursWhite

def getBlackKeyContours(contours):
    contoursBlack = []
    for contour in contours:
        area = cv2.contourArea(contour)
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
    
        min_area = 500 
        max_area = 50000
        min_aspect_ratio = 0.25
        max_aspect_ratio = 2 
    
        if min_area < area < max_area and min_aspect_ratio < aspect_ratio < max_aspect_ratio:
            contoursBlack.append(contour)
    return contoursBlack