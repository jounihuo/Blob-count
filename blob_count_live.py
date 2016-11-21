import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)

#Wheat parameters
params = cv2.SimpleBlobDetector_Params()
# Change thresholds
params.minThreshold = 0
params.maxThreshold = 100
# Filter by Area.
params.filterByArea = True
params.maxArea = 900
params.minArea = 300
# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.5
params.maxCircularity = 1.0
# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.4
params.maxConvexity = 1.0    
# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.1
params.maxInertiaRatio = 1.0
# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)

#Larger blob parameters
params2 = cv2.SimpleBlobDetector_Params()
# Change thresholds
params2.minThreshold = 0
params2.maxThreshold = 100
# Filter by Area.
params2.filterByArea = True
params2.maxArea = 2800
params2.minArea = 900
# Filter by Circularity
params2.filterByCircularity = True
params2.minCircularity = 0.01
params2.maxCircularity = 1.0
# Filter by Convexity
params2.filterByConvexity = True
params2.minConvexity = 0.1
params2.maxConvexity = 1.0    
# Filter by Inertia
params2.filterByInertia = True
params2.minInertiaRatio = 0.01
params2.maxInertiaRatio = 1.0
# Create a detector with the parameters
detector2 = cv2.SimpleBlobDetector_create(params2)

font = cv2.FONT_HERSHEY_SIMPLEX
note = 0

current_type = "wheat"

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = 255 - gray
    rows,cols = gray.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),180,1)
    gray = cv2.warpAffine(gray,M,(cols,rows))
    keypoints = detector.detect(gray)
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
    # Display the resulting frame
    cv2.imshow('frame',gray)
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