import cv2
import numpy as np

Fire_Reported = 0

#video = cv2.VideoCapture("fogo.mp4") # If you want to use webcam use Index like 0,1.
#video = cv2.VideoCapture("Wildfires.mp4")
video = cv2.VideoCapture("flame.mp4")
while True:
    (grabbed, frame) = video.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (960, 540))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Set the lower and upper range values for hue
    lower_red = np.array([0, 175, 175])
    upper_red = np.array([15, 255, 255])
    lower_red2 = np.array([165, 175, 175])
    upper_red2 = np.array([180, 255, 255])

    # Create two masks for the two hue ranges and combine them using bitwise OR
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Apply morphology operations to remove noise and merge nearby fire regions
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=4)

    output = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    no_red = cv2.countNonZero(mask)

    if int(no_red) > 100:
        Fire_Reported = Fire_Reported + 1
        # Draw a rectangle around the detected fire region
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # Print "Fire Detected!" on the output frame
        cv2.putText(frame, "Fire Detected!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
   
    cv2.imshow("output", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
