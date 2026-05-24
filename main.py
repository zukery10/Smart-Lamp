from motion_sensor_v1 import sense_motion
from rules_engine import  checkTime, processMotionEvent, processTemp, wake_up_slow, checkExactTime,urgent_flashing
from light_controller import setLightState,sendUDP
from sense_reader import capture_humidity, capture_temp
from sense_hat import SenseHat
from picamera2 import Picamera2
import time,os
from pi_camera_capture import capture_photo
import BlynkLib
from flask_web_api import sunset_time,run_flask
from cloudinary_upload import upload_image
from datetime import datetime
import threading
from dotenv import find_dotenv, load_dotenv
#https://github.com/UselessMnemonic/OpenWiz
sense = SenseHat()
camera = Picamera2()
capture_config = camera.create_video_configuration()
camera.configure(capture_config)
camera.start()


dotenv_path = find_dotenv() #load the enviroment variable file
load_dotenv(dotenv_path)

BLYNK_AUTH_TOKEN = os.getenv("BLYNK_AUTH_TOKEN") #uses the .env file to get blynk token
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

print(BLYNK_AUTH_TOKEN)



# Default values/Initialising Variables
timeLog = 0
weatherLog = 0
security_mode = False #secure mode is off on startup
security_toggle = 0
minutes = "00"
hours ="12"
enter_time_set = 0


enter_alarm_set = 0
alarm_minutes = "00"
alarm_hours ="00"
alarm_on_time = "00:00"
alarm_active = "0"
alarm_step = 0
last_alarm_update = 0

#lamp_on_time = sunset_time()
lamp_on_time = "00:00:00"
# blynk.virtual_write(5,lamp_on_time) #labels the time of sunset/active lamp

event = None



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
    global alarm_active
    alarm_active = value[0]
    print(alarm_active)

@blynk.on("V7")
def handle_v7_write(value):
    global alarm_hours
    alarm_hours = value[0]
    alarm_hours = str(alarm_hours)
    print(alarm_hours)

@blynk.on("V8")
def handle_v8_write(value):
    global alarm_minutes 
    alarm_minutes = value[0]
    alarm_minutes = str(alarm_minutes)
    print(alarm_minutes)

@blynk.on("V9")
def handle_v9_write(value):
    global enter_alarm_set 
    enter_alarm_set = value[0]
    print(enter_alarm_set)
  

def log_movement(check_event_type): #Inserts info from top to bottom - newest to oldest
    with open('static/movement_log.txt','r') as f:  #https://www.reddit.com/r/learnpython/comments/mz31yw/how_can_i_append_write_a_line_to_the_top_and/
        text = f.read() #reads exisiting text
    if check_event_type.get("secureMode") == True: #adds new text then plus old text - overwrites old text to add new
        with open('static/movement_log.txt','w') as f: #https://www.pythontutorial.net/python-basics/python-write-text-file/
            f.write(f"SECURITY BREACH at {datetimeNow.strftime("%m/%d/%Y, %H:%M:%S")}\n" + text)#https://www.programiz.com/python-programming/datetime/strftime

    else:
        with open('static/movement_log.txt','w') as f: #https://www.pythontutorial.net/python-basics/python-write-text-file/
            f.write(f"Movement Detected at {datetimeNow.strftime("%m/%d/%Y, %H:%M:%S")}\n"+ text)#https://www.programiz.com/python-programming/datetime/strftime


#https://www.youtube.com/watch?v=STEOavXqXkQ
chore2 = threading.Thread(target=run_flask) #initialises the thread to start another def simultaneously
chore2.start() #starts flask
while True:
        datetimeNow = datetime.now() #for movement log
        now = time.time() #for time processing
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

        #===================================================================Alarm Mode===================================================================
        
        if alarm_active == "1":
            if enter_alarm_set == "1": #set time of day with enter button
                alarm_on_time = (alarm_hours + ":" + alarm_minutes)
                print(alarm_on_time)
            
            alarmSet = checkExactTime(alarm_on_time)
            #alarmSet = checkExactTime("19:03")
            if alarmSet["time"] == True and event is None:
                
                if time.time() - last_alarm_update > 1:
                    alarm = wake_up_slow(alarm_step)
                    sendUDP(setLightState(alarm))
                    alarm_step += 1
                    last_alarm_update = now
                    if alarm_step == 99 :
                        alarm_active = False #turn off after
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
#===================================================================Security Mode===================================================================                    
                    if event.get("secureMode") == True:
                        print("Secure Mode")
                        capture_photo(camera,sense)
                        url = upload_image('./static/last_visitor.jpg')
                        time.sleep(.05)
                       
                        print(url)
                        #blynk.log_event("movement_detected", f"Movement Detected:\n{url}")
   
                        
                        #capture_video(camera)
                timeLog = now           

            if event != None:
                alarm_active = False
                sendUDP(setLightState(event))
                log_movement(event)
                
            time.sleep(0.1)


    






