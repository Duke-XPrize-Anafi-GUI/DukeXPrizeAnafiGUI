import time
import cv2
#import cv2, time

# creating object -> Zero for external drone camera
video = cv2.VideoCapture(0)

while True:
    # creating a frame

    check, frame = video.read()

    print(check)
    print(frame) # image

    #converting to gray scale

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show the frame

    cv2.imshow("Capturing", frame)

    # For any key press 
    # cv2.waitKey(0)

    # for playing video
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

#shutdown camera
video.release()

cv2.destroyAllWindows()