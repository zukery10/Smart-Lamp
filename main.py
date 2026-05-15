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
from flask_web_api import sunset_time
from cloudinary_upload import upload_image
#https://github.com/UselessMnemonic/OpenWiz
sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()


blynk = BlynkLib.Blynk("1GpojHp7VRzUa6ZnrKNetsc_MfdzXPnW")



# Default values
timeLog = 0
weatherLog = 0
security_mode = False #secure mode is off on startup
security_toggle = 0
minutes = "00"
hours ="12"
enter_time_set = 0
#lamp_on_time = sunset_time()
lamp_on_time = "00:00:00"
# blynk.virtual_write(5,lamp_on_time) #labels the time of sunset/active lamp


@blynk.on("V1")
def handle_v1_write(value):
    button_value = value[0]
    #print(f'Current button value: {button_value}')
    global security_toggle 
    security_toggle = button_value

@blynk.on("V2")
def handle_v2_write(value):
    global hours
    hours = value[0]
    hours = str(hours)
    #print(f'Hours:{hours}')

@blynk.on("V3")
def handle_v3_write(value):
    global minutes 
    minutes = value[0]
    minutes = str(minutes)
  
    
@blynk.on("V4")
def handle_v4_write(value):
    global enter_time_set 
    enter_time_set = value[0]
    print(enter_time_set)
    





while True:
        now = time.time()
        blynk.run()  # Process Blynk events        
        #print("Blynk Running")
        #time.sleep(.01) 

        if enter_time_set == "1": #set time of day with enter button
            lamp_on_time = (hours + ":" + minutes +":00")  #set from blynk    
            #blynk.virtual_write(5, lamp_on_time)
            #print(lamp_on_time)
        #===================================================================Security Mode===================================================================

        if security_toggle == "1":
            security_mode = True
      

        if security_toggle == "0":
            security_mode = False
    
                
   

        #===================================================================Home Mode===================================================================
     
        timeSet = checkTime(lamp_on_time)
        print(lamp_on_time)
       
        #https://www.w3schools.com/python/python_dictionaries_access.asp
        if timeSet["time"] == True: # checks if time set by user for motion/daytime 
            
            print("Passed Time Test")

            if time.time() - weatherLog > 1800:
                temp = capture_temp()
                hum = capture_humidity()


            if time.time() - timeLog > 0.1:
                detection = sense_motion(camera)
                event = processMotionEvent(detection, security_mode,processTemp(temp,hum))
                
                if event != None:
                    if event.get("secureMode") == True:
                        print("Secure Mode")
                        blynk.set_property("V6", "offImageUrl", upload_image('./static/last_visitor.jpg'))
                       #blynk.log_event("movement_detected", "Movement Detected")
                        
                        
                        capture_photo(camera,sense)
                        #capture_video(camera)
                timeLog = now           

            if event != None:
                sendUDP(setLightState(event))

            #sendUDP()
            time.sleep(0.1)


    






