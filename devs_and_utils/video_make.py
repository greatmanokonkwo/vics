import numpy as np
import cv2
import time

def gstreamer_pipeline():
	return (
		"nvarguscamerasrc ! "
		"video/x-raw(memory:NVMM), "
		"width=(int)2464, height=(int)2464, "
		"format=(string)NV12, framerate=(fraction)60/1 ! "
		"nvvidconv flip-method=0 ! "
		"video/x-raw, width=(int)2464, height=(int)2464, format=(string)BGRx ! "
		"nvegltransform ! nveglglessink -e"
	)


cap = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)


# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

start = time.time()
while(time.time() - start < 10):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
