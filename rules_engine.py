import json
from datetime import datetime
from light_controller import getLightState
#https://github.com/UselessMnemonic/OpenWiz
lamp_on_time = "15:00:00"
format_time  ="%H:%M:%S"
prev_motion = False
light_state = getLightState()
def processMotionEvent(motion):
    
    global prev_motion, light_state
    #light_state = lightState  #sets the state of the light 

    #motion is happening and not happening before = True
    #motion is happening and it happened before = False
    if motion and not prev_motion: # checks for new motion event , prev_motion = was motion in previous frame, motion = was there motion
        light_state = not light_state

    prev_motion = motion  # sets the previous motion type
    return light_state

def processTemp(temp,humidity):
    kelvin = (2*temp) * humidity * 1.5
    print(kelvin)
    return int(kelvin)
        

def checkTime(lamp_on_time):
    #lamp_on_time = "13:00:00" 
    format_time  ="%H:%M:%S"
    now = datetime.now()
    now = now.strftime("%H:%M:%S")
    
    if datetime.strptime(now,format_time) > datetime.strptime(lamp_on_time,format_time):
        return True
    else: 
        return False


