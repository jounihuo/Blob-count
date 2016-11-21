import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

type_parameters = {
'wheat':     (0, 100, 1000, 400,  0.5, 1.0,  0.4, 1.0,  0.1, 1.00, 1),
'barley':    (0, 100, 1500, 700,  0.2, 1.0,  0.4, 1.0,  0.1, 1.00, 1),
'oat':       (0, 100, 2000, 500, 0.01, 1.0, 0.01, 1.0, 0.01, 0.30, 1),
'rye':       (0, 140, 1300, 300,  0.5, 0.8,  0.1, 1.0, 0.01, 0.30, 1),
'rape seed': (0, 100,  100,  50,  0.5, 1.0,  0.4, 1.0,  0.1, 1.00, 0)}

def create_blob_detect(type_parameters):
    #Function returns a blob detector with given parameters
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = type_parameters[0]
    params.maxThreshold = type_parameters[1]
    # Filter by Area.
    params.filterByArea = True
    params.maxArea = type_parameters[2]
    params.minArea = type_parameters[3]
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = type_parameters[4]
    params.maxCircularity = type_parameters[5]
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = type_parameters[6]
    params.maxConvexity = type_parameters[7]   
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = type_parameters[8]
    params.maxInertiaRatio = type_parameters[9]
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    return detector

def create_not_range_detect(type_parameters):
    #Function returns a blob detector with out of range parameters
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = type_parameters[0]
    params.maxThreshold = type_parameters[1]
    # Filter by Area.
    params.filterByArea = True
    params.maxArea = type_parameters[2]*5
    params.minArea = type_parameters[2]
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = type_parameters[4]
    params.maxCircularity = type_parameters[5]
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = type_parameters[6]
    params.maxConvexity = type_parameters[7]   
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = type_parameters[8]
    params.maxInertiaRatio = type_parameters[9]
    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    return detector
    
font = cv2.FONT_HERSHEY_SIMPLEX
note = 0
current_type = "wheat"

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if type_parameters[current_type][10] == 1:
        gray = 255 - gray
    #Image rotation of 180 degrees
    rows,cols = gray.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    gray = cv2.warpAffine(gray,M,(cols,rows))
    detector = create_blob_detect(type_parameters[current_type])
    keypoints = detector.detect(gray)
    detector2 = create_not_range_detect(type_parameters[current_type])
    keypoints2 = detector2.detect(gray)
    gray = cv2.drawKeypoints(gray, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    gray = cv2.drawKeypoints(gray, keypoints2, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #Text to display
    cv2.putText(gray,'Number of blobs = '+str(len(keypoints)),(10,50), font, 1,(255,0,0),2)
    cv2.putText(gray,'Using '+current_type+' settings.',(500,50), font, 1,(255,0,0),2)
    cv2.putText(gray,'Press s to save.',(10,80), font, 0.8,(255,0,0),2)
    cv2.putText(gray,'Press q to quit.',(10,110), font, 0.8,(255,0,0),2)
    localtime = time.asctime( time.localtime(time.time()) )
    cv2.putText(gray, localtime,(1550,1020), font, 0.8,(255,0,0),2)
    if note==1:
        cv2.putText(gray,'Saving image...',(10,510), font, 1,(255,0,0),2)
        cv2.imshow('frame',gray)
        note = 0
    #Display the resulting frame
    cv2.imshow('frame',gray)
    #User input from keys
    c = cv2.waitKey(1)
    #Change grain type
    if ord('1') == (c & 0xFF):
        current_type = "wheat"
    if ord('2') == (c & 0xFF):
        current_type = "barley"
    if ord('3') == (c & 0xFF):
        current_type = "oat"
    if ord('4') == (c & 0xFF):
        current_type = "rye"
    if ord('5') == (c & 0xFF):
        current_type = "rape seed"
    #To save
    if ord('s') == (c & 0xFF):
        cv2.imwrite(time.strftime('%Y_%m_%d_%H_%M ') + current_type + ".jpg", 255-gray)
        note = 1
        print 'Saved an image.'
    #To quit
    if ord('q') == (c & 0xFF):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()