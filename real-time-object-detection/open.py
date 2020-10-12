"""
Test of the opencv based mambo vision code

Author: Nigel Veach
"""

from pyparrot.Minidrone import Mambo
from pyparrot.DroneVision import DroneVision
# from pyparrot.Model import Model
from imutils.video import VideoStream
from imutils.video import FPS

import threading
import cv2
import time
import numpy as np
import cv2
import os
import argparse
import imutils

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", required=True,
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", required=True,
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))



os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = 'protocol_whitelist;file,tcp,rtp,udp | fflags;nobuffer | flag;low_delay'
mamboAddr = "DC-71-96-21-9C-E7"

# make my mambo object
# remember to set True/False for the wifi depending on if you are using the wifi or the BLE to connect
mambo = Mambo(mamboAddr, use_wifi=True)
print("trying to connect to mambo now")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)
time.sleep(2)
mambo.fps = 30

print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])
# initialize the video stream, allow the cammera sensor to warmup,
# and initialize the FPS counter
print("[INFO] starting video stream...")
cap = cv2.VideoCapture("rtsp://192.168.99.1/media/stream2", cv2.CAP_FFMPEG)
time.sleep(2.0)
fps = FPS().start()

ret, frame = cap.read()

(w, h, c) = frame.shape

#syntax: cv2.resize(img, (width, height))
img = cv2.resize(frame,(400, h))

print(w, h)
print(img.shape)

while ret:
    # grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	ret, frame = cap.read()
	frame = cv2.resize(frame, (400, h))

	# grab the frame dimensions and convert it to a blob
	(w, h) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
		0.007843, (300, 300), 127.5)
	# pass the blob through the network and obtain the detections and
	# predictions
	net.setInput(blob)
	detections = net.forward()

# loop over the detections
	for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]
		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
			idx = int(detections[0, 0, i, 1])
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			# draw the prediction on the frame
			label = "{}: {:.2f}%".format(CLASSES[idx],
				confidence * 100)
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				COLORS[idx], 2)
			y = startY - 15 if startY - 15 > 15 else startY + 15
			cv2.putText(frame, label, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
	# update the FPS counter
	fps.update()
    # stop the timer and display FPS information

fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
cap.release()
cv2.destroyAllWindows()
cap.stop()
mambo.disconnect()
print("disconnect")
# When everything done, release the capture
