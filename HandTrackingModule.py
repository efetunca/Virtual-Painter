import cv2 as cv
import mediapipe as mp
import time

class handDetection():

    # Defining a function for initialization of "Mediapipe's Hands() function"
    def __init__(self, imageMode=False, maxHandNumber=2, modelComplexity=1, detectConf=0.5, trackConf=0.5):
        self.imageMode = imageMode
        self.maxHandNumber = maxHandNumber
        self.detectConf = detectConf
        self.trackConf = trackConf
        self.modelComplexity = modelComplexity

        # Declaring a 'self' variable to start Mediapipe hand detection module
        self.mpHandModule = mp.solutions.hands

        # Declaring another 'self' variable for detecting hands
        self.detectHands = self.mpHandModule.Hands(self.imageMode, self.maxHandNumber, self.modelComplexity,
                                                   self.detectConf, self.trackConf)

        # Declaring another 'self' variable to draw lines between landmarks of hands
        self.mpDraw = mp.solutions.drawing_utils

        # Creating an array that stores the IDs of fingertips
        self.tipIDs = [4, 8, 12, 16, 20]


    # Defining a function to find hands in the frame
    def findHand(self, frame, draw=True):

        # Converting frame to RGB in order to Mediapipe module to process 
        RGBframe = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.handResult = self.detectHands.process(RGBframe)

        # Marking hand landmarks with Mediapipe
        self.handLandmarks = self.handResult.multi_hand_landmarks
        if self.handLandmarks:
            for landmark in self.handLandmarks:
                if draw:
                    # Showing the landmarks and drawing the lines betweeen points
                    self.mpDraw.draw_landmarks(frame, landmark, self.mpHandModule.HAND_CONNECTIONS)
        
        # As result, the function returns the 'frame' value
        return frame
    
    # Defining a function to find positions of landmarks
    def findPosition(self, frame, handNumber=0, draw=True):

        # Creating an empty array to store position values
        self.landmarkPositions = []

        if self.handLandmarks:
            # Declaring a variable for choosing hand
            handNo = self.handLandmarks[handNumber]
            # Gathering landmark informations
            for id, lm in enumerate(handNo.landmark):
                # Getting height, width and channel info of 'frame'
                height, width, channel = frame.shape

                # Since the 'lm' values gives the decimal values of points,
                # in other words, giving the ratio of points to the 'frame',
                # we have to multiply these values with height and width values of 'frame' to get locations of points.
                posX, posY = int(lm.x * width), int(lm.y * height)

                # Adding calculated X and Y positions with finger IDs to the list which created at the beginning of the function
                self.landmarkPositions.append([id, posX, posY])

                # If 'draw' parameter is set as 'True', then draw circles on each finger landmark
                if draw:
                    cv.circle(frame, (posX, posY), 10, (0, 255, 255), cv.FILLED)

        # As result, the function returns the 'landmarkPositions' value
        return self.landmarkPositions

    # Defining a function to count raised fingers
    def fingersUp(self):

        # Creating an empty array to store situations of fingers
        fingerSituation = []

        # If the Landmark 0 is at the right of the Landmark 1, then there is right hand in the frame
        if self.landmarkPositions[0][1] > self.landmarkPositions[1][1]:
            rightHand = True
        else:
            rightHand = False

        ########################################
        # If a fingertip's landmark is below the previous two indexes relative to its y-coordinate,
        #   it means that, that finger is closed.
        # But if the thumb is closed, the index of the tip will not be below of the previous index;
        #   it's further to the right if it is right hand.
        # Therefore, the x-coordinate of the thumb tip should be checked, not the y-coordinate.
        ########################################

        # If it is right hand, then the thumb tip will be on the left of the previous index when the finger is up/open
        if rightHand:
            if self.landmarkPositions[self.tipIDs[0]][1] < self.landmarkPositions[self.tipIDs[0]-1][1]:
                # If the finger is opened, then add '1' to the 'fingerSituation' list
                fingerSituation.append(1)
            else:
                # If not, add '0' to the list
                fingerSituation.append(0)
        # If it is left hand, the opposite of the previous check should be performed
        else:
            if self.landmarkPositions[self.tipIDs[0]][1] > self.landmarkPositions[self.tipIDs[0]-1][1]:
                fingerSituation.append(1)
            else:
                fingerSituation.append(0)

        # For the other fingers, the y-coordinate of landmarks should be checked
        for i in range(1, 5):
            if self.landmarkPositions[self.tipIDs[i]][2] < self.landmarkPositions[self.tipIDs[i]-2][2]:
                fingerSituation.append(1)
            else:
                fingerSituation.append(0)

        return fingerSituation

def main():

    # Capturing the frames with the built-in webcam
    # The number '0' can be changed according to the webcams connected to PC (eg. VideoCapture(1), VideoCapture(2), ...)
    capture = cv.VideoCapture(0)

    # If camera is not opened, then exit the program.
    if not capture.isOpened():
        print("Camera can not be opened!")
        exit()

    # Declaring a variable to calculate the FPS
    previousTime = 0

    # Initializating the 'handDetection()' function with a variable
    detect = handDetection()

    while True:
        # Capturing frames and giving mirror view
        ret, frame = capture.read()
        frame = cv.flip(frame, 1)

        # Running the 'findHand' function to be able to detect hands 
        frame = detect.findHand(frame)

        # Detecting positions of landmarks and printing them
        landmarkPositions = detect.findPosition(frame)

        # If no hands are detected after the webcam is turned on, the program will give an error
        # To prevent this, the landmark positions are printed only when a landmark is detected
        if len(landmarkPositions) != 0:
            print(landmarkPositions[0])

         # When frames are read correctly, then 'ret' will be True
        if not ret:
            print("Frames can not be received. Exiting...")
            break

        # Calculating the FPS and displaying it on the frame
        currentTime = time.time()
        FPS = 1 / (currentTime - previousTime)
        previousTime = currentTime
        cv.putText(frame, f"FPS: {int(FPS)}", (10, 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Displaying the captured frames
        cv.imshow("Hand Tracking", frame)

        # End the 'while' loop (shortly, kill the program) if the key 'q' is pressed
        if cv.waitKey(1) == ord("q"):
            break
    
    # Releasing the capture and kill the windows that are opened, if everything is done
    capture.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()