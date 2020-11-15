import numpy as np
import cv2
import os

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = 'rtsp_transport;udp'

cap = cv2.VideoCapture('rtsp://192.168.42.1/live', cv2.CAP_FFMPEG)

ret, frame = cap.read()

while ret:
    cv2.imshow('frame', frame)
    # do other processing on frame...

    ret, frame = cap.read()
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
