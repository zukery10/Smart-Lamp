from motion_sensor_v1 import sense_motion
from rules_engine import  checkTime, processMotionEvent, processTemp
from light_controller import setLightState, getLightState,setLightWarmth,sendUDP
from sense_reader import capture_humidity, capture_temp
from sense_hat import SenseHat
from picamera2 import Picamera2
#from blynk_client import initialise_functions
import time
from pi_camera_capture import capture_photo, capture_video
import BlynkLib
#https://github.com/UselessMnemonic/OpenWiz
sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()


blynk = BlynkLib.Blynk("1GpojHp7VRzUa6ZnrKNetsc_MfdzXPnW")

timeLog = 0
weatherLog = 0
security_mode = False #secure mode is off on startup

security_toggle = 0

#need to figure out method to adapt sensitivity to lighting - brighter light sets off motion

lamp_on_time = "09:00:00"  #set from blynk

@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    print(f'Current button value: {button_value}')
    global security_toggle 
    security_toggle = button_value

while True:
        now = time.time()
        blynk.run()  # Process Blynk events        
        #print("Blynk Running")
        #time.sleep(.01) 



        #===================================================================Security Mode===================================================================

        if security_toggle == "1":
            security_mode = True
            #print("Secure Mode ON")

        if security_toggle == "0":
            security_mode = False
            #print("Secure Mode OFF")
                
        #print(security_toggle)

        #===================================================================Home Mode===================================================================
        #light_state = getLightState()
        timeSet = checkTime(lamp_on_time)
        #print(capture_temp(),capture_humidity())
        #https://www.w3schools.com/python/python_dictionaries_access.asp
        if timeSet["time"] == True: # checks if time set by user for motion/daytime 


            if time.time() - weatherLog > 1800:
                temp = capture_temp()
                hum = capture_humidity()


            if time.time() - timeLog > 0.1:
                detection = sense_motion(camera)
                event = processMotionEvent(detection, security_mode,processTemp(temp,hum))
                
                if event != None:
                    if event.get("secureMode") == True:
                        print("Secure Mode")
                        #send alert to blynk
                        
                        
                        capture_photo(camera,sense)
                        #capture_video(camera)
                timeLog = now           

            if event != None:
                sendUDP(setLightState(event))

            #sendUDP()
            time.sleep(0.1)


    






