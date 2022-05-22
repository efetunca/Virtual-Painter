import cv2 as cv
import numpy as np
import HandTrackingModule as htm

### Information about some lines are not given as they are given in the 'HandTrackingModule' ###

capture = cv.VideoCapture(0)

# The drawing will be done on this frame
# The explanation of why the drawing is made on another frame is given below
drawFrame = np.zeros((720, 1280, 3), np.uint8)

if not capture.isOpened():
    print("Camera can not be opened!")
    exit()

detectFinger = htm.handDetection(maxHandNumber=1)
# Since the drawing process will be done with one hand, the number of hands to be detected is limited to 1

# Declaring brush color and brush size variables for initialization
brushColor = (0, 0, 255)    # Initial brush color is red
brushSize = 15

# Declaring previous X and Y-Coordinates for index finger
# This has to be done for a proper line drawing
# Actually these are not declared as index finger at this point, but will be declared in the 'Drawing Mode' part
prev_X, prev_Y = 0, 0

while True:
    ret, frame = capture.read()
    frame = cv.flip(frame, 1)

    if not ret:
        print("Frames can not be received! Exiting...")
        break

    frame = detectFinger.findHand(frame, draw=False)
    posList = detectFinger.findPosition(frame, draw=False)

    if len(posList) != 0:

        # Drawing 4 rectangles of 90*55 size for color or eraser selection
        #   (Red, Green, Blue and Eraser, respectively)
        #   at the top of the frame
        cv.rectangle(frame, (184, 25), (274, 80), (0, 0, 255), cv.FILLED)
        cv.rectangle(frame, (458, 25), (548, 80), (0, 255, 0), cv.FILLED)
        cv.rectangle(frame, (732, 25), (822, 80), (255, 0, 0), cv.FILLED)
        cv.rectangle(frame, (1006, 25), (1096, 80), (0, 0, 0), cv.FILLED)

        # Declaring variables for X and Y-Coordinates of index and middle fingers.
        index_X, index_Y = posList[8][1:]
        middle_X, middle_Y = posList[12][1:]

        fingerSituation = detectFinger.fingersUp()

        ### Selection Mode ###
        # If index and middle fingers are up at the same time, then it is selection mode
        if fingerSituation[1] and fingerSituation[2]:

            # Reset previous X-Y-Coordinates of index finger after changing mode to selection
            prev_X, prev_Y = 0, 0
            
            # Write 'Select' at the bottom-right of the frame to indicate the mode
            cv.putText(frame, "Select", (1160, 690), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # If middle finger is at the color/eraser selection area, then check the following conditions:
            if middle_Y < 90:

                # Resetting brush size after a selection is made
                # This has to be done due to brush size change for eraser
                # If not, brush size will remain at '65' pixels after the eraser is selected
                brushSize = 15
                if 170 < middle_X < 290:
                    brushColor = (0, 0, 255)
                elif 445 < middle_X < 560:
                    brushColor = (0, 255, 0)
                elif 720 < middle_X < 835:
                    brushColor = (255, 0, 0)
                elif 995 < middle_X < 1110:
                    brushColor = (0, 0, 0)
                    brushSize = 65      # To erase easily
            
            # Draw a rectangle between index and middle finger to indicate selection mode and selected color
            cv.rectangle(frame, (index_X, index_Y-30), (middle_X, middle_Y+30), brushColor, cv.FILLED)

        ### Drawing Mode ###
        # If index finger is up and middle finger is down at the same time, then it is drawing mode
        if fingerSituation[1] and fingerSituation[2]==False:

            # Write 'Draw' at the bottom-right of the frame to indicate the mode
            cv.putText(frame, "Draw", (1180, 690), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # Draw a circle at the tip of the index finger to indicate drawing mode and selected color
            cv.circle(frame, (index_X, index_Y), brushSize, brushColor, cv.FILLED)

            # If X-Y-Coordinates of index finger are '0', then equalize them to current coordinates of index finger
            # This part is only runs when this program is started with drawing mode or when a new color/eraser is selected
            # If these values were not equalized to current coordinates,
            #   then program would start drawing a line directly from the 0,0 coordinate to the coordinate where the finger is currently located
            if prev_X==0 and prev_Y==0:
                prev_X, prev_Y = index_X, index_Y
            
            # Draw a line on 'drawFrame' between previous and current coordinates of index finger
            cv.line(drawFrame, (prev_X, prev_Y), (index_X, index_Y), brushColor, brushSize)
            
            # After drawing the line, change previous coordinate values with current coordinate values
            prev_X, prev_Y = index_X, index_Y
            
    ########################################
    # Since the 'frame' refreshes continuously, drawn lines will not be permanent.
    # They will be visible only momentarily and then erased due to refreshing.
    # To prevent this, the drawing should be done on another frame (namely 'drawFrame') and then merged with the main frame (namely 'frame').
    # This process can be done with threshold of drawFrame.
    #######################################

    # To apply threshold with OpenCV, the image must be converted to gray first
    grayFrame = cv.cvtColor(drawFrame, cv.COLOR_BGR2GRAY)

    # After converting to gray, threshold can be applied
    var, frameThreshold = cv.threshold(grayFrame, 10, 255, cv.THRESH_BINARY_INV)

    # Then threshold applied image is converted again to RGB (BGR in terms of OpenCV)
    convertedFrame = cv.cvtColor(frameThreshold, cv.COLOR_GRAY2BGR)

    # The 'frame' is merged with 'convertedFrame' with 'bitwise and' method to show the drawn lines on the 'frame'
    frame = cv.bitwise_and(frame, convertedFrame)

    # Then the merged frame is merged with 'drawFrame' but this time with 'bitwise or' method to show the colors of the lines
    frame = cv.bitwise_or(frame, drawFrame)

    ########################################
    # To make it more clear; the drawn lines could be shown on the 'frame with just one line:
    #       frame = cv.bitwise_or(frame, drawFrame)
    # but due to alpha channels, the lines appear semi-transparent.
    # This is where thresholding comes into play.
    # With thresholding, the lines are drawn with 8-bit colors, from white to black.
    # The 'convertedFrame' and 'frameThreshold' has no difference as appearance since threshold image consist of black and white.
    # But we have to convert threshold image to RGB first to be able to merge it with 'frame'.
    # When we merged 'convertedFrame' and 'frame' with bitwise and,
    #   the white parts of 'convertedFrame' will not be shown and the lines on it will be shown as black or black-ish.
    # To colorize the black lines with the colors we have selected, we merge the merged 'frame' and 'drawFrame' with bitwise or.
    #######################################

    cv.imshow("Virtual Painter", frame)
    
    if cv.waitKey(1) == ord("q"):
        break

capture.release()
cv.destroyAllWindows()