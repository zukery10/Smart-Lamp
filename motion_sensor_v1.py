#https://pip-assets.raspberrypi.com/categories/652-raspberry-pi-camera-module-2/documents/RP-008156-DS-2-picamera2-manual.pdf?disposition=inline

#cap img = grayscale = blur = compare = print
import socket # this is a network library
import cv2 as cv
import numpy as np
from picamera2 import Picamera2
import time, os,json
from sense_hat import SenseHat
from picamera2.encoders import H264Encoder
import datetime

#use os to set up base and static folder 
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #get current directory
STATIC_DIR = os.path.join(BASE_DIR, "static") #set static directory path
os.makedirs(STATIC_DIR, exist_ok=True) #create static directory if it doesn't exist
IMAGE_PATH = os.path.join(STATIC_DIR, "last_visitor.jpg") #set image path

sense = SenseHat()
camera = Picamera2()

x,y,w,h = 640,87,191,160 # https://pixspy.com/ - to find x,y,w,h
#https://www.photopea.com/

capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()

output = "lastVisitor.h264"
encoder = H264Encoder()



def capture_video(filename="lastVisitor.h264", duration=2):
    print("Recording video...")
    camera.start_recording(encoder,output)
    time.sleep(duration)
    print("Stopped video...")
    camera.stop_recording()
    camera.stop()
    
def capture_photo():
    print("Capturing visitor photo...")
    camera.capture_file(IMAGE_PATH)
    sense.clear(0, 255, 0)  # flash green
    time.sleep(0.1)
    sense.clear(0, 0, 0)
    print("Photo saved to:", IMAGE_PATH)

def sense_motion():
    x,y,w,h = 640,87,191,160 # https://pixspy.com/ - to find x,y,w,h
                                    #https://www.photopea.com/
    backgroundFrame = None
    triggered = None
    time_triggered = None
    while True:

        frame = camera.capture_array() #https://forums.raspberrypi.com/viewtopic.php?t=363106#p2178171

        roi = frame[y:y+h, x:x+w] #https://learnopencv.com/cropping-an-image-using-opencv/
        grayScale = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)#https://www.geeksforgeeks.org/python/python-grayscaling-of-images-using-opencv/
        currentFrame = cv.GaussianBlur(grayScale, (21, 21), 0) # blurs image so it removes noise
        cv.rectangle(frame,(x,x+w),(y,y+h), (255,0,0), 2) #draw a rectangle to debug
        if backgroundFrame is None: 
            backgroundFrame = currentFrame  #captures the first frame
            continue # then restart while loop to capture current frames


        diff = cv.absdiff(backgroundFrame,currentFrame) #https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga6fef31bc8c4071cbc114a758a2b79c14    
        motion_detection = np.mean(diff) #https://numpy.org/devdocs/reference/generated/numpy.sum.html
        #print(motion_detection)


        if motion_detection > 10:
            triggered = True
            if time_triggered is None: # gets the time triggered
                time_triggered = time.time()

            duration = time.time() - time_triggered #time taken from trigger to now
            


            if duration >= .5: #if the time taken in motion is less then .5 of a second send the message, avg time to talk through a door
                sense.clear(255,0,0)
                print("Motion")
                time.sleep(1)
                return True  
        else:
            backgroundFrame = cv.addWeighted(currentFrame, 0.05, backgroundFrame, 0.95, 0) #this makes the background adaptive, blends background img to current slowly
            sense.clear()
            cv.imwrite("debug.jpg", frame)
            time_triggered = None # resets
            triggered = False # resets
            
            
    
    


            


