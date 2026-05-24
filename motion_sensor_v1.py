#https://pip-assets.raspberrypi.com/categories/652-raspberry-pi-camera-module-2/documents/RP-008156-DS-2-picamera2-manual.pdf?disposition=inline

#cap img = grayscale = blur = compare = print
import cv2 as cv
import numpy as np
import time

from sense_hat import SenseHat


sense = SenseHat()
backgroundFrame = None
motion_counter = 0
def sense_motion(camera):
    
    x,y,w,h = 700,20,200,120 # https://pixspy.com/ - to find x,y,w,h
                                    #https://www.photopea.com/
    
    global backgroundFrame #https://www.w3schools.com/python/python_variables_global.asp - so the main.py can access it
    global motion_counter
    frame = camera.capture_array() #https://forums.raspberrypi.com/viewtopic.php?t=363106#p2178171

    roi = frame[y:y+h, x:x+w] #https://learnopencv.com/cropping-an-image-using-opencv/
    grayScale = cv.cvtColor(roi,cv.COLOR_BGR2GRAY)#https://www.geeksforgeeks.org/python/python-grayscaling-of-images-using-opencv/
    currentFrame = cv.GaussianBlur(grayScale, (21, 21), 0) # blurs image so it removes noise
    #currentFrame = cv.add(currentFrame, np.array([60.0]))  
    cv.rectangle(frame,(700,20),(900,140) ,(0,255,0), 2) #draw a rectangle to debug
    if backgroundFrame is None: 
        backgroundFrame = currentFrame  #captures the first frame
        #continue # then restart while loop to capture current frames


    diff = cv.absdiff(backgroundFrame,currentFrame) #https://docs.opencv.org/4.x/d2/de8/group__core__array.html#ga6fef31bc8c4071cbc114a758a2b79c14     
    _,thresh1 = cv.threshold(diff,30,255,cv.THRESH_BINARY) #https://techskillguru.com/opencv/motion-detector-and-alert-system-in-opencv
    #motion_detection = np.sum(diff) #https://numpy.org/devdocs/reference/generated/numpy.sum.html
    motion_pixels = np.count_nonzero(thresh1) #https://techskillguru.com/opencv/motion-detector-and-alert-system-in-opencv




    #print(motion_pixels)



    if motion_pixels > 3000: #sensitivy
       
        motion_counter += 1
        #time.sleep(1) 
        #print(motion_counter) 
        if motion_counter == 2: #so two motions can set off light, combats extreme lighting change
            return True
            
    else:
        backgroundFrame = cv.addWeighted(currentFrame, 0.01, backgroundFrame, 0.99, 0) #this makes the background adaptive, blends background img to current slowly
        sense.clear()
        cv.imwrite("debug.jpg", frame)
        motion_counter = 0
         
       
    backgroundFrame = currentFrame #update frame to adapt to new lighting
        
        




        


