from motion_sensor_v1 import sense_motion
from rules_engine import  checkTime, processMotionEvent, processTemp
from light_controller import setLightState, getLightState,setLightWarmth,sendUDP
from sense_reader import capture_humidity, capture_temp
from sense_hat import SenseHat
from picamera2 import Picamera2
import time
from pi_camera_capture import capture_photo
#https://github.com/UselessMnemonic/OpenWiz
sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()


security_mode = False #secure mode is off on startup

#need to figure out method to adapt sensitivity to lighting - brighter light sets off motion

lamp_on_time = "09:00:00"
while True:
    #time.sleep(.5) 
    #Security Mode
    for event in sense.stick.get_events():
        if event.action == "pressed":
            security_mode = not security_mode
            if security_mode :
                print("Secure Mode ON")


    #Home Mode
    light_state = getLightState()
    timeSet = checkTime(lamp_on_time)
    
    #https://www.w3schools.com/python/python_dictionaries_access.asp
    if timeSet["time"] == True: # checks if time set by user for motion/daytime 


        #print("On time")
        print(f"motion = {sense_motion(camera)}")
        event = processMotionEvent(sense_motion(camera), security_mode)

        if event != None:
            if event.get("alert") == True and event.get("captureVideo") == True:
                capture_photo(camera,sense)
                print("Secure Mode")

        #print(event)
        sendUDP(setLightState(event))

        #sendUDP(setLightWarmth(processTemp(capture_temp(),capture_humidity())))

    






