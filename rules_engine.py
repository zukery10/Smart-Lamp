import json
from datetime import datetime
from light_controller import getLightState
from sense_hat import SenseHat


sense = SenseHat()



#https://github.com/UselessMnemonic/OpenWiz
lamp_on_time = "15:00:00"
format_time  ="%H:%M:%S"
prev_motion = False
light_state = getLightState()


def processMotionEvent(motion, secureMode,temp):
    global prev_motion, light_state
    #light_state = lightState  #sets the state of the light 
    #motion is happening and not happening before = True
    #motion is happening and it happened before = False

    if not motion: #if no motion then the previous motion is false - no motion before motion?????
        prev_motion = False

    if motion and not prev_motion and not secureMode: # checks for new motion event , prev_motion = was motion in previous frame, motion = was there motion
        light_state = not light_state
        sense.clear(0,255,0)
        prev_motion = True  # sets the previous motion type
        print("Motion")

        if not light_state:
            return {"state" : light_state} # https://www.w3schools.com/python/python_dictionaries.asp return a dictionary for more control
        if light_state:
            return {"state" : light_state,
                "temp": temp,
                "r":255,
                "g": 255,
                "b": 255}    


    
    if motion and not prev_motion and secureMode:
        print("Security Breach")
        sense.clear(255,0,0)
        return {"alert" : True,
                "captureVideo" : True,
                "senseLight" : True,
                "state" : True,
                "r" : 255} #returns that there's been an alert and captures video
    return None

def processTemp(temp,humidity):
    kelvin = (2*temp) * humidity * 1.5
    #print(kelvin)
    return int(kelvin)
        

def checkTime(lamp_on_time):
    #lamp_on_time = "13:00:00" 
    format_time  ="%H:%M:%S"
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    
    if datetime.strptime(now,format_time) > datetime.strptime(lamp_on_time,format_time):
        return {"time" : True}
    else: 
        return {"time" : False}
    



