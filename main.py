from motion_sensor_v1 import sense_motion
from rules_engine import  checkTime, processMotionEvent, processTemp, wake_up_slow, urgent_flashing
from light_controller import setLightState, getLightState,setLightWarmth,sendUDP
from sense_reader import capture_humidity, capture_temp
from sense_hat import SenseHat
from picamera2 import Picamera2
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
alarm_set = True

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

@blynk.on("V6")
def handle_v6_write(value):
    global alarm_time
    alarm_time = value[0]


while True:
        now = time.time()
        blynk.run()  # Process Blynk events        
        #time.sleep(.01) 

        if enter_time_set == "1": #set time of day with enter button
            lamp_on_time = (hours + ":" + minutes +":00")  #set from blynk    
            #blynk.virtual_write(5, lamp_on_time)============================REMEMBER

        #===================================================================Security Mode===================================================================

        if security_toggle == "1":
            security_mode = True
      

        if security_toggle == "0":
            security_mode = False
    
        if alarm_set :
            for i in range(100):
                time.sleep(.05)
                alarm = wake_up_slow(i)
                sendUDP(setLightState(alarm))
                print("SENT")
            if alarm:
                for j in range(100):
                    time.sleep(.4)
                    sendUDP(setLightState(urgent_flashing(j)))
            alarm_set = False #turn off after
   

        #===================================================================Home Mode===================================================================
     
        timeSet = checkTime(lamp_on_time)
        #print(lamp_on_time)
       
        #https://www.w3schools.com/python/python_dictionaries_access.asp
        if timeSet["time"] == True: # checks if time set by user for motion/daytime 
            
            #print("Passed Time Test")

            if time.time() - weatherLog > 1800:
                temp = capture_temp()
                hum = capture_humidity()


            if time.time() - timeLog > 0.1:
                detection = sense_motion(camera)
                event = processMotionEvent(detection, security_mode,processTemp(temp,hum))
                
                if event != None:
                    if event.get("secureMode") == True:
                        print("Secure Mode")
                        capture_photo(camera,sense)
                        url = upload_image('./static/last_visitor.jpg')
                        time.sleep(1)
                        blynk.log_event("movement_detected", f"Movement Detected:\n{url}")
                        
                        
                        
                        #capture_video(camera)
                timeLog = now           

            if event != None:
                sendUDP(setLightState(event))

            #sendUDP()
            time.sleep(0.1)


    






